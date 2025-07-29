from pathlib import Path
import json

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

from src.file_dei_path import domain_file_corretto, problem_file_corretto


# Inizializzazione LLM
llm = ChatOllama(model="llama3", temperature=0.7)


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
    print("GENERAZIONE JSON")
    params = estrai_parametri_da_lore_path(lore_path)
    domain = domain_file_corretto.read_text()
    problem = problem_file_corretto.read_text()
    prompt = genera_prompt_grafo(lore, domain, problem, params)

    messages = [
        SystemMessage(content="Rispondi esclusivamente con un oggetto JSON valido che rappresenta la storia."),
        HumanMessage(content=prompt)
    ]

    response = llm.invoke(messages)

    raw_output = response.content

    try:
        start = raw_output.find("{")
        end = raw_output.rfind("}") + 1
        json_output = raw_output[start:end]
        grafo = json.loads(json_output)

        return grafo
    except Exception as e:
        print(raw_output)
        print("Errore nella conversione in JSON:", e)
        return {}
