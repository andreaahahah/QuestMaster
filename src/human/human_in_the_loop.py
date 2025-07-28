import tkinter as tk
from tkinter import ttk, messagebox

# Percorsi dei file PDDL corretti
domain_file_path = r"C:\Users\butterfly\Desktop\ciao\MAGISTRALE\AI\llama3\src\documents\corretti\domain_corretto.pddl"
problem_file_path = r"C:\Users\butterfly\Desktop\ciao\MAGISTRALE\AI\llama3\src\documents\corretti\problem_corretto.pddl"

def salva_e_valida(domain_text, problem_text, root):
    from src.agenti.validator_agent import validate_pddl


    with open(domain_file_path, "w") as f:
        f.write(domain_text.get("1.0", tk.END))
    with open(problem_file_path, "w") as f:
        f.write(problem_text.get("1.0", tk.END))


    valid = validate_pddl(
        2,
        "/mnt/c/Users/butterfly/Desktop/ciao/MAGISTRALE/AI/llama3/src/documents/corretti/domain_corretto.pddl",
        "/mnt/c/Users/butterfly/Desktop/ciao/MAGISTRALE/AI/llama3/src/documents/corretti/problem_corretto.pddl"
    )

    if valid:
        messagebox.showinfo("Validazione", "I file PDDL sono validi!")
    else:
        messagebox.showerror("Errore di validazione", " I file PDDL non sono validi.")

def apri_editor():

    root = tk.Tk()
    root.title(" Human-in-the-Loop PDDL Editor")

    # Crea il contenitore per le tab
    tab_control = ttk.Notebook(root)

    # Crea le due tab
    domain_tab = ttk.Frame(tab_control)
    problem_tab = ttk.Frame(tab_control)
    tab_control.add(domain_tab, text='domain.pddl')
    tab_control.add(problem_tab, text='problem.pddl')

    # Aggiungi le aree di testo
    domain_text = tk.Text(domain_tab, wrap='word', width=100, height=30)
    problem_text = tk.Text(problem_tab, wrap='word', width=100, height=30)

    # Carica i file se esistono
    try:
        with open(domain_file_path) as f:
            domain_text.insert(tk.END, f.read())
    except FileNotFoundError:
        pass
    try:
        with open(problem_file_path) as f:
            problem_text.insert(tk.END, f.read())
    except FileNotFoundError:
        pass

    domain_text.pack(expand=1, fill='both')
    problem_text.pack(expand=1, fill='both')

    tab_control.pack(expand=1, fill='both', padx=10, pady=10)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    btn_salva = tk.Button(btn_frame, text=" Salva e Valida", command=lambda: salva_e_valida(domain_text, problem_text, root))
    btn_chiudi = tk.Button(btn_frame, text=" Chiudi", command=root.destroy)

    btn_salva.pack(side='left', padx=10)
    btn_chiudi.pack(side='left')

    root.mainloop()

