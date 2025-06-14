from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


file_path = Path ("documents/output")

# Funzione per caricare gli esempi PDDL da una cartella
def load_pddl_examples(folder: Path) -> str:
    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError(f"Esempi PDDL non trovati nella cartella: {folder}")

    examples_text = ""
    for file in sorted(folder.glob("*.pddl")):
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            examples_text += f"\n\n;; ESEMPIO: {file.name}\n"
            examples_text += f.read()
    return examples_text.strip()

# Funzione per caricare la guida PDDL
def load_pddl_guide(guide_path: Path) -> str:
    if not guide_path.exists():
        raise FileNotFoundError(f"Guida PDDL non trovata: {guide_path}")

    with open(guide_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()

file = load_pddl_examples(file_path)

# Configurazione LLM
llm = ChatOllama(
    model="llama3",
    temperature=0.7,
)

# Prompt iniziale
system_message = (
    "Sei un esperto di PDDL. Analizza il seguente file PDDL"
    f"{file}" 
    "individua i problemi e suggerisci le modifiche appropriate. "
    "Usa come riferimento gli esempi forniti e la guida PDDL. Interagisci con l'utente e suggerisci le modifiche chiedendo "
    "la sua approvazione o maggiori informazioni o input prima di finalizzare tutte le modifiche."
)

# Funzione di chat interattiva
def refine_pddl_chat(errore: str, esempi_path: Path, guida_path: Path):

    esempi = load_pddl_examples(esempi_path)
    guida = load_pddl_guide(guida_path)

    # Inizializzo il contesto della chat
    history = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Errore dei file:\n{errore}\n\nEsempi di pddl corretti su cui basarsi:\n{esempi}\n\nGuida sintassi pddl:\n{guida}File pddl da revisionare:\n{file}\n\n"}
    ]

    while True:
        # Invio la cronologia al modello
        response = llm.invoke(history)

        print(f"\n🦙 Llama3: {response.content}\n")

        user_input = input("💬 Tu: ")

        if user_input.lower() in ["exit", "esci", "quit"]:
            print("👋 Chat terminata.")
            break

        # Aggiungo la risposta dell'utente alla cronologia
        history.append({"role": "assistant", "content": response.content})
        history.append({"role": "user", "content": user_input})
