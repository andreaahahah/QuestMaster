#creare un agente che data la storia e degli esempi completi genera i file pddl
#usare un agente con memoria in modo da evitare di caricare sempre i file e inoltre nella fase successiva quando dovremo validare il pddl lo ricorda.

from pathlib import Path
import ollama


# Carica tutti gli esempi PDDL come contesto
def load_pddl_examples(folder: Path) -> str:
    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError(f"Esempi PDDL non trovati nella cartella: {folder}")

    examples_text = ""
    for file in sorted(folder.glob("*.pddl")):
        with open(file, "r", encoding="utf-8") as f:
            examples_text += f"\n\n;; ESEMPIO: {file.name}\n"
            examples_text += f.read()
    return examples_text.strip()


# Chiedi a LLaMA3 di generare i file PDDL a partire dalla storia e dalla memoria
def generate_pddl_from_story(story: str, examples: str, guida: str) -> dict:
    prompt = (
        "sei un esperto di planning in pddl"
        "Hai il compito di generare due file PDDL coerenti: `domain.pddl` e `problem.pddl`, "
        "partendo dalla seguente descrizione narrativa. I file devono essere validi e seguire la sintassi PDDL.\n\n"
        "Per le regole di pddl attieniti ed impara da questo testo in modo da non commetter errori"
        f"{guida}\n\n"
        
        " ora, basandoti sulla seguente descrizione narrativa, genera un dominio e un problema, commenta bene ogni riga di codice seguendo la sintassi corretta:\n\n"
        f"{story}\n\n"
        "Hai a disposizione il riassunto di una missione fantasy. Il tuo compito è generare due file PDDL validi:\n\n"
        "1. Un file `domain.pddl` che definisce:\n"
        "- i tipi di oggetti (usando :typing se necessario),\n"
        "- i predicati logici rilevanti,\n"
        "- le azioni STRIPS che il protagonista può intraprendere.\n\n"
        "2. Un file `problem.pddl` che definisce:\n"
        "- gli oggetti specifici della missione,\n"
        "- lo stato iniziale,\n"
        "- lo stato obiettivo,\n"
        "Restituisci solo il contenuto dei due file PDDL nel seguente formato:\n"
        "[DOMAIN]\n...contenuto domain.pddl...\n\n[PROBLEM]\n...contenuto problem.pddl..."
        "UNA VOLTA CHE HAI GENERATO IL PDDL ANALIZZALO E FAI UN AUTOCRITICA GENERALE IN MODO DA VEDERE SE è CORRETTO FACENDO DEL FINE TUNING"
    )

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response["message"]["content"]

    # Estrai i due blocchi separati
    domain_start = content.find("[DOMAIN]")
    problem_start = content.find("[PROBLEM]")

    domain = content[domain_start + len("[DOMAIN]"):problem_start].strip()
    problem = content[problem_start + len("[PROBLEM]"):]

    return {"domain": domain, "problem": problem}


# Funzione principale chiamata da main
def generate_pddl_files_from_lore(lore_text: str, examples_folder: Path,guide_path: Path) -> dict:
    guida = load_pddl_examples(guide_path)
    examples = load_pddl_examples(examples_folder)
    return generate_pddl_from_story(lore_text, examples, guida)
