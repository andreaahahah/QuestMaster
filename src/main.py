import json
import webbrowser
from pathlib import Path

from agenti.narrative_agent import load_lore, process_lore_with_llama
from agenti.pddl_generator_agent import generate_pddl_files_from_lore
from agenti.validator_agent import validate_pddl
from agenti.web_agent import genera_frontend_con_chat
from agenti.json_generator_agent import json_generator
from src.file_dei_path import guida_path, lore_path, esempi_path, domain_path ,problem_path, domain_file, problem_file,domain_file_corretto, problem_file_corretto,graph_path,path_html, esempio1_path

def save_pddl_files(domain_str, problem_str):
    with open(domain_path, 'w') as f:
        f.write(domain_str)
    with open(problem_path, 'w') as f:
        f.write(problem_str)

def main():
    try:

        print("CREAZIONE DELLA STORIA DALLA LORE\n")
        lore_output = process_lore_with_llama(lore_path)

        print("\nGENRAZIONE PDDL\n")
        pddl_files = generate_pddl_files_from_lore(lore_output, esempi_path, guida_path)

        # creo file
        save_pddl_files(pddl_files["domain"], pddl_files["problem"])

        # Chiamo la validazione
        validate_pddl(0,domain_file,problem_file)

        validate_pddl(1,domain_file_corretto,problem_file_corretto)

        #fase2

        #llm che si prende la storia e i constraint e genera il grafo in json
        grafo = json_generator(lore_output,lore_path)

        grafo = (json.dumps(grafo, indent=2, ensure_ascii=False))
        with open(graph_path, 'w') as f:
            f.write(grafo)

        #il json viene mandato all'llm che genra il frontend e siamo tutti felici

        genera_frontend_con_chat(
            graph_path,
            esempio1_path,
            path_html
        )

        html_path = Path(path_html).absolute().as_uri()
        webbrowser.open(html_path)
    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")

if __name__ == "__main__":
    main()
