from pathlib import Path
import ollama

#carica il documento della lore
def load_lore(filepath: Path ) -> str:
    if not filepath.exists():
        raise FileNotFoundError(f"Lore file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()

def ask_llama3(prompt: str) -> str:
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response['message']['content']

def process_lore_with_llama(lore_path: Path) -> str:
    lore_text = load_lore(lore_path)
    prompt = (
        "Analizza la seguente descrizione di quest fantasy e genera una lista di azioni chiave "
        "che il protagonista potrebbe intraprendere per completarla. Includi anche una sintesi "
        "strutturata con stato iniziale, obiettivo e ostacoli principali.\n\n"
        f"{lore_text}"
    )
    return ask_llama3(prompt)
