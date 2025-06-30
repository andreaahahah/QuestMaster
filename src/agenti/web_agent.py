from pathlib import Path
import subprocess


esempio = Path(r"C:\Users\butterfly\Desktop\ciao\MAGISTRALE\AI\llama3\src\documents\corretti\domain_corretto.pddl")
def genera_prompt_frontend(lore: str, domain: str, problem: str, esempio: str) -> str:
    return f"""
Sei un esperto sviluppatore web. Crea un file HTML completo e valido, con JavaScript incluso inline, che implementi un'interfaccia interattiva per una storia testuale basata sui dati seguenti:

LORE:
{lore}

DOMAIN:
{domain}

PROBLEM:
{problem}

REQUISITI:
1. La pagina deve mostrare un paragrafo di storia.
2. Deve mostrare sotto il paragrafo delle scelte cliccabili (ad esempio: "Vai a nord", "Apri la porta").
3. Quando l'utente clicca su una scelta, la pagina deve inviare una richiesta POST a http://localhost:8000/next con un JSON che contiene:
   {{
     "current_text": testo_corrente,
     "choice": scelta_selezionata
   }}
4. Deve ricevere in risposta un JSON con:
   {{
     "paragrafo": nuovo_testo,
     "scelte": [array_di_nuove_scelte]
   }}
5. La pagina deve aggiornare dinamicamente il paragrafo e le scelte con i dati ricevuti.

ISTRUZIONI:
- Scrivi SOLO il codice HTML completo, partendo da <!DOCTYPE html> fino a </html>.
- Includi tutto il JavaScript necessario dentro un tag <script> nel file HTML.
- Non scrivere spiegazioni, commenti fuori dal codice, o backticks.
- Il codice deve essere eseguibile così com'è senza modifiche.

BASATI SU QUESTO ESEMPIO:
{esempio}

Inizia subito con il codice HTML senza commenti:
"""


def genera_frontend_con_ollama(lore_path: Path, domain_path: Path, problem_path: Path, output_path: Path):
    # carica i file
    lore = lore_path.read_text()
    domain = domain_path.read_text()
    problem = problem_path.read_text()
    esempio_html = esempio.read_text()

    prompt = genera_prompt_frontend(lore, domain, problem,esempio_html)

    print("🧠 Generazione HTML tramite Ollama...\n")

    # chiama Ollama via subprocess
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

    # salva l'output HTML
    output_path.write_text(stdout)

    print(f"✅ Frontend salvato in: {output_path}")
