import subprocess
import sys
from pathlib import Path

def main():
    print("=== Legal Study System ===\n")

    if len(sys.argv) < 3:
        print("Gebruik: python run.py <audiobestand.mp3> <vaknaam>")
        print("Voorbeeld: python run.py hoorcollege.mp3 \"Burgerlijk Recht\"")
        sys.exit(1)

    audio_file = sys.argv[1]
    vak = sys.argv[2]

    audio_path = Path(audio_file)
    if not audio_path.exists():
        print(f"Fout: bestand '{audio_file}' niet gevonden.")
        sys.exit(1)

    transcript_path = audio_path.with_suffix(".txt")

    # Stap 1: Transcriptie
    print(f"[1/2] Transcriberen: {audio_file}")
    result = subprocess.run(
        [sys.executable, "scripts/transcribe.py", audio_file],
        capture_output=False
    )
    if result.returncode != 0:
        print("Fout tijdens transcriptie. Gestopt.")
        sys.exit(1)

    # Stap 2: Verwerking
    print(f"\n[2/2] Verwerken: {transcript_path} → {vak}")
    result = subprocess.run(
        [sys.executable, "scripts/process_lecture.py", str(transcript_path), vak],
        capture_output=False
    )
    if result.returncode != 0:
        print("Fout tijdens verwerking. Gestopt.")
        sys.exit(1)

    print("\n✓ Alles klaar. Open Obsidian om je notitie te bekijken.")
    print(f"  Vergeet niet: schrijf eerst zelf wat je weet VOOR je de notitie leest.")


if __name__ == "__main__":
    main()