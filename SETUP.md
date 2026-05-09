# Legal Study System — Setup Tutorial

Volledig installatiehandboek voor het juridisch studiesysteem.  
Platform: **Windows** | Niveau: **beginner/intermediate**

---

## Inhoudsopgave

1. [Benodigdheden](#1-benodigdheden)
2. [Python installeren](#2-python-installeren)
3. [Git installeren](#3-git-installeren)
4. [VS Code installeren](#4-vs-code-installeren)
5. [Obsidian installeren en inrichten](#5-obsidian)
6. [Anki installeren](#6-anki-installeren)
7. [Projectstructuur aanmaken](#7-projectstructuur-aanmaken)
8. [GitHub repo koppelen](#8-github-repo-koppelen)
9. [API keys instellen](#9-api-keys-instellen)
10. [Virtual environment en libraries](#10-virtual-environment-en-libraries)
11. [Scripts plaatsen](#11-scripts-plaatsen)
12. [Testen](#12-testen)
13. [Dagelijkse workflow](#13-dagelijkse-workflow)
14. [Veelvoorkomende fouten](#14-veelvoorkomende-fouten)

---

## 1. Benodigdheden

Zorg dat je het volgende hebt voordat je begint:

- Een Windows laptop/PC
- Een GitHub account (gratis via github.com)
- Een OpenAI account (platform.openai.com) — creditcard vereist, gebruik ~€0,40/uur audio
- Een Anthropic account (console.anthropic.com) — creditcard vereist, gebruik ~€2–5/maand
- Internetverbinding

---

## 2. Python installeren

**Download**  
Ga naar: https://python.org/downloads  
Download Python 3.12 (of nieuwer).

**Installatie**  
Open het installatieprogramma.  
⚠️ Vink **"Add Python to PATH"** aan — dit is verplicht.  
Klik Install Now.

**Controleer**  
Open Command Prompt (zoek op `cmd` in de Windows zoekbalk):
```
python --version
```
Verwachte output: `Python 3.12.x`

Als je een foutmelding ziet: herinstalleer en zorg dat je PATH aanvinkt.

---

## 3. Git installeren

**Download**  
Ga naar: https://git-scm.com  
Download Git for Windows.

**Installatie**  
Gebruik de standaardinstellingen. Klik steeds op Next.

**Controleer**
```
git --version
```
Verwachte output: `git version 2.x.x`

---

## 4. VS Code installeren

**Download**  
Ga naar: https://code.visualstudio.com  
Download en installeer.

**Python extensie**  
Open VS Code → klik op het blokjes-icoontje in de linkerzijbalk (Extensions) → zoek op `Python` → installeer de extensie van Microsoft.

---

## 5. Obsidian

### Installeren

Ga naar: https://obsidian.md  
Download en installeer.

### Vault openen

Open Obsidian → klik **Open folder as vault** → navigeer naar:
```
Documents\legal-study\vault
```

### Templates plugin aanzetten

Ga naar: Settings (tandwiel) → Core plugins → zet **Templates** aan.

Ga daarna naar: Settings → Templates → stel in:
- Template folder location: `templates`
- Date format: `YYYY-MM-DD`

### Templatebestanden aanmaken

Maak drie bestanden aan in de `templates` map van je vault.

**hoorcollege.md**
```
---
datum: {{date}}
vak: 
week: 
tags: [hoorcollege]
---

# Hoorcollege — Week 

## Eigen aantekeningen (schrijf dit EERST, zonder hulp)

## Kernbegrippen

## Wetsartikelen

## Jurisprudentie
⚠️ Verifieer alles op rechtspraak.nl

## Wat de docent benadrukte

## Vragen die ik nog heb

## AI-verwerkte versie

## Delta: wat miste ik?
```

**jurisprudentie.md**
```
---
ecli: 
datum: {{date}}
instantie: 
vak: 
tags: [jurisprudentie]
---

# [Naam arrest]

ECLI geverifieerd op rechtspraak.nl: [ ]

## Rechtsvraag

## Feiten

## Redenering rechter

## Criterium

## Ratio decidendi

## Gevolg voor rechtspraktijk

## Anki-kaart aangemaakt: [ ]
```

**exam-sim.md**
```
---
datum: {{date}}
vak: 
niveau: 
tags: [exam-sim]
---

# Exam Sim

## Casus

## Mijn antwoord (timer: ___ min, gesloten boek)

## Claude feedback
Score: /10

Verbeterpunten:
1. 
2. 
3. 

## Herschreven antwoord

## Toegevoegd aan error database: [ ]
```

### Template gebruiken

Om een template in te voegen in een nieuwe notitie:  
`Ctrl+P` → typ `template` → kies **Templates: Insert template** → kies het gewenste template.

---

## 6. Anki installeren

Ga naar: https://apps.ankiweb.net  
Download en installeer.

Anki hoef je nu verder niet te configureren. De flashcards worden later automatisch als CSV aangeleverd door het script.

**CSV importeren (later, na eerste scriptrun)**  
Open Anki → File → Import → selecteer het CSV-bestand uit `exports/anki/`

Instellingen bij import:
- Type: Basic
- Field 1 → Front
- Field 2 → Back  
- Field 3 → Tags

---

## 7. Projectstructuur aanmaken

Open Command Prompt en voer dit uit:

```cmd
cd %USERPROFILE%\Documents
mkdir legal-study
cd legal-study
mkdir scripts prompts exports vault
mkdir vault\vakken vault\templates vault\errors vault\inbox vault\meta
mkdir exports\anki
```

Maak daarna twee bestanden aan in de `legal-study` map.

**.gitignore** (maak aan via VS Code of Notepad):
```
.env
venv/
.obsidian/
*.mp3
*.mp4
*.wav
*.m4a
__pycache__/
*.pyc
.DS_Store
```

**README.md**:
```markdown
# Juridisch Studie Systeem

Privé systeem voor het verwerken van hoorcolleges, wetgeving en tentamenvoorbereiding.

## Focus
- Begrip van juridische concepten
- Structurering van studiemateriaal
- Herhaling via flashcards
```

---

## 8. GitHub repo koppelen

### Repo aanmaken op GitHub

1. Ga naar github.com → log in
2. Klik op **New repository**
3. Naam: `legal-study`
4. Zet op **Private**
5. Klik **Create repository**

### Lokale map koppelen

Open Command Prompt in je `legal-study` map:

```cmd
git init
git add .
git commit -m "init: project setup"
git branch -M main
git remote add origin https://github.com/JOUW-GEBRUIKERSNAAM/legal-study.git
git push -u origin main
```

Vervang `JOUW-GEBRUIKERSNAAM` door je GitHub gebruikersnaam.

### Dagelijkse git-routine

```cmd
git add .
git commit -m "omschrijving van wat je deed"
git push
```

Commit naming convention:
```
study:   aantekeningen of samenvattingen toegevoegd
build:   script toegevoegd of aangepast
fix:     fout opgelost
prompt:  prompt aangepast
error:   fout toegevoegd aan error database
review:  weekreview bijgewerkt
```

---

## 9. API keys instellen

### OpenAI key

1. Ga naar: https://platform.openai.com
2. Log in of maak een account aan
3. Klik rechtsboven op je naam → **API keys**
4. Klik **Create new secret key**
5. Kopieer de key (begint met `sk-`)

### Anthropic key

1. Ga naar: https://console.anthropic.com
2. Log in of maak een account aan
3. Ga naar **API Keys**
4. Klik **Create Key**
5. Kopieer de key (begint met `sk-ant-`)

### Keys opslaan

Open het bestand `.env` in VS Code en vul in:

```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxx
```

⚠️ Dit bestand staat in `.gitignore` en komt nooit op GitHub.  
⚠️ Deel deze keys nooit met anderen.

---

## 10. Virtual environment en libraries

Open Command Prompt in je `legal-study` map:

```cmd
python -m venv venv
venv\Scripts\activate
```

Je ziet nu `(venv)` voor je cursor. Dit betekent dat de omgeving actief is.

Installeer de benodigde libraries:

```cmd
pip install openai anthropic python-dotenv
pip freeze > requirements.txt
```

**Belangrijk**: activeer de venv altijd opnieuw als je een nieuw Command Prompt venster opent:
```cmd
venv\Scripts\activate
```

---

## 11. Scripts plaatsen

Zet de twee scripts in de `scripts/` map. Maak de bestanden aan via VS Code.

### scripts/transcribe.py

```python
import openai
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def transcribe(audio_path: str, language: str = "nl") -> str:
    client = openai.OpenAI()
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language=language
        )
    return result.text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Gebruik: python scripts/transcribe.py <audiobestand.mp3>")
        sys.exit(1)

    audio_file = sys.argv[1]
    output_file = Path(audio_file).with_suffix(".txt")

    print(f"Transcriberen: {audio_file}...")
    transcript = transcribe(audio_file)

    output_file.write_text(transcript, encoding="utf-8")
    print(f"Klaar. Transcript opgeslagen als: {output_file}")
```

### scripts/process_lecture.py

```python
import anthropic
import json
import sys
import csv
from pathlib import Path
from datetime import date
from dotenv import load_dotenv

load_dotenv()

PROMPT = """
Je bent een juridisch studieassistent voor een HBO Rechten student.
Verwerk het onderstaande transcript naar gestructureerde studieoutput.

TRANSCRIPT:
{transcript}

Geef output UITSLUITEND als geldig JSON. Geen backticks. Geen tekst ervoor of erna.

{{
  "summary": "markdown samenvatting, max 400 woorden",
  "key_terms": [
    {{
      "term": "begrip",
      "definition": "max 2 zinnen",
      "wetsartikel": "bijv. art. 6:162 BW, of null"
    }}
  ],
  "flashcards": [
    {{
      "front": "vraag die begrip en toepassing test, geen definitieherkenning",
      "back": "antwoord max 3 zinnen + wetsartikel"
    }}
  ],
  "articles": ["genoemde wetsartikelen"],
  "jurisprudentie": ["genoemde uitspraken"],
  "tentamenwaarschuwingen": ["wat de docent benadrukte als tentamenstof"]
}}
"""

def process(transcript: str) -> dict:
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": PROMPT.format(transcript=transcript)
        }]
    )
    raw = response.content[0].text.strip()
    return json.loads(raw)

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
    for t in data['key_terms']:
        art = f" ({t['wetsartikel']})" if t.get('wetsartikel') else ""
        note += f"- **{t['term']}**{art}: {t['definition']}\n"

    note += "\n## Wetsartikelen\n"
    for a in data['articles']:
        note += f"- {a}\n"

    note += "\n## Jurisprudentie\n"
    for j in data['jurisprudentie']:
        note += f"- {j} ⚠️ VERIFIEER OP RECHTSPRAAK.NL\n"

    note += "\n## Tentamenwaarschuwingen\n"
    for w in data['tentamenwaarschuwingen']:
        note += f"- {w}\n"

    out_path = out_dir / f"{today}-{vak_slug}.md"
    out_path.write_text(note, encoding="utf-8")
    print(f"Notitie opgeslagen: {out_path}")

def save_flashcards(data: dict, vak: str):
    today = date.today().isoformat()
    vak_slug = vak.lower().replace(" ", "-")
    out_dir = Path("exports/anki")
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / f"{today}-{vak_slug}.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for card in data['flashcards']:
            writer.writerow([card['front'], card['back'], vak_slug])

    print(f"Flashcards opgeslagen: {out_path}")
    print(f"Importeer in Anki via: File → Import")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Gebruik: python scripts/process_lecture.py <transcript.txt> <vaknaam>")
        sys.exit(1)

    transcript_file = sys.argv[1]
    vak = sys.argv[2]

    transcript = Path(transcript_file).read_text(encoding="utf-8")

    print("Verwerken via Claude...")
    data = process(transcript)

    save_note(data, vak)
    save_flashcards(data, vak)
    print("Klaar.")
```

Commit daarna:
```cmd
git add .
git commit -m "build: scripts toegevoegd"
git push
```

---

## 12. Testen

### Stap 1 — Testbestand maken

Neem een minuut audio op via je telefoon en zet het bestand als `test.mp3` in je `legal-study` map. Of gebruik elk ander kort MP3-bestand.

### Stap 2 — Transcriptie testen

```cmd
venv\Scripts\activate
python scripts/transcribe.py test.mp3
```

Verwachte output:
```
Transcriberen: test.mp3...
Klaar. Transcript opgeslagen als: test.txt
```

Controleer: staat er een `test.txt` bestand met leesbare tekst?

### Stap 3 — Verwerking testen

```cmd
python scripts/process_lecture.py test.txt "Burgerlijk Recht"
```

Verwachte output:
```
Verwerken via Claude...
Notitie opgeslagen: vault/vakken/burgerlijk-recht/aantekeningen/2026-05-09-burgerlijk-recht.md
Flashcards opgeslagen: exports/anki/2026-05-09-burgerlijk-recht.csv
Klaar.
```

Controleer:
- Staat er een `.md` bestand in `vault/vakken/burgerlijk-recht/aantekeningen/`?
- Staat er een `.csv` bestand in `exports/anki/`?

### Stap 4 — Anki importeren

Open Anki → File → Import → selecteer het CSV-bestand.

### Stap 5 — Commit

```cmd
git add .
git commit -m "study: eerste test geslaagd"
git push
```

---

## 13. Dagelijkse workflow

```cmd
cd %USERPROFILE%\Documents\legal-study
venv\Scripts\activate
python scripts/transcribe.py hoorcollege.mp3
python scripts/process_lecture.py hoorcollege.txt "Vaknaam"
git add . && git commit -m "study: vaknaam week X" && git push
```

Daarna:
1. Open Obsidian → lees de gegenereerde notitie
2. Vul de **Delta** sectie in: wat miste je in je eigen aantekeningen?
3. Open Anki → importeer de CSV → doe je dagelijkse reviews (15–20 min)

---

## 14. Veelvoorkomende fouten

**`python` wordt niet herkend**  
→ Python is niet aan PATH toegevoegd. Herinstalleer en vink "Add Python to PATH" aan.

**`ModuleNotFoundError: No module named 'openai'`**  
→ Venv is niet actief. Voer eerst uit: `venv\Scripts\activate`

**`AuthenticationError` of `invalid API key`**  
→ Controleer je `.env` bestand. Zijn de keys correct ingevuld zonder spaties?

**`JSONDecodeError` bij process_lecture.py**  
→ Claude heeft geen geldige JSON teruggegeven. Probeer het opnieuw — dit is zeldzaam.

**`.env` staat op GitHub**  
→ Verwijder direct:
```cmd
git rm --cached .env
git commit -m "fix: env verwijderd uit repo"
git push
```
Maak daarna nieuwe API keys aan — de oude zijn gecompromitteerd.

**Obsidian ziet de templates niet**  
→ Controleer in Settings → Templates of de folder correct is ingesteld op `templates`.

---

## Structuuroverzicht

```
legal-study/
├── scripts/
│   ├── transcribe.py          ← audio → tekst
│   └── process_lecture.py     ← tekst → notitie + flashcards
├── vault/
│   ├── vakken/                ← aantekeningen per vak
│   ├── templates/             ← Obsidian templates
│   ├── errors/                ← foutenlogboek
│   ├── inbox/                 ← ruwe aantekeningen
│   └── meta/                  ← evaluatie, exam sim log
├── exports/
│   └── anki/                  ← CSV bestanden voor Anki
├── prompts/                   ← Claude prompts
├── .env                       ← API keys (nooit op GitHub)
├── .gitignore
├── README.md
├── SETUP.md                   ← dit bestand
└── requirements.txt
```

---

*Laatste update: mei 2026*
