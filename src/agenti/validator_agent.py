import subprocess
from pathlib import Path


def validate_pddl():
    # converto i path Windows in path WSL
    domain_file =Path( "/mnt/c/Users/butterfly/Desktop/ciao/MAGISTRALE/AI/llama3/src/documents/output/domain.pddl")
    problem_file = Path( "/mnt/c/Users/butterfly/Desktop/ciao/MAGISTRALE/AI/llama3/src/documents/output/problem.pddl")



    try:
        command = [
            "wsl",
            "bash", "-c",
            f'./fast-downward.py {domain_file} {problem_file} --search "astar(lmcut())"'
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=60)
        print(result.stdout)
        if "Solution found" in result.stdout:
            print("✅ Valid PDDL files and solvable problem.")
            return True
        else:
            print("❌ Valid syntax but problem not solvable.")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

