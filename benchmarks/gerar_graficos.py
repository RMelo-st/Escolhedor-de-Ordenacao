
import csv
from pathlib import Path

import matplotlib.pyplot as plt


# ============================================================
# 1. CONFIGURACOES
# ============================================================

RAIZ_PROJETO = Path(__file__).resolve().parent.parent

ARQUIVO_CSV = RAIZ_PROJETO / "resultados" / "resultados.csv"
PASTA_GRAFICOS = RAIZ_PROJETO / "resultados" / "graficos"

PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)

REPETICOES_ESPERADAS = 7

CENARIOS = {
    "Aleatorio_chaves_grandes": "Aleatório - chaves grandes",
    "Faixa_restrita": "Faixa restrita",
    "Quase_ordenado": "Quase ordenado",
    "Lista_pequena": "Lista pequena",
}

METODOS = {
    "Insercao": "Inserção",
    "Intercalacao": "Intercalação",
    "Rapida": "Rápida",
    "Hibrida": "Híbrida",
    "Contagem": "Contagem",
    "Base_Radix": "Radix Sort",
    "Escolhedor": "Escolhedor",
}

# O seletor retorna uma funcao com um destes nomes.
FUNCOES_METODOS = {
    "ordenar_insercao": "Insercao",
    "ordenar_intercalacao": "Intercalacao",
    "ordenar_rapida": "Rapida",
    "ordenar_hibrida": "Hibrida",
    "ordenar_contagem": "Contagem",
    "ordenar_base": "Base_Radix",
}

ORDEM_METODOS = [
    "Insercao",
    "Intercalacao",
    "Rapida",
    "Hibrida",
    "Contagem",
    "Base_Radix",
    "Escolhedor",
]


# ============================================================
# 2. LEITURA E VALIDACAO DO CSV
# ============================================================

def carregar_resultados():
    """Carrega os resultados produzidos pelo benchmark."""

    if not ARQUIVO_CSV.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado:\n{ARQUIVO_CSV}\n\n"
            "Execute primeiro:\n"
            "python benchmarks/executar_benchmarks.py"
        )

    with open(
        ARQUIVO_CSV,
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")
        dados = list(leitor)

    if not dados:
        raise ValueError("O arquivo CSV nao possui resultados.")

    campos_obrigatorios = {
        "cenario",
        "metodo",
        "tempo_mediano_ms",
        "metodo_selecionado",
        "status",
    }

    campos_disponiveis = set(dados[0].keys())
    faltantes = campos_obrigatorios - campos_disponiveis

    if faltantes:
        raise ValueError(
            "O CSV nao possui as colunas necessarias: "
            + ", ".join(sorted(faltantes))
        )

    return dados


def converter_tempo(valor):
    """Converte um tempo do CSV em numero."""

    if valor is None or not valor.strip():
        return None

    try:
        tempo = float(valor.replace(",", "."))

        if tempo < 0:
            return None

        return tempo

    except ValueError:
        return None


def obter_tempos(dados, cenario):
    """Retorna os tempos validos dos metodos de um cenario."""

    tempos = {}

    for linha in dados:
        if linha["cenario"] != cenario:
            continue

        tempo = converter_tempo(linha["tempo_mediano_ms"])

        if tempo is not None:
            tempos[linha["metodo"]] = tempo

    return tempos


def obter_metodo_escolhido(dados, cenario):
    """Identifica qual algoritmo o seletor escolheu."""

    for linha in dados:
        if (
            linha["cenario"] == cenario
            and linha["metodo"] == "Escolhedor"
        ):
            nome_funcao = linha.get(
                "metodo_selecionado", ""
            ).strip()

            return FUNCOES_METODOS.get(nome_funcao)

    return None


def obter_melhor_fixo(tempos):
    """Retorna o algoritmo fixo mais rapido e seu tempo."""

    fixos = {
        metodo: tempo
        for metodo, tempo in tempos.items()
        if metodo in METODOS and metodo != "Escolhedor"
    }

    if not fixos:
        return None, None

    melhor = min(fixos, key=fixos.get)
    return melhor, fixos[melhor]


def nome_metodo(metodo):
    """Converte o identificador para um nome legivel."""

    return METODOS.get(metodo, metodo)


# ============================================================
# 3. GRAFICO 1 - VISAO GERAL DO DESEMPENHO
# ============================================================

def grafico_desempenho(dados):
    """
    Compara todos os algoritmos em cada cenario.
    Usa escala logaritmica para permitir visualizar
    tempos muito pequenos e muito grandes no mesmo painel.
    """

    fig, eixos = plt.subplots(2, 2, figsize=(15, 10))
    eixos = eixos.flatten()

    for eixo, (cenario, titulo) in zip(eixos, CENARIOS.items()):
        tempos = obter_tempos(dados, cenario)

        metodos = [
            metodo for metodo in ORDEM_METODOS
            if metodo in tempos
        ]

        nomes = [nome_metodo(m) for m in metodos]
        valores = [tempos[m] for m in metodos]

        barras = eixo.bar(nomes, valores)

        eixo.set_title(titulo)
        eixo.set_ylabel("Tempo mediano (ms)")
        eixo.set_yscale("log")
        eixo.tick_params(axis="x", rotation=35)
        eixo.grid(axis="y", alpha=0.25)

        for barra, valor in zip(barras, valores):
            eixo.annotate(
                f"{valor:.4g}",
                (
                    barra.get_x() + barra.get_width() / 2,
                    barra.get_height(),
                ),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                fontsize=8,
            )

    fig.suptitle(
        "1. Visao geral do desempenho dos algoritmos",
        fontsize=15,
    )

    fig.tight_layout(rect=[0, 0, 1, 0.96])

    destino = PASTA_GRAFICOS / "01_desempenho_geral.png"
    fig.savefig(destino, dpi=220, bbox_inches="tight")
    plt.close(fig)

    print(f"Grafico 1 salvo: {destino}")


# ============================================================
# 4. GRAFICO 2 - CUSTO TOTAL DO SELETOR
# ============================================================

def grafico_custo_seletor(dados):
    """
    Compara o tempo total do Escolhedor com o melhor
    algoritmo fixo de cada cenario.
    """

    cenarios = []
    melhores = []
    seletores = []
    rotulos_melhores = []

    for cenario, titulo in CENARIOS.items():
        tempos = obter_tempos(dados, cenario)

        if "Escolhedor" not in tempos:
            continue

        melhor_metodo, melhor_tempo = obter_melhor_fixo(tempos)

        if melhor_metodo is None:
            continue

        cenarios.append(titulo)
        melhores.append(melhor_tempo)
        seletores.append(tempos["Escolhedor"])
        rotulos_melhores.append(nome_metodo(melhor_metodo))

    posicoes = list(range(len(cenarios)))
    altura = 0.36

    fig, eixo = plt.subplots(figsize=(12, 7))

    barras_melhor = eixo.barh(
        [p - altura / 2 for p in posicoes],
        melhores,
        height=altura,
        label="Melhor algoritmo fixo",
    )

    barras_seletor = eixo.barh(
        [p + altura / 2 for p in posicoes],
        seletores,
        height=altura,
        label="Escolhedor: escolha + ordenacao",
    )

    eixo.set_yticks(posicoes)
    eixo.set_yticklabels(cenarios)
    eixo.set_xlabel("Tempo mediano (ms)")
    eixo.set_title("2. Custo total do seletor versus melhor algoritmo fixo")
    eixo.legend()
    eixo.grid(axis="x", alpha=0.25)
    eixo.invert_yaxis()

    maior_valor = max(melhores + seletores) if cenarios else 1
    eixo.set_xlim(0, maior_valor * 1.35)

    for barras in (barras_melhor, barras_seletor):
        for barra in barras:
            valor = barra.get_width()

            eixo.annotate(
                f"{valor:.4g} ms",
                (valor, barra.get_y() + barra.get_height() / 2),
                xytext=(5, 0),
                textcoords="offset points",
                va="center",
                fontsize=8,
            )

    # Informa o vencedor fixo em uma coluna separada.
    for p, nome in enumerate(rotulos_melhores):
        eixo.text(
            1.01,
            p,
            f"Melhor: {nome}",
            transform=eixo.get_yaxis_transform(),
            va="center",
            fontsize=9,
        )

    fig.tight_layout()

    destino = PASTA_GRAFICOS / "02_custo_total_seletor.png"
    fig.savefig(destino, dpi=220, bbox_inches="tight")
    plt.close(fig)

    print(f"Grafico 2 salvo: {destino}")


# ============================================================
# 5. GRAFICO 3 - QUALIDADE DA ESCOLHA
# ============================================================

def grafico_qualidade_escolha(dados):
    """
    Compara o tempo do algoritmo escolhido com o melhor fixo.
    Aqui nao usamos o tempo total do Escolhedor: usamos
    o tempo medido do algoritmo fixo que ele selecionou.
    """

    cenarios = []
    tempos_escolhidos = []
    tempos_melhores = []
    nomes_escolhidos = []
    nomes_melhores = []
    acertos = []

    for cenario, titulo in CENARIOS.items():
        tempos = obter_tempos(dados, cenario)

        escolhido = obter_metodo_escolhido(dados, cenario)
        melhor, tempo_melhor = obter_melhor_fixo(tempos)

        if escolhido is None or escolhido not in tempos:
            print(
                f"Aviso: nao foi possivel validar a escolha "
                f"no cenario {titulo}."
            )
            continue

        if melhor is None:
            continue

        cenarios.append(titulo)
        tempos_escolhidos.append(tempos[escolhido])
        tempos_melhores.append(tempo_melhor)
        nomes_escolhidos.append(nome_metodo(escolhido))
        nomes_melhores.append(nome_metodo(melhor))
        acertos.append(escolhido == melhor)

    posicoes = list(range(len(cenarios)))
    altura = 0.36

    fig, eixo = plt.subplots(figsize=(12, 7))

    barras_escolhido = eixo.barh(
        [p - altura / 2 for p in posicoes],
        tempos_escolhidos,
        height=altura,
        label="Algoritmo escolhido",
    )

    barras_melhor = eixo.barh(
        [p + altura / 2 for p in posicoes],
        tempos_melhores,
        height=altura,
        label="Melhor algoritmo fixo",
    )

    eixo.set_yticks(posicoes)
    eixo.set_yticklabels(cenarios)
    eixo.set_xlabel("Tempo mediano de ordenacao (ms)")
    eixo.set_title("3. Qualidade da decisao do seletor")
    eixo.legend()
    eixo.grid(axis="x", alpha=0.25)
    eixo.invert_yaxis()

    maior_valor = max(
        tempos_escolhidos + tempos_melhores
    ) if cenarios else 1

    eixo.set_xlim(0, maior_valor * 1.35)

    for barras in (barras_escolhido, barras_melhor):
        for barra in barras:
            valor = barra.get_width()

            eixo.annotate(
                f"{valor:.4g}",
                (valor, barra.get_y() + barra.get_height() / 2),
                xytext=(5, 0),
                textcoords="offset points",
                va="center",
                fontsize=8,
            )

    # Registra a decisao sem sobrepor os valores das barras.
    for p, (escolhido, melhor, acertou) in enumerate(
        zip(nomes_escolhidos, nomes_melhores, acertos)
    ):
        if acertou:
            texto = f"Acerto: {escolhido}"
        else:
            texto = f"Escolheu: {escolhido} | Melhor: {melhor}"

        eixo.text(
            1.01,
            p,
            texto,
            transform=eixo.get_yaxis_transform(),
            va="center",
            fontsize=8,
        )

    fig.tight_layout()

    destino = PASTA_GRAFICOS / "03_qualidade_escolha.png"
    fig.savefig(destino, dpi=220, bbox_inches="tight")
    plt.close(fig)

    print(f"Grafico 3 salvo: {destino}")


# ============================================================
# 6. GRAFICO 4 - COMPARACAO EM ESCALA LINEAR
# ============================================================

def grafico_linear(dados):
    """
    Mostra os tempos em escala linear.
    Cada cenario tem seu proprio eixo vertical para preservar
    a leitura dos valores pequenos e grandes.
    """

    fig, eixos = plt.subplots(2, 2, figsize=(15, 10))
    eixos = eixos.flatten()

    for eixo, (cenario, titulo) in zip(eixos, CENARIOS.items()):
        tempos = obter_tempos(dados, cenario)

        metodos = [
            metodo for metodo in ORDEM_METODOS
            if metodo in tempos
        ]

        nomes = [nome_metodo(m) for m in metodos]
        valores = [tempos[m] for m in metodos]

        barras = eixo.bar(nomes, valores)

        eixo.set_title(titulo)
        eixo.set_ylabel("Tempo mediano (ms)")
        eixo.tick_params(axis="x", rotation=35)
        eixo.grid(axis="y", alpha=0.25)

        # Comeca em zero: escala linear, sem logaritmo.
        eixo.set_ylim(
            0,
            max(valores) * 1.18 if valores else 1,
        )

        for barra, valor in zip(barras, valores):
            eixo.annotate(
                f"{valor:.4g}",
                (
                    barra.get_x() + barra.get_width() / 2,
                    barra.get_height(),
                ),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                fontsize=8,
            )

    fig.suptitle(
        "4. Comparacao detalhada em escala linear",
        fontsize=15,
    )

    fig.tight_layout(rect=[0, 0, 1, 0.96])

    destino = PASTA_GRAFICOS / "04_comparacao_linear.png"
    fig.savefig(destino, dpi=220, bbox_inches="tight")
    plt.close(fig)

    print(f"Grafico 4 salvo: {destino}")


# ============================================================
# 7. EXECUCAO
# ============================================================

def main():
    try:
        dados = carregar_resultados()

        print(f"Resultados lidos: {len(dados)} registros")
        print(f"Graficos serao salvos em: {PASTA_GRAFICOS}\n")

        grafico_desempenho(dados)
        grafico_custo_seletor(dados)
        grafico_qualidade_escolha(dados)
        grafico_linear(dados)

        print("\nGeracao finalizada.")
        print("Foram gerados quatro graficos.")

    except (FileNotFoundError, ValueError) as erro:
        print(f"\nErro: {erro}")

    except ImportError:
        print(
            "\nMatplotlib nao esta instalado. Execute:\n"
            "python -m pip install matplotlib"
        )


if __name__ == "__main__":
    main()
