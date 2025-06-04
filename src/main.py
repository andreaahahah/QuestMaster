from pathlib import Path
from agenti.narrative_agent import load_lore, process_lore_with_llama

def main():
    lore_path = Path("documents/Lore.txt")

    print("🧠 Generazione narrativa in corso...\n")
    output = process_lore_with_llama(lore_path)
    print("📜 Risultato:\n")
    print(output)

if __name__ == "__main__":
    main()
