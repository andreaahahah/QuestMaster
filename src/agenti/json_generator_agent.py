from pathlib import Path
import subprocess
import json

domain_file_corretto = Path(
    r"C:\Users\butterfly\Desktop\ciao\MAGISTRALE\AI\llama3\src\documents\corretti\domain_corretto.pddl")
problem_file_corretto = Path(
    r"C:\Users\butterfly\Desktop\ciao\MAGISTRALE\AI\llama3\src\documents\corretti\problem_corretto.pddl")


def estrai_parametri_da_lore_path(lore_path: Path) -> dict:
    testo = lore_path.read_text()
    params = {}
    for line in testo.splitlines():
        if "depth_min" in line:
            params["depth_min"] = int(line.split(":")[1].strip())
        elif "depth_max" in line:
            params["depth_max"] = int(line.split(":")[1].strip())
        elif "branching_min" in line:
            params["branching_min"] = int(line.split(":")[1].strip())
        elif "branching_max" in line:
            params["branching_max"] = int(line.split(":")[1].strip())
    return params


def genera_prompt_grafo(lore: str, domain: str, problem: str, params: dict) -> str:
    return f"""
Sei un generatore intelligente di storie interattive in formato JSON.

LORE:
{lore}

DOMAIN:
{domain}

PROBLEM:
{problem}

Usa questi vincoli:
- Profondità minima: {params["depth_min"]}
- Profondità massima: {params["depth_max"]}
- Branching factor minimo: {params["branching_min"]}
- Branching factor massimo: {params["branching_max"]}

Genera una struttura ad albero in JSON dove:
- Ogni nodo ha un "testo" (narrazione) che deve essere articolato, abbastanza lungo e poi un array "scelte".
- Ogni scelta ha un "testo" (azione) e un campo "next" con l'id del prossimo nodo.


Formato esempio:
{{
  "inizio": {{
    "testo": "Inizio della storia...",
    "scelte": [
      {{
        "testo": "Vai a nord",
        "next": "nodo_1"
      }},
      {{
        "testo": "Parla con il vecchio",
        "next": "nodo_2"
      }}
    ]
  }},
  "nodo_1": {{
    "testo": "Ti incammini verso nord...",
    "scelte": [...]
  }},
  ...
}}

Genera tutto il grafo, partendo da "inizio", fino alla profondità massima.
"""

def json_generator(
    lore: str,
    lore_path: Path
) -> dict:
    params = estrai_parametri_da_lore_path(lore_path)
    domain = domain_file_corretto.read_text()
    problem = problem_file_corretto.read_text()
    prompt = genera_prompt_grafo(lore, domain, problem, params)

    print("🧠 Invio prompt a Ollama...\n")

    proc = subprocess.Popen(
        ["ollama", "run", "llama3"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = proc.communicate(prompt)

    if stderr:
        print("❌ Errore Ollama:", stderr)

    # Cerca di estrarre il JSON dallo stdout
    try:
        start = stdout.find("{")
        end = stdout.rfind("}") + 1
        json_output = stdout[start:end]
        grafo = json.loads(json_output)
        print("✅ Grafo generato con successo.")
        return grafo
    except Exception as e:
        print("❌ Errore nella conversione in JSON:", e)
        return {}

