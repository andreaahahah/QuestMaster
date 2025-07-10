from pathlib import Path
import subprocess

# Path all'esempio HTML (può essere un template minimale già funzionante)
esempio = Path(r"C:\Users\butterfly\Desktop\ciao\MAGISTRALE\AI\llama3\src\documents\corretti\domain_corretto.pddl")


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


def safe_read_text(file_path: Path, encodings=['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']):
    """
    Legge un file di testo provando diversi encoding fino a trovare quello corretto.
    Args:
        file_path: Path al file da leggere
        encodings: Lista di encoding da provare in ordine di priorità
    Returns:
        str: Contenuto del file
    Raises:
        UnicodeDecodeError: Se nessun encoding funziona
    """
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                print(f"✅ File letto con encoding: {encoding}")
                return content
        except UnicodeDecodeError:
            print(f"❌ Fallito con encoding: {encoding}")
            continue
        except Exception as e:
            print(f"❌ Errore durante la lettura con {encoding}: {e}")
            continue
    # Se tutti gli encoding falliscono, prova con 'errors='ignore''
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            print("⚠️ File letto con utf-8 ignorando errori (alcuni caratteri potrebbero essere persi)")
            return content
    except Exception as e:
        raise UnicodeDecodeError(f"Impossibile leggere il file {file_path} con nessun encoding testato: {e}")


def safe_write_text(file_path: Path, content: str, encoding='utf-8'):
    """
    Scrive un file di testo con gestione sicura dell'encoding.
    Args:
        file_path: Path dove salvare il file
        content: Contenuto da scrivere
        encoding: Encoding da usare (default: utf-8)
    """
    try:
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        print(f"✅ File scritto con encoding: {encoding}")
    except Exception as e:
        print(f"❌ Errore durante la scrittura: {e}")
        # Fallback: prova con utf-8 ignorando errori
        try:
            with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(content)
            print("⚠️ File scritto con utf-8 ignorando errori")
        except Exception as e2:
            raise Exception(f"Impossibile scrivere il file: {e2}")


def genera_frontend_con_ollama(json_story_path: Path, output_path: Path):
    """
    Genera un frontend HTML usando Ollama con gestione corretta dell'encoding.
    """
    try:
        # Carica i file con gestione sicura dell'encoding
        esempio1_path = Path(r"C:\Users\butterfly\Desktop\ciao\MAGISTRALE\AI\llama3\src\esempi_web\esempio1.txt")
        # Verifica che i file esistano
        if not esempio1_path.exists():
            print(f"❌ File non trovato: {esempio1_path}")
            return
        if not json_story_path.exists():
            print(f"❌ File non trovato: {json_story_path}")
            return
        # Leggi i file con gestione sicura dell'encoding
        print("📖 Lettura dei file...")
        esempio1 = safe_read_text(esempio1_path)
        json_story = safe_read_text(json_story_path)
        # Genera prompt
        prompt = genera_prompt_frontend(json_story, esempio1)
        print("🧠 Generazione HTML tramite Ollama...\n")
        # Chiama Ollama via subprocess con encoding UTF-8
        proc = subprocess.Popen(
            ["ollama", "run", "llama3"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'  # Sostituisce caratteri non decodificabili
        )
        stdout, stderr = proc.communicate(prompt)
        if stderr:
            print("❌ Errore Ollama:", stderr)
        if stdout:
            # Pulisce l'output da eventuali commenti o testo extra
            html_content = clean_html_output(stdout)
            # Salva l'output HTML con gestione sicura dell'encoding
            safe_write_text(output_path, html_content)
            print(f"✅ Frontend salvato in: {output_path}")
        else:
            print("❌ Nessun output ricevuto da Ollama")
    except Exception as e:
        print(f"❌ Errore generale: {e}")


def clean_html_output(raw_output: str) -> str:
    """
    Pulisce l'output di Ollama per estrarre solo il codice HTML valido.
    """
    import re
    # Trova l'inizio del DOCTYPE
    doctype_match = re.search(r'<!DOCTYPE html>', raw_output, re.IGNORECASE)
    if not doctype_match:
        print("⚠️ DOCTYPE non trovato, cerco tag <html>")
        html_match = re.search(r'<html[^>]*>', raw_output, re.IGNORECASE)
        if html_match:
            start_pos = html_match.start()
        else:
            print("❌ Nessun tag HTML valido trovato")
            return raw_output
    else:
        start_pos = doctype_match.start()
    # Trova la fine del tag </html>
    end_match = re.search(r'</html>', raw_output, re.IGNORECASE)
    if end_match:
        end_pos = end_match.end()
        html_content = raw_output[start_pos:end_pos]
    else:
        # Se non trova </html>, prende tutto dal DOCTYPE in poi
        html_content = raw_output[start_pos:]
    # Rimuove eventuali commenti o testo prima/dopo
    html_content = html_content.strip()
    print(f"🧹 HTML pulito: {len(html_content)} caratteri")
    return html_content


# Funzione di utilità per diagnosticare l'encoding di un file
def detect_file_encoding(file_path: Path):
    """
    Tenta di rilevare l'encoding di un file.
    Richiede il pacchetto 'chardet': pip install chardet
    """
    try:
        import chardet
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        result = chardet.detect(raw_data)
        print(f"🔍 Encoding rilevato per {file_path}: {result}")
        return result
    except ImportError:
        print("⚠️ Per il rilevamento automatico dell'encoding, installa: pip install chardet")
        return None
    except Exception as e:
        print(f"❌ Errore nel rilevamento encoding: {e}")
        return None


# Esempio di utilizzo
if __name__ == "__main__":
    # Test della funzione
    json_path = Path("test_story.json")
    output_path = Path("output.html")
    # Opzionalmente, rileva l'encoding prima di leggere
    # detect_file_encoding(json_path)
    # Genera il frontend
    genera_frontend_con_ollama(json_path, output_path)