import subprocess
from pathlib import Path

from src.agenti import reflection_agent

file_path = Path ("documents/output")
esempi_path = Path ("documents/esempi_storie")
guida_path = Path("documents/guida_pddl/guida_pddl.txt")

def validate_pddl():
    # Path già in formato WSL
    domain_file = "/mnt/c/Users/butterfly/Desktop/ciao/MAGISTRALE/AI/llama3/src/documents/output/domain.pddl"
    problem_file = "/mnt/c/Users/butterfly/Desktop/ciao/MAGISTRALE/AI/llama3/src/documents/output/problem.pddl"

    try:
        wsl_working_directory = "/wsl.localhost/Ubuntu/home/andrea/downward"

        # Comando come stringa
        command = (
            "cd /home/andrea/downward && "
            f"./fast-downward.py {domain_file} {problem_file} --search 'astar(ff())'"
        )

        full_command = ["wsl", "sh", "-c", command]

        print(f"Running command: {' '.join(full_command)}")

        result = subprocess.run(full_command, capture_output=True, text=True, timeout=60)

        print("--- STDOUT ---")
        print(result.stdout)
        print("--- STDERR ---")
        #print(result.stderr) CI DA I PROBLEMI DEI FILE PDDL


        if "Solution found" in result.stdout:
            print("✅ Valid PDDL files and solvable problem.")
            return True
        else:
            print("❌ Valid syntax but problem not solvable.")
            reflection_agent.refine_pddl_chat(result.stderr,esempi_path,guida_path)
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


