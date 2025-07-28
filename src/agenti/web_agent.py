from pathlib import Path
import re
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


llm = ChatOllama(model="llama3", temperature=0.9)

#METODO CREATO PER PROBLEMI CON L'ENCODING
def safe_read_text(file_path: Path, encodings=['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']):
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except:
            continue
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def safe_write_text(file_path: Path, content: str, encoding='utf-8'):
    try:
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
    except Exception as e:
        print(f" Errore durante la scrittura: {e}")




def genera_prompt_frontend(json_story: str, esempio1: str) -> str:
    return f"""Crea una pagina HTML completa per una storia interattiva. Usa ESATTAMENTE questo JSON:
{json_story}

ESEMPIO DI RIFERIMENTO:
{esempio1}

ISTRUZIONI CRITICHE:
1. Inizia IMMEDIATAMENTE con <!DOCTYPE html>
2. NON scrivere spiegazioni, commenti o altro testo
3. La pagina deve caricare automaticamente il nodo "inizio"
4. Usa il JSON fornito come storyData
5. Implementa le funzioni loadNode() e gestione scelte
6. Mostra "Fine dell'avventura!" quando non ci sono scelte

FORMATO RICHIESTO:
<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Storia Interattiva</title>
<style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f5f5f5; }}
        #game-container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        #story-text {{ font-size: 18px; line-height: 1.6; margin-bottom: 25px; color: #333; }}
        #choices-container {{ display: flex; flex-direction: column; gap: 10px; }}
        .choice-button {{ background: #007bff; color: white; border: none; padding: 12px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; }}
        .choice-button:hover {{ background: #0056b3; }}
        #game-over {{ text-align: center; font-size: 20px; color: #28a745; margin-top: 20px; }}
</style>
</head>
<body>
<div id="game-container">
<div id="story-text"></div>
<div id="choices-container"></div>
<div id="game-over" style="display: none;">Fine dell'avventura!</div>
</div>
<script>
        const storyData = {json_story};
        function loadNode(nodeKey) {{
            if (!storyData[nodeKey]) return;
            const node = storyData[nodeKey];
            document.getElementById('story-text').innerHTML = node.testo;
            document.getElementById('choices-container').innerHTML = '';
            document.getElementById('game-over').style.display = 'none';
            if (node.scelte && node.scelte.length > 0) {{
                node.scelte.forEach(choice => {{
                    const button = document.createElement('button');
                    button.textContent = choice.testo;
                    button.className = 'choice-button';
                    button.onclick = () => loadNode(choice.next);
                    document.getElementById('choices-container').appendChild(button);
                }});
            }} else {{
                document.getElementById('game-over').style.display = 'block';
            }}
        }}
        window.onload = () => loadNode('inizio');
</script>
</body>
</html>

INIZIA SUBITO CON <!DOCTYPE html>"""


def clean_html_output(raw_output: str) -> str:
    doctype_match = re.search(r'<!DOCTYPE html>', raw_output, re.IGNORECASE)
    start_pos = doctype_match.start() if doctype_match else 0
    end_match = re.search(r'</html>', raw_output, re.IGNORECASE)
    end_pos = end_match.end() if end_match else len(raw_output)
    html_content = raw_output[start_pos:end_pos].strip()
    return html_content


def genera_frontend_con_chat(json_story_path: Path, esempio1_path: Path, output_path: Path):
    if not json_story_path.exists() or not esempio1_path.exists():
        print("Uno dei file richiesti non esiste.")
        return

    json_story = safe_read_text(json_story_path)
    esempio1 = safe_read_text(esempio1_path)

    prompt = genera_prompt_frontend(json_story, esempio1)

    history = [
        SystemMessage(content="Sei un esperto sviluppatore frontend. Rispondi SOLO con il codice HTML richiesto, senza aggiungere commenti o testo extra."),
        HumanMessage(content=prompt)
    ]

    print("GENERAZIONE HTML")
    response = llm.invoke(history)

    html_pulito = clean_html_output(response.content)
    safe_write_text(output_path, html_pulito)


