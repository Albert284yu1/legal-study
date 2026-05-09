# Juridisch Studie Systeem

Een persoonlijk AI-ondersteund studiesysteem voor HBO Rechten, gebouwd rond cognitief effectieve leermethoden en eenvoudige automatisering.

---

## Wat dit systeem doet

Dit systeem neemt een audiobestand van een hoorcollege als input en levert automatisch drie dingen op:

1. Een gestructureerde Obsidian-notitie met samenvatting, kernbegrippen, wetsartikelen en jurisprudentie
2. Een CSV-bestand met flashcards klaar voor import in Anki
3. Een lijst van tentamenwaarschuwingen op basis van wat de docent benadrukte

Daarnaast bevat het een complete studiestructuur met templates voor jurisprudentieanalyse, exam simulations en een foutenlogboek.

---

## Waarom dit je studieresultaten verbetert

Rechtenstudie faalt zelden door gebrek aan informatie. Het faalt door drie concrete problemen:

**Probleem 1: Kennis aanwezig, maar niet beschikbaar onder druk**  
Je begrijpt de stof als je ernaar kijkt, maar bij een tentamen kom je er niet op. Dit is het verschil tussen herkenning en retrieval. Anki lost dit op via spaced repetition — herhaling op het moment dat je het dreigt te vergeten.

**Probleem 2: Begrip aanwezig, toepassing faalt**  
Je weet wat onrechtmatige daad is, maar je past het verkeerd toe in een casus. Dit lost de exam simulator op — oefenen onder tijdsdruk met AI-feedback op je eigen antwoord.

**Probleem 3: Passief studeren voelt productief maar is het niet**  
Samenvatting lezen, slides doorkijken, YouTube-colleges kijken — dit geeft het gevoel van studeren zonder het leereffect. Dit systeem dwingt je tot actieve verwerking: eerst zelf schrijven, dan AI-feedback, dan herschrijven.

Het systeem vervangt geen studie-inspanning. Het zorgt dat de inspanning die je levert effectiever wordt ingezet.

---

## Hoe het werkt

```
Audiobestand (hoorcollege)
        ↓
transcribe.py — OpenAI Whisper API
        ↓
Teksttranscript
        ↓
process_lecture.py — Anthropic Claude API
        ↓
┌─────────────────────┬──────────────────────┐
│ Obsidian notitie    │ Anki CSV             │
│ (vault/vakken/)     │ (exports/anki/)      │
└─────────────────────┴──────────────────────┘
```

Alle output is lokaal opgeslagen op je eigen laptop. Niets wordt automatisch gedeeld of gepubliceerd.

---

## Werkwijze: closed book first

Dit systeem is gebouwd rond één principe: **jij denkt eerst, AI helpt daarna.**

De volgorde bij elk hoorcollege:
1. Maak aantekeningen tijdens het college
2. Sluit je aantekeningen — schrijf uit geheugen op wat je weet
3. Draai het script over de opname
4. Vergelijk de AI-output met jouw eigen versie
5. Noteer wat je miste (de "delta")

Claude opent pas nadat jij al hebt nagedacht. Zo voorkom je passief consumeren van AI-output, wat het leereffect volledig wegneemt.

---

## ⚠️ Kosten en API-gebruik

Dit systeem maakt gebruik van betaalde externe API's. Dit zijn geen abonnementen maar pay-per-use diensten.

### OpenAI Whisper API (transcriptie)
- Kosten: ~€0,006 per minuut audio
- Een college van 60 minuten kost ~€0,36
- Een volledig semester van 200 uur college kost ~€7,20

### Anthropic Claude API (verwerking)
- Kosten: afhankelijk van modelkeuze en hoeveelheid tekst
- Normaal studiegebruik: ~€2–8 per maand

### Wat je nodig hebt
- Een creditcard voor beide accounts
- Een OpenAI account: platform.openai.com
- Een Anthropic account: console.anthropic.com

### Gratis alternatieven

Als je geen geld wil uitgeven aan API's zijn er alternatieven, maar ze vragen meer technische kennis of leveren minder kwaliteit:

| Onderdeel | Betaald (dit systeem) | Gratis alternatief |
|---|---|---|
| Transcriptie | OpenAI Whisper API | Whisper lokaal draaien via Python (trager, vereist goede GPU) |
| Tekstverwerking | Claude API | Gratis tier van Claude.ai of ChatGPT (handmatig kopiëren, geen automatisering) |
| Spaced repetition | Anki (gratis) | Anki (gratis) |
| Notities | Obsidian (gratis) | Obsidian (gratis) |

Voor lokale Whisper zonder API:
```
pip install openai-whisper
whisper hoorcollege.mp3 --language nl
```
Dit werkt, maar is significant trager op een normale laptop zonder GPU.

Voor tekstverwerking zonder API kun je transcripts handmatig kopiëren naar claude.ai of chatgpt.com en de prompts uit de `prompts/` map gebruiken. Je verliest de automatisering, maar de studiewerkwijze blijft intact.

---

## Wat dit systeem niet doet

- Het studeert niet voor je
- Het vervangt het lezen van jurisprudentie en wetgeving niet
- Het garandeert geen hogere cijfers zonder consistente inzet
- Het is geen juridisch adviesgereedschap

**Belangrijk voor rechten**: Claude kan juridische informatie verzinnen die plausibel klinkt maar feitelijk onjuist is. Verifieer altijd:
- Wetsartikelen via wetten.overheid.nl
- Jurisprudentie via rechtspraak.nl
- EU-recht via eur-lex.europa.eu

Gebruik Claude voor redeneren en structureren, nooit als primaire bron voor juridische feiten.

---

## Inhoud van dit systeem

```
legal-study/
├── scripts/
│   ├── transcribe.py          ← audio naar tekst via Whisper
│   └── process_lecture.py     ← tekst naar notitie + flashcards via Claude
├── vault/
│   ├── vakken/                ← aantekeningen per vak
│   ├── templates/             ← Obsidian templates (hoorcollege, jurisprudentie, exam-sim)
│   ├── errors/                ← foutenlogboek
│   ├── inbox/                 ← ruwe aantekeningen, onverwerkt
│   └── meta/                  ← evaluatie per vak, exam sim log
├── exports/
│   └── anki/                  ← CSV bestanden voor Anki-import
├── prompts/                   ← Claude prompts voor handmatig gebruik
├── .env                       ← API keys (staat niet op GitHub)
├── .gitignore
├── requirements.txt
├── SETUP.md                   ← volledige installatiehandleiding
└── README.md                  ← dit bestand
```

---

## Snelstart

Volledige installatiehandleiding: zie [SETUP.md](SETUP.md)

Kort overzicht:
```cmd
# 1. Dependencies installeren
python -m venv venv
venv\Scripts\activate
pip install openai anthropic python-dotenv

# 2. API keys invullen in .env
# OPENAI_API_KEY=...
# ANTHROPIC_API_KEY=...

# 3. College verwerken
python scripts/transcribe.py hoorcollege.mp3
python scripts/process_lecture.py hoorcollege.txt "Burgerlijk Recht"
```

---

## Stack

| Tool | Doel | Kosten |
|---|---|---|
| Python 3.12 | Automatisering | Gratis |
| OpenAI Whisper API | Audiotranscriptie | Pay-per-use |
| Anthropic Claude API | Tekstverwerking en feedback | Pay-per-use |
| Obsidian | Kennisopslag en notities | Gratis |
| Anki | Spaced repetition flashcards | Gratis |
| Git + GitHub | Versiebeheer | Gratis (private repo) |

---

*Persoonlijk studiesysteem*  
