import tkinter as tk
from tkinter import filedialog
import sqlite3
from PIL import Image, ImageTk
import os

DB_PATH = "apostila.db"

class Pagina:
    def __init__(self, master, id_pagina, db_conn):
        self.master = master
        self.id_pagina = id_pagina
        self.db_conn = db_conn
        self.frame = tk.Frame(master)
        self.titulo = "Título da Página"
        self.texto = "Texto da página."
        self.caminho_imagem = None
        self.label_titulo = tk.Label(self.frame, text=self.titulo, font=("Arial", 16, "bold"))
        self.label_titulo.pack(pady=5)
        self.label_texto = tk.Label(self.frame, text=self.texto, wraplength=450, justify="left")
        self.label_texto.pack(pady=5)
        self.imagem_label = tk.Label(self.frame)
        self.imagem_label.pack()
        self.botao_upload = tk.Button(self.frame, text="Selecionar Imagem", command=self.selecionar_imagem)
        self.botao_upload.pack(pady=10)
        self.botao_editar = tk.Button(self.frame, text="Editar Página", command=self.abrir_editor)
        self.botao_editar.pack(pady=5)
        self.imagem_tk = None
        self.carregar_dados()

    def carregar_dados(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT titulo, texto, caminho_imagem FROM paginas WHERE id = ?", (self.id_pagina,))
        resultado = cursor.fetchone()
        if resultado:
            self.titulo, self.texto, self.caminho_imagem = resultado
            self.label_titulo.config(text=self.titulo)
            self.label_texto.config(text=self.texto)
            if self.caminho_imagem and os.path.exists(self.caminho_imagem):
                imagem = Image.open(self.caminho_imagem)
                imagem = imagem.resize((400, 400))
                self.imagem_tk = ImageTk.PhotoImage(imagem)
                self.imagem_label.config(image=self.imagem_tk)

    def salvar_dados(self):
        cursor = self.db_conn.cursor()
        cursor.execute("""
            INSERT INTO paginas (id, titulo, texto, caminho_imagem)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                titulo=excluded.titulo,
                texto=excluded.texto,
                caminho_imagem=excluded.caminho_imagem
        """, (self.id_pagina, self.titulo, self.texto, self.caminho_imagem))
        self.db_conn.commit()

    def selecionar_imagem(self):
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos de imagem", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if caminho:
            self.caminho_imagem = caminho
            imagem = Image.open(caminho)
            imagem = imagem.resize((400, 400))
            self.imagem_tk = ImageTk.PhotoImage(imagem)
            self.imagem_label.config(image=self.imagem_tk)
            self.salvar_dados()

    def abrir_editor(self):
        editor = tk.Toplevel(self.frame)
        editor.title("Editar Página")
        editor.geometry("400x300")

        tk.Label(editor, text="Título:").pack(pady=5)
        entrada_titulo = tk.Entry(editor)
        entrada_titulo.insert(0, self.titulo)
        entrada_titulo.pack(fill="x", padx=10)

        tk.Label(editor, text="Texto:").pack(pady=5)
        entrada_texto = tk.Text(editor, height=10)
        entrada_texto.insert("1.0", self.texto)
        entrada_texto.pack(fill="both", padx=10, pady=5, expand=True)

        def salvar():
            self.titulo = entrada_titulo.get()
            self.texto = entrada_texto.get("1.0", "end").strip()
            self.label_titulo.config(text=self.titulo)
            self.label_texto.config(text=self.texto)
            self.salvar_dados()
            editor.destroy()

        botao_salvar = tk.Button(editor, text="Salvar", command=salvar)
        botao_salvar.pack(pady=10)

    def mostrar(self):
        self.frame.pack(fill="both", expand=True)

    def esconder(self):
        self.frame.pack_forget()

class Aplicacao:
    def __init__(self, master):
        self.master = master
        self.master.title("Apostila de Imagens")
        self.master.geometry("500x650")
        self.db_conn = sqlite3.connect(DB_PATH)
        self.criar_tabela()
        self.paginas = [Pagina(master, i+1, self.db_conn) for i in range(3)]
        self.indice_pagina = 0

        self.frame_botoes = tk.Frame(master)
        self.frame_botoes.pack(side="bottom", fill="x", pady=10)

        self.botao_anterior = tk.Button(self.frame_botoes, text="Página Anterior", command=self.pagina_anterior)
        self.botao_anterior.pack(side="left", padx=20)

        self.botao_proximo = tk.Button(self.frame_botoes, text="Próxima Página", command=self.proxima_pagina)
        self.botao_proximo.pack(side="right", padx=20)

        self.atualizar_pagina()

    def criar_tabela(self):
        cursor = self.db_conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS paginas (
                id INTEGER PRIMARY KEY,
                titulo TEXT,
                texto TEXT,
                caminho_imagem TEXT
            )
        """)
        self.db_conn.commit()

    def atualizar_pagina(self):
        for i, pagina in enumerate(self.paginas):
            if i == self.indice_pagina:
                pagina.mostrar()
            else:
                pagina.esconder()

    def pagina_anterior(self):
        if self.indice_pagina > 0:
            self.indice_pagina -= 1
            self.atualizar_pagina()

    def proxima_pagina(self):
        if self.indice_pagina < len(self.paginas) - 1:
            self.indice_pagina += 1
            self.atualizar_pagina()

    def __del__(self):
        self.db_conn.close()

janela = tk.Tk()
app = Aplicacao(janela)
janela.mainloop()
