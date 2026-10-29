import random
import statistics
import subprocess
import sys
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox

from algoritmos.insercao import ordenar_insercao
from algoritmos.intercalacao import ordenar_intercalacao
from algoritmos.rapida import ordenar_rapida
from algoritmos.hibrida import ordenar_hibrida
from algoritmos.contagem import ordenar_contagem
from algoritmos.base import ordenar_base
from algoritmos.seletor import escolher, ordenar


# ============================================================
# CONFIGURACOES
# ============================================================

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
REPETICOES_GUI = 5

ALGORITMOS = {
    "Inserção": ordenar_insercao,
    "Intercalação": ordenar_intercalacao,
    "Rápida": ordenar_rapida,
    "Híbrida": ordenar_hibrida,
    "Contagem": ordenar_contagem,
    "Radix Sort": ordenar_base,
}

CENARIOS = [
    "Aleatório - chaves grandes",
    "Faixa restrita",
    "Quase ordenado",
    "Lista pequena",
]


def criar_cenario(nome):
    """Gera dados reproduziveis para cada cenario."""

    gerador = random.Random(42)

    if nome == "Aleatório - chaves grandes":
        return [
            gerador.randint(-1_000_000_000, 1_000_000_000)
            for _ in range(2000)
        ]

    if nome == "Faixa restrita":
        return [
            gerador.randint(0, 50)
            for _ in range(2000)
        ]

    if nome == "Quase ordenado":
        lista = list(range(2000))

        for _ in range(20):
            i = gerador.randrange(len(lista))
            j = gerador.randrange(len(lista))
            lista[i], lista[j] = lista[j], lista[i]

        return lista

    return [8, 3, 5, 1, 9, 2, 7, 4]


def medir(algoritmo, lista, esperado):
    """Retorna a mediana do tempo em milissegundos ou None."""

    tempos = []

    for _ in range(REPETICOES_GUI):
        inicio = time.perf_counter()

        try:
            resultado = algoritmo(lista.copy())
        except ValueError:
            return None

        fim = time.perf_counter()

        if resultado != esperado:
            raise ValueError(
                f"O algoritmo {algoritmo.__name__} "
                "produziu uma ordenacao incorreta."
            )

        tempos.append((fim - inicio) * 1000)

    return statistics.median(tempos)


class AplicativoOrdenacao:
    def __init__(self, janela):
        self.janela = janela
        self.tarefa_em_execucao = False

        self.janela.title("Escolhedor de Ordenação | Projeto G2")
        self.janela.geometry("1120x760")
        self.janela.minsize(900, 650)
        self.janela.configure(bg="#F1F5F9")

        self.configurar_estilos()
        self.criar_interface()

    def configurar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#1E293B",
            fieldbackground="#FFFFFF",
            rowheight=32,
            font=("Segoe UI", 10),
        )
        estilo.configure(
            "Treeview.Heading",
            background="#E2E8F0",
            foreground="#0F172A",
            font=("Segoe UI", 10, "bold"),
            padding=8,
        )
        estilo.map(
            "Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", "#1D4ED8")],
        )
        estilo.configure("TCombobox", padding=7, font=("Segoe UI", 10))

    def criar_interface(self):
        cabecalho = tk.Frame(
            self.janela,
            bg="#172554",
            padx=28,
            pady=22,
        )
        cabecalho.pack(fill="x")

        tk.Label(
            cabecalho,
            text="ESCOLHEDOR DE ORDENAÇÃO",
            font=("Segoe UI", 21, "bold"),
            fg="#FFFFFF",
            bg="#172554",
        ).pack(anchor="w")

        tk.Label(
            cabecalho,
            text="Projeto G2 • Comparação de algoritmos de ordenação",
            font=("Segoe UI", 10),
            fg="#BFDBFE",
            bg="#172554",
        ).pack(anchor="w", pady=(5, 0))

        principal = tk.Frame(
            self.janela,
            bg="#F1F5F9",
            padx=22,
            pady=18,
        )
        principal.pack(fill="both", expand=True)

        painel = tk.Frame(
            principal,
            bg="#FFFFFF",
            padx=18,
            pady=15,
            highlightbackground="#E2E8F0",
            highlightthickness=1,
        )
        painel.pack(fill="x", pady=(0, 14))

        tk.Label(
            painel,
            text="CENÁRIO DE TESTE",
            font=("Segoe UI", 10, "bold"),
            fg="#334155",
            bg="#FFFFFF",
        ).pack(anchor="w")

        linha_cenario = tk.Frame(painel, bg="#FFFFFF")
        linha_cenario.pack(fill="x", pady=(8, 0))

        self.cenario = ttk.Combobox(
            linha_cenario,
            values=CENARIOS,
            state="readonly",
            width=34,
        )
        self.cenario.current(0)
        self.cenario.pack(side="left", padx=(0, 12))

        self.botao_seletor = self.criar_botao(
            linha_cenario,
            "Executar seletor",
            self.executar_seletor,
            "#2563EB",
        )
        self.botao_seletor.pack(side="left", padx=(0, 8))

        self.botao_comparar = self.criar_botao(
            linha_cenario,
            "Comparar algoritmos",
            self.comparar_algoritmos,
            "#0F766E",
        )
        self.botao_comparar.pack(side="left")

        # Segunda linha para evitar que os botoes fiquem espremidos.
        linha_ferramentas = tk.Frame(painel, bg="#FFFFFF")
        linha_ferramentas.pack(fill="x", pady=(10, 0))

        self.botao_testes = self.criar_botao(
            linha_ferramentas,
            "Executar testes",
            self.executar_testes,
            "#7C3AED",
        )
        self.botao_testes.pack(side="left", padx=(0, 8))

        self.botao_graficos = self.criar_botao(
            linha_ferramentas,
            "Gerar gráficos",
            self.gerar_graficos,
            "#475569",
        )
        self.botao_graficos.pack(side="left", padx=(0, 8))

        self.botao_benchmark = self.criar_botao(
            linha_ferramentas,
            "Executar benchmark oficial",
            self.executar_benchmark,
            "#B45309",
        )
        self.botao_benchmark.pack(side="left", padx=(0, 8))

        self.botao_limpar = self.criar_botao(
            linha_ferramentas,
            "Limpar resultados",
            self.limpar,
            "#E2E8F0",
            "#334155",
        )
        self.botao_limpar.pack(side="left")

        indicadores = tk.Frame(principal, bg="#F1F5F9")
        indicadores.pack(fill="x", pady=(0, 14))

        self.valor_metodo = self.criar_indicador(
            indicadores, "MÉTODO ESCOLHIDO", "Aguardando execução"
        )
        self.valor_tempo = self.criar_indicador(
            indicadores, "TEMPO MEDIANO", "--"
        )
        self.valor_elementos = self.criar_indicador(
            indicadores, "ELEMENTOS", "--"
        )

        quadro_tabela = tk.Frame(
            principal,
            bg="#FFFFFF",
            padx=14,
            pady=14,
            highlightbackground="#E2E8F0",
            highlightthickness=1,
        )
        quadro_tabela.pack(fill="both", expand=True)

        tk.Label(
            quadro_tabela,
            text="RESULTADOS DA EXECUÇÃO",
            font=("Segoe UI", 11, "bold"),
            fg="#0F172A",
            bg="#FFFFFF",
        ).pack(anchor="w", pady=(0, 10))

        colunas = ("metodo", "tempo", "status")
        self.tabela = ttk.Treeview(
            quadro_tabela,
            columns=colunas,
            show="headings",
            height=10,
        )

        self.tabela.heading("metodo", text="Algoritmo")
        self.tabela.heading("tempo", text="Tempo mediano (ms)")
        self.tabela.heading("status", text="Resultado")

        self.tabela.column("metodo", width=220)
        self.tabela.column("tempo", width=190, anchor="center")
        self.tabela.column("status", width=430, anchor="w")

        barra = ttk.Scrollbar(
            quadro_tabela,
            orient="vertical",
            command=self.tabela.yview,
        )
        self.tabela.configure(yscrollcommand=barra.set)

        self.tabela.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        self.status = tk.StringVar(
            value="Pronto. Selecione um cenário e escolha uma ação."
        )
        tk.Label(
            principal,
            textvariable=self.status,
            font=("Segoe UI", 9),
            fg="#64748B",
            bg="#F1F5F9",
            anchor="w",
        ).pack(fill="x", pady=(9, 0))

    @staticmethod
    def criar_botao(pai, texto, comando, fundo, texto_cor="#FFFFFF"):
        return tk.Button(
            pai,
            text=texto,
            command=comando,
            bg=fundo,
            fg=texto_cor,
            activebackground=fundo,
            activeforeground=texto_cor,
            relief="flat",
            padx=13,
            pady=9,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )

    def criar_indicador(self, pai, titulo, valor_inicial):
        cartao = tk.Frame(
            pai,
            bg="#FFFFFF",
            padx=15,
            pady=13,
            highlightbackground="#E2E8F0",
            highlightthickness=1,
        )
        cartao.pack(side="left", fill="both", expand=True, padx=(0, 9))

        tk.Label(
            cartao,
            text=titulo,
            font=("Segoe UI", 9, "bold"),
            fg="#64748B",
            bg="#FFFFFF",
        ).pack(anchor="w")

        valor = tk.Label(
            cartao,
            text=valor_inicial,
            font=("Segoe UI", 14, "bold"),
            fg="#1D4ED8",
            bg="#FFFFFF",
        )
        valor.pack(anchor="w", pady=(6, 0))
        return valor

    def obter_lista(self):
        return criar_cenario(self.cenario.get())

    def limpar_tabela(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

    def atualizar_indicadores(self, metodo, tempo, quantidade):
        self.valor_metodo.config(text=metodo)
        self.valor_tempo.config(
            text="--" if tempo is None else f"{tempo:.4f} ms"
        )
        self.valor_elementos.config(text=str(quantidade))

    def executar_seletor(self):
        try:
            lista = self.obter_lista()
            esperado = sorted(lista)
            funcao_escolhida = escolher(lista)

            nome = next(
                (
                    nome
                    for nome, funcao in ALGORITMOS.items()
                    if funcao is funcao_escolhida
                ),
                funcao_escolhida.__name__,
            )

            tempo = medir(ordenar, lista, esperado)

            self.limpar_tabela()
            self.tabela.insert(
                "",
                "end",
                values=(
                    "Escolhedor",
                    f"{tempo:.6f}",
                    f"Método selecionado: {nome}",
                ),
            )

            self.atualizar_indicadores(nome, tempo, len(lista))
            self.status.set("Ordenação concluída e resultado validado.")

        except Exception as erro:
            messagebox.showerror("Erro na execução", str(erro), parent=self.janela)

    def comparar_algoritmos(self):
        try:
            lista = self.obter_lista()
            esperado = sorted(lista)
            funcao_escolhida = escolher(lista)

            nome_escolhido = next(
                (
                    nome
                    for nome, funcao in ALGORITMOS.items()
                    if funcao is funcao_escolhida
                ),
                funcao_escolhida.__name__,
            )

            self.limpar_tabela()
            resultados = []

            for nome, algoritmo in ALGORITMOS.items():
                tempo = medir(algoritmo, lista, esperado)
                resultados.append((nome, tempo))

            validos = [
                (nome, tempo)
                for nome, tempo in resultados
                if tempo is not None
            ]

            if not validos:
                raise RuntimeError("Nenhum algoritmo concluiu a ordenação.")

            melhor_nome, melhor_tempo = min(
                validos,
                key=lambda item: item[1],
            )

            for nome, tempo in resultados:
                if tempo is None:
                    texto_tempo = "--"
                    situacao = "Inadequado para a faixa de valores"
                else:
                    texto_tempo = f"{tempo:.6f}"
                    situacao = "Ordenação correta"

                if nome == nome_escolhido:
                    situacao += " • Selecionado"

                if nome == melhor_nome:
                    situacao += " • Mais rápido"

                self.tabela.insert(
                    "",
                    "end",
                    values=(nome, texto_tempo, situacao),
                )

            self.tabela.insert(
                "",
                "end",
                values=(
                    "Melhor algoritmo fixo",
                    f"{melhor_tempo:.6f}",
                    melhor_nome,
                ),
            )

            tempo_escolhido = next(
                tempo
                for nome, tempo in resultados
                if nome == nome_escolhido
            )
            self.atualizar_indicadores(
                nome_escolhido,
                tempo_escolhido,
                len(lista),
            )

            self.status.set(
                f"Comparação concluída. Mais rápido: {melhor_nome}. "
                f"Seletor escolheu: {nome_escolhido}."
            )

        except Exception as erro:
            messagebox.showerror("Erro na comparação", str(erro), parent=self.janela)

    def executar_testes(self):
        comando = [
            sys.executable,
            "-m",
            "pytest",
            "tests/",
            "-v",
        ]
        self.iniciar_tarefa(
            "Executando testes automatizados...",
            comando,
            "Testes automatizados",
        )

    def gerar_graficos(self):
        comando = [
            sys.executable,
            "benchmarks/gerar_graficos.py",
        ]
        self.iniciar_tarefa(
            "Gerando os quatro gráficos...",
            comando,
            "Geração de gráficos",
        )

    def executar_benchmark(self):
        comando = [
            sys.executable,
            "benchmarks/executar_benchmarks.py",
        ]
        self.iniciar_tarefa(
            "Executando benchmark oficial...",
            comando,
            "Benchmark oficial",
        )

    def iniciar_tarefa(self, mensagem, comando, titulo):
        """Executa comandos externos em segundo plano."""

        if self.tarefa_em_execucao:
            messagebox.showwarning(
                "Operação em andamento",
                "Aguarde a operação atual terminar.",
                parent=self.janela,
            )
            return

        self.tarefa_em_execucao = True
        self.status.set(mensagem)
        self.definir_botoes(False)

        def executar():
            try:
                processo = subprocess.run(
                    comando,
                    cwd=RAIZ_PROJETO,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=300,
                )

                saida = processo.stdout.strip()
                erros = processo.stderr.strip()

                resultado = saida

                if erros:
                    resultado += ("\n\n" if resultado else "") + erros

                sucesso = processo.returncode == 0

                if not resultado:
                    resultado = (
                        "Operação concluída."
                        if sucesso
                        else "O comando terminou com erro."
                    )

            except subprocess.TimeoutExpired:
                resultado = (
                    "A operação ultrapassou cinco minutos "
                    "e foi interrompida."
                )
                sucesso = False

            except Exception as erro:
                resultado = str(erro)
                sucesso = False

            self.janela.after(
                0,
                lambda: self.finalizar_tarefa(
                    titulo,
                    resultado,
                    sucesso,
                ),
            )

        threading.Thread(target=executar, daemon=True).start()

    def definir_botoes(self, habilitados):
        estado = "normal" if habilitados else "disabled"

        for botao in (
            self.botao_seletor,
            self.botao_comparar,
            self.botao_testes,
            self.botao_graficos,
            self.botao_benchmark,
            self.botao_limpar,
        ):
            botao.config(state=estado)

        self.cenario.config(
            state="readonly" if habilitados else "disabled"
        )

    def finalizar_tarefa(self, titulo, resultado, sucesso):
        self.tarefa_em_execucao = False
        self.definir_botoes(True)

        if sucesso:
            self.status.set(f"{titulo}: concluído.")
            messagebox.showinfo(
                titulo,
                resultado,
                parent=self.janela,
            )
        else:
            self.status.set(f"{titulo}: houve um erro.")
            messagebox.showerror(
                titulo,
                resultado or "O comando terminou com erro.",
                parent=self.janela,
            )

    def limpar(self):
        if self.tarefa_em_execucao:
            return

        self.limpar_tabela()
        self.atualizar_indicadores(
            "Aguardando execução",
            None,
            "--",
        )
        self.status.set("Resultados limpos. Pronto para novo teste.")


def iniciar():
    janela = tk.Tk()
    AplicativoOrdenacao(janela)
    janela.mainloop()


if __name__ == "__main__":
    iniciar()
