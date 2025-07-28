from pathlib import Path
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.file_dei_path import file_path, esempi_path, guida_path

def load_pddl_folder(folder: Path) -> str:
    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError(f"Cartella non trovata: {folder}")

    content = ""
    for file in sorted(folder.glob("*.pddl")):
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            content += f"\n\n;; FILE: {file.name}\n"
            content += f.read()
    return content.strip()


llm = ChatOllama(
    model="llama3",
    temperature=0.7,
)


def refine_pddl_chat(errore: str):
    esempi = load_pddl_folder(esempi_path)
    guida = load_pddl_folder(guida_path)
    file_content = load_pddl_folder(file_path)

    system_message = (
        "Sei un esperto di PDDL. Analizza i seguenti file PDDL:\n"
        f"{file_content}\n\n"
        "Individua i problemi e suggerisci le modifiche appropriate. "
        "Usa come riferimento gli esempi forniti e la guida PDDL. "
        "Interagisci con l'utente e suggerisci le modifiche chiedendo la sua approvazione, SENZA AGGIUNGERE COMMENTI "
        "o maggiori informazioni o input prima di finalizzare tutte le modifiche."
        "se ti viene detto di applicare le modifiche tu lo fai e NON AGGIUNGI COMMENTI"
    )

    history = [
        SystemMessage(content=system_message),
        HumanMessage(
            content=f"Errore dei file:\n{errore}\n\nEsempi di PDDL corretti su cui basarsi:\n{esempi}\n\nGuida sintassi PDDL:\n{guida}\n\nFile PDDL da revisionare:\n{file_content}\n non aggiungere commenti\n")
    ]

    while True:
        response = llm.invoke(history)
        print(f"\n Llama3: {response.content}\n")

        user_input = input(" Tu {PER CHIUDERE SCRIVERE \"applica modifiche\" }: ")

        #verifico le keywords
        if user_input.lower() in ["exit", "esci", "quit"]:
            print("\n Chat terminata.\n")
            break

        if user_input.lower() in ["applica modifiche"] :

            domain_start = response.content.find("(define (domain")
            problem_start = response.content.find("(define (problem")

            domain_da_salvare = response.content[domain_start :problem_start].strip()
            problem_da_salvare = response.content[problem_start :].strip()

            output_folder = Path("documents/corretti")
            output_folder.mkdir(parents=True, exist_ok=True)

            # salvataggio dei file separati
            domain_file_path = output_folder / "domain_corretto.pddl"
            problem_file_path = output_folder / "problem_corretto.pddl"

            domain_file_path.write_text(domain_da_salvare, encoding="utf-8")
            problem_file_path.write_text(problem_da_salvare, encoding="utf-8")
            break



        history.append(AIMessage(content=response.content))
        history.append(HumanMessage(content=user_input))
