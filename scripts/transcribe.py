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