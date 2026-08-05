import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.models.estado import Estado

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Estado_Terminal_View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.configurar_janela()
        self.criar_componentes()
        self.configurar_treeview()
        self.configurar_eventos()
        self.atualizar_tabela()

    def configurar_janela(self):
        self.root.title("CRUD de Estados")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

    def criar_componentes(self):
        self.lbl_titulo = tk.Label(
            self.root,
            text="Cadastro de Estados",
            font=("Arial", 16, "bold"),
        )
        self.lbl_titulo.grid(
            row=0,
            column=0,
            columnspan=4,
            padx=5,
            pady=5
        )

        self.frm_dados = tk.LabelFrame(
            self.root,
            text="Dados do Estado"
        )
        self.frm_dados.grid(
            row=1,
            column=0,
            columnspan=4,
            padx=10,
            pady=5,
            sticky="ew"
        )

        self.lbl_id = tk.Label(
            self.frm_dados,
            text="ID:"
        )
        self.lbl_id.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="W"
        )

        self.txt_id = tk.Entry(
            self.frm_dados,
            width=10,
            state="readonly"
        )
        self.txt_id.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="W"
        )

        self.lbl_nome = tk.Label(
            self.frm_dados,
            text="Nome:"
        )
        self.lbl_nome.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="W"
        )

        self.txt_nome = tk.Entry(
            self.frm_dados,
            width=40
        )
        self.txt_nome.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            sticky="W"
        )

        self.lbl_sigla = tk.Label(
            self.frm_dados,
            text="Sigla:"
        )
        self.lbl_sigla.grid(
            row=1,
            column=2,
            padx=5,
            pady=5,
            sticky="W"
        )

        self.txt_sigla = tk.Entry(
            self.frm_dados,
            width=10
        )
        self.txt_sigla.grid(
            row=1,
            column=3,
            padx=5,
            pady=5,
            sticky="W"
        )

        self.frm_botoes = tk.Frame(
            self.root,
            border=2,
            relief="groove"
        )
        self.frm_botoes.grid(
            row=2,
            column=0,
            padx=10,
            pady=5,
            columnspan=4,
        )

        self.btn_novo = tk.Button(
            self.frm_botoes,
            text="Novo",
            width=12,
            command=self.limpar_campos
        )
        self.btn_novo.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.btn_salvar = tk.Button(
            self.frm_botoes,
            text="Salvar",
            width=12,
            command=self.salvar
        )
        self.btn_salvar.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )        

        self.btn_alterar = tk.Button(
            self.frm_botoes,
            text="Alterar",
            width=12,
            command=self.alterar
        )
        self.btn_alterar.grid(
            row=0,
            column=2,
            padx=5,
            pady=5
        )        

        self.btn_excluir = tk.Button(
            self.frm_botoes,
            text="Excluir",
            width=12,
            command=self.excluir
        )
        self.btn_excluir.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )   

        self.btn_fechar = tk.Button(
            self.frm_botoes,
            text="Fechar",
            width=12,
            command=self.root.destroy
        )
        self.btn_fechar.grid(
            row=0,
            column=4,
            padx=5,
            pady=5
        ) 

    def configurar_treeview(self):
        # Frame container para a tabela e barra de rolagem
        self.frm_tabela = tk.Frame(self.root)
        self.frm_tabela.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Configuração das colunas da Treeview
        self.tbl_estados = ttk.Treeview(
            self.frm_tabela,
            columns=("id", "nome", "sigla"),
            show="headings",
            height=12
        )
        
        self.tbl_estados.heading("id", text="ID")
        self.tbl_estados.heading("nome", text="Nome")
        self.tbl_estados.heading("sigla", text="Sigla")

        self.tbl_estados.column("id", width=80, anchor="center")
        self.tbl_estados.column("nome", width=450, anchor="w")
        self.tbl_estados.column("sigla", width=100, anchor="center")

        # Barra de rolagem (Scrollbar)
        self.scrollbar = ttk.Scrollbar(self.frm_tabela, orient="vertical", command=self.tbl_estados.yview)
        self.tbl_estados.configure(yscrollcommand=self.scrollbar.set)

        self.tbl_estados.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def configurar_eventos(self):
        # Evento de clique para selecionar item da tabela
        self.tbl_estados.bind("<<TreeviewSelect>>", self.selecionar_registro)

    # --- Métodos de Ação (CRUD) ---

    def limpar_campos(self):
        self.txt_id.config(state="normal")
        self.txt_id.delete(0, tk.END)
        self.txt_id.config(state="readonly")
        
        self.txt_nome.delete(0, tk.END)
        self.txt_sigla.delete(0, tk.END)
        self.txt_nome.focus_set()

    def selecionar_registro(self, event):
        item_selecionado = self.tbl_estados.selection()
        if item_selecionado:
            valores = self.tbl_estados.item(item_selecionado, "values")
            
            self.txt_id.config(state="normal")
            self.txt_id.delete(0, tk.END)
            self.txt_id.insert(0, valores[0])
            self.txt_id.config(state="readonly")

            self.txt_nome.delete(0, tk.END)
            self.txt_nome.insert(0, valores[1])

            self.txt_sigla.delete(0, tk.END)
            self.txt_sigla.insert(0, valores[2])

    def atualizar_tabela(self):
        # Limpa tabela atual
        for item in self.tbl_estados.get_children():
            self.tbl_estados.delete(item)
            
        # Tenta buscar a lista do controller se disponível
        if hasattr(self.controller, "listar"):
            estados = self.controller.listar()
            for est in estados:
                # Trata caso receba objetos ou dicionários do controller
                if isinstance(est, Estado):
                    self.tbl_estados.insert("", "end", values=(est.id, est.nome, est.sigla))
                elif isinstance(est, (list, tuple)):
                    self.tbl_estados.insert("", "end", values=est)

    def salvar(self):
        nome = self.txt_nome.get().strip()
        sigla = self.txt_sigla.get().strip()

        if not nome or not sigla:
            messagebox.showwarning("Aviso", "Preencha os campos Nome e Sigla.")
            return

        if hasattr(self.controller, "salvar"):
            self.controller.salvar(nome, sigla)
            messagebox.showinfo("Sucesso", "Estado salvo com sucesso!")
            self.limpar_campos()
            self.atualizar_tabela()

    def alterar(self):
        id_estado = self.txt_id.get()
        nome = self.txt_nome.get().strip()
        sigla = self.txt_sigla.get().strip()

        if not id_estado:
            messagebox.showwarning("Aviso", "Selecione um estado para alterar.")
            return

        if hasattr(self.controller, "alterar"):
            self.controller.alterar(id_estado, nome, sigla)
            messagebox.showinfo("Sucesso", "Estado alterado com sucesso!")
            self.limpar_campos()
            self.atualizar_tabela()

    def excluir(self):
        id_estado = self.txt_id.get()

        if not id_estado:
            messagebox.showwarning("Aviso", "Selecione um estado para excluir.")
            return

        if messagebox.askyesno("Confirmação", "Deseja realmente excluir este registro?"):
            if hasattr(self.controller, "excluir"):
                self.controller.excluir(id_estado)
                messagebox.showinfo("Sucesso", "Estado excluído com sucesso!")
                self.limpar_campos()
                self.atualizar_tabela()