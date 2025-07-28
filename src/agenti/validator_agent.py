import subprocess
from src.agenti import reflection_agent
from src.human.human_in_the_loop import apri_editor


def validate_pddl(primavolta,domain_file_corretto,problem_file_corretto):
    # path WSL
    domain_file = "/mnt/c/Users/butterfly/Desktop/ciao/MAGISTRALE/AI/llama3/src/documents/output/domain.pddl"
    problem_file = "/mnt/c/Users/butterfly/Desktop/ciao/MAGISTRALE/AI/llama3/src/documents/output/problem.pddl"

    try:

        if primavolta == 0:
            # Comando come stringa
            command = (
                "cd /home/andrea/downward && "
                f"./fast-downward.py {domain_file} {problem_file} --search 'astar(ff())'"
            )
        else:
            command = (
                "cd /home/andrea/downward && "
                f"./fast-downward.py {domain_file_corretto} {problem_file_corretto} --search 'astar(ff())'"
            )

        full_command = ["wsl", "sh", "-c", command]

        print("VALIDO IL PDDL")

        result = subprocess.run(full_command, capture_output=True, text=True, timeout=60)


        if "Solution found" in result.stdout:
            print("PDDL VALIDI E RISOLVIBILI")
            return True
        else:
            print("SINTASSI VALIDA MA PROBLEMA NON RISOLVIBILE")
            if primavolta == 0:
                reflection_agent.refine_pddl_chat(result.stderr)
            elif primavolta == 1:
                print("COMUNICA CON L'UTENTE PER RISOLVERE I PROBLEMI")
                apri_editor()
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


