import anthropic
import json
import sys
import csv
import re
import time
from pathlib import Path
from datetime import date
from dotenv import load_dotenv

load_dotenv()

# ─── Configuratie ────────────────────────────────────────────────────────────

MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 4096
CHUNK_SIZE = 3000       # woorden per chunk
MAX_RETRIES = 3
RETRY_DELAY = 5         # seconden tussen retries

# Kosten per 1M tokens (mei 2026, controleer console.anthropic.com voor updates)
COST_INPUT_PER_1M  = 3.00   # USD
COST_OUTPUT_PER_1M = 15.00  # USD

# ─── Prompt ──────────────────────────────────────────────────────────────────

PROMPT = """
Je bent een juridisch studieassistent voor een HBO Rechten student in Nederland.
Verwerk het onderstaande transcript naar gestructureerde studieoutput.

TRANSCRIPT:
{transcript}

Geef output UITSLUITEND als geldig JSON. Geen backticks, geen tekst ervoor of erna.
Alle velden zijn verplicht. Gebruik null voor ontbrekende waarden.

{{
  "summary": "markdown samenvatting van de kern van dit college, max 400 woorden",
  "key_terms": [
    {{
      "term": "begrip",
      "definition": "max 2 zinnen, eigen woorden",
      "wetsartikel": "bijv. art. 6:162 BW, of null"
    }}
  ],
  "flashcards": [
    {{
      "front": "vraag die begrip EN toepassing test, geen definitieherkenning",
      "back": "antwoord max 3 zinnen + wetsartikel indien van toepassing"
    }}
  ],
  "articles": ["alle genoemde wetsartikelen, bijv. art. 6:162 BW"],
  "jurisprudentie": ["alle genoemde uitspraken met ECLI indien vermeld"],
  "tentamenwaarschuwingen": ["alles wat de docent benadrukte als tentamenstof"]
}}
"""

MERGE_PROMPT = """
Je hebt een hoorcollege in meerdere delen verwerkt. Hieronder staan de JSON-outputs per deel.
Combineer ze tot één coherente JSON-output. Verwijder duplicaten in key_terms, articles en jurisprudentie.
De summary moet de volledige inhoud van het college omvatten.

DELEN:
{parts}

Geef output UITSLUITEND als geldig JSON. Geen backticks, geen tekst ervoor of erna.
Gebruik hetzelfde JSON-schema als de input.
"""

# ─── Hulpfuncties ────────────────────────────────────────────────────────────

def extract_json(raw: str) -> dict:
    """Haal JSON uit response, ook als er tekst omheen staat."""
    # Eerst proberen of de hele string JSON is
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        pass

    # Zoek naar JSON-blok met regex
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Geen geldige JSON gevonden in response:\n{raw[:500]}")


def call_with_retry(fn, retries=MAX_RETRIES, delay=RETRY_DELAY):
    """Voer een functie uit met automatische retry bij fouten."""
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            if attempt == retries - 1:
                raise
            print(f"  ⚠ Fout: {e}")
            print(f"  Retry {attempt + 1}/{retries - 1} over {delay} seconden...")
            time.sleep(delay)


def split_into_chunks(text: str, chunk_size: int = CHUNK_SIZE) -> list[str]:
    """Splits tekst in chunks van ~chunk_size woorden, op alinea-grenzen."""
    words = text.split()
    if len(words) <= chunk_size:
        return [text]

    chunks = []
    current_words = []

    for word in words:
        current_words.append(word)
        if len(current_words) >= chunk_size and word.endswith('.'):
            chunks.append(' '.join(current_words))
            current_words = []

    if current_words:
        chunks.append(' '.join(current_words))

    return chunks


def calculate_cost(input_tokens: int, output_tokens: int) -> float:
    """Bereken geschatte kosten in USD."""
    cost = (input_tokens / 1_000_000 * COST_INPUT_PER_1M +
            output_tokens / 1_000_000 * COST_OUTPUT_PER_1M)
    return cost

# ─── Verwerking ──────────────────────────────────────────────────────────────

def process_chunk(client: anthropic.Anthropic, transcript: str, chunk_num: int, total: int) -> tuple[dict, int, int]:
    """Verwerk één chunk, geeft (data, input_tokens, output_tokens) terug."""
    print(f"  Chunk {chunk_num}/{total} verwerken...")

    def api_call():
        return client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{
                "role": "user",
                "content": PROMPT.format(transcript=transcript)
            }]
        )

    response = call_with_retry(api_call)
    raw = response.content[0].text.strip()
    data = extract_json(raw)

    return data, response.usage.input_tokens, response.usage.output_tokens


def merge_chunks(client: anthropic.Anthropic, parts: list[dict]) -> tuple[dict, int, int]:
    """Combineer meerdere chunk-outputs tot één."""
    print("  Chunks samenvoegen...")
    parts_json = json.dumps(parts, ensure_ascii=False, indent=2)

    def api_call():
        return client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{
                "role": "user",
                "content": MERGE_PROMPT.format(parts=parts_json)
            }]
        )

    response = call_with_retry(api_call)
    raw = response.content[0].text.strip()
    data = extract_json(raw)

    return data, response.usage.input_tokens, response.usage.output_tokens


def process(transcript: str) -> dict:
    """Verwerk een volledig transcript, met chunking indien nodig."""
    client = anthropic.Anthropic()
    chunks = split_into_chunks(transcript)

    total_input_tokens = 0
    total_output_tokens = 0

    if len(chunks) == 1:
        print(f"Transcript verwerken (1 chunk, {len(transcript.split())} woorden)...")
        data, inp, out = process_chunk(client, chunks[0], 1, 1)
        total_input_tokens += inp
        total_output_tokens += out
    else:
        print(f"Lang transcript gedetecteerd — splitsen in {len(chunks)} chunks...")
        parts = []
        for i, chunk in enumerate(chunks):
            data, inp, out = process_chunk(client, chunk, i + 1, len(chunks))
            parts.append(data)
            total_input_tokens += inp
            total_output_tokens += out

        data, inp, out = merge_chunks(client, parts)
        total_input_tokens += inp
        total_output_tokens += out

    # Cost-tracking output
    cost = calculate_cost(total_input_tokens, total_output_tokens)
    print(f"\n── API-gebruik ──────────────────────────────")
    print(f"  Input tokens:  {total_input_tokens:,}")
    print(f"  Output tokens: {total_output_tokens:,}")
    print(f"  Geschatte kosten: ${cost:.4f} USD (~€{cost * 0.92:.4f})")
    print(f"────────────────────────────────────────────\n")

    return data

# ─── Opslaan ─────────────────────────────────────────────────────────────────

def save_note(data: dict, vak: str):
    today = date.today().isoformat()
    vak_slug = vak.lower().replace(" ", "-")
    out_dir = Path("vault/vakken") / vak_slug / "aantekeningen"
    out_dir.mkdir(parents=True, exist_ok=True)

    note = f"""---
datum: {today}
vak: {vak}
tags: [hoorcollege, {vak_slug}]
---

# {vak} — {today}

## Samenvatting

{data['summary']}

## Kernbegrippen

"""
    for t in data.get('key_terms', []):
        art = f" ({t['wetsartikel']})" if t.get('wetsartikel') else ""
        note += f"- **{t['term']}**{art}: {t['definition']}\n"

    note += "\n## Wetsartikelen\n"
    for a in data.get('articles', []):
        note += f"- {a}\n"

    note += "\n## Jurisprudentie\n"
    for j in data.get('jurisprudentie', []):
        note += f"- {j} ⚠️ VERIFIEER OP RECHTSPRAAK.NL\n"

    note += "\n## Tentamenwaarschuwingen\n"
    for w in data.get('tentamenwaarschuwingen', []):
        note += f"- ⚠️ {w}\n"

    note += "\n## Delta: wat miste ik in mijn eigen aantekeningen?\n\n_Vul dit zelf in na vergelijking._\n"

    out_path = out_dir / f"{today}-{vak_slug}.md"
    out_path.write_text(note, encoding="utf-8")
    print(f"✓ Notitie opgeslagen: {out_path}")


def save_flashcards(data: dict, vak: str):
    today = date.today().isoformat()
    vak_slug = vak.lower().replace(" ", "-")
    out_dir = Path("exports/anki")
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / f"{today}-{vak_slug}.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for card in data.get('flashcards', []):
            writer.writerow([card['front'], card['back'], vak_slug])

    print(f"✓ Flashcards opgeslagen: {out_path} ({len(data.get('flashcards', []))} kaarten)")


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Gebruik: python scripts/process_lecture.py <transcript.txt> <vaknaam>")
        sys.exit(1)

    transcript_file = sys.argv[1]
    vak = sys.argv[2]

    transcript = Path(transcript_file).read_text(encoding="utf-8")
    data = process(transcript)

    save_note(data, vak)
    save_flashcards(data, vak)
    print("\n✓ Klaar.")