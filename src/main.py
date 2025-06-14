from pathlib import Path
from agenti.narrative_agent import load_lore, process_lore_with_llama
from agenti.pddl_generator_agent import generate_pddl_files_from_lore
from agenti.validator_agent import validate_pddl

def save_pddl_files(domain_str, problem_str, domain_path, problem_path):
    with open(domain_path, 'w') as f:
        f.write(domain_str)
    with open(problem_path, 'w') as f:
        f.write(problem_str)
def main():
    try:
        lore_path = Path("documents/Lore.txt")
        guide_path = Path("documents/guida_pddl")
        examples_path = Path("documents/esempi_storie")

        domain_path = Path("documents/output/domain.pddl")
        problem_path = Path("documents/output/problem.pddl")

        print("🧠 Generazione narrativa in corso...\n")
        lore_output = process_lore_with_llama(lore_path)
        print("📜 Storia generata:\n")
        print(lore_output)

        print("\n🧩 Generazione dei file PDDL in corso...\n")
        pddl_files = generate_pddl_files_from_lore(lore_output, examples_path, guide_path)

        print("\n📂 DOMAIN.PDDL:\n")
        print(pddl_files["domain"])
        print("\n📂 PROBLEM.PDDL:\n")
        print(pddl_files["problem"])

        # creo file
        save_pddl_files(pddl_files["domain"], pddl_files["problem"], domain_path, problem_path)

        # ✅ Chiamo la validazione solo dopo aver completato tutto
        validate_pddl()

    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")

if __name__ == "__main__":
    main()
