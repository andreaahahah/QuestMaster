from pathlib import Path
from agenti.narrative_agent import load_lore, process_lore_with_llama
from agenti.pddl_generator_agent import generate_pddl_files_from_lore

def main():
    lore_path = Path("documents/Lore.txt")
    guide_path = Path("documents/guida_pddl")
    examples_path = Path("documents/esempi")

    print("🧠 Generazione narrativa in corso...\n")
    lore_output = process_lore_with_llama(lore_path)
    print("📜 Storia generata:\n")
    print(lore_output)

    print("\n🧩 Generazione dei file PDDL in corso...\n")
    pddl_files = generate_pddl_files_from_lore(lore_output, examples_path,guide_path)

    print("\n📂 DOMAIN.PDDL:\n")
    print(pddl_files["domain"])
    print("\n📂 PROBLEM.PDDL:\n")
    print(pddl_files["problem"])

if __name__ == "__main__":
    main()
