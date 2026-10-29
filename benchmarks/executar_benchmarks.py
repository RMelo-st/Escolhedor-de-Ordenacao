
import sys
import csv
import random
import statistics
import time
from pathlib import Path

# Localiza a pasta principal do projeto.
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ_PROJETO))

# Importa os algoritmos do projeto.
from algoritmos.insercao import ordenar_insercao
from algoritmos.intercalacao import ordenar_intercalacao
from algoritmos.rapida import ordenar_rapida
from algoritmos.hibrida import ordenar_hibrida
from algoritmos.contagem import ordenar_contagem
from algoritmos.base import ordenar_base
from algoritmos.seletor import escolher, ordenar


# Configurações dos testes.
REPETICOES = 7
SEMENTE = 42

random.seed(SEMENTE)


# Algoritmos fixos que serão comparados.
ALGORITMOS = {
    "Insercao": ordenar_insercao,
    "Intercalacao": ordenar_intercalacao,
    "Rapida": ordenar_rapida,
    "Hibrida": ordenar_hibrida,
    "Contagem": ordenar_contagem,
    "Base_Radix": ordenar_base,
}


def criar_cenarios():
    """Cria os quatro cenários do trabalho."""

    aleatorio = [
        random.randint(-1_000_000_000, 1_000_000_000)
        for _ in range(2000)
    ]

    faixa_restrita = [
        random.randint(0, 50)
        for _ in range(2000)
    ]

    quase_ordenado = list(range(2000))

    # Faz 20 trocas para criar uma lista quase ordenada.
    for _ in range(20):
        i = random.randint(0, len(quase_ordenado) - 1)
        j = random.randint(0, len(quase_ordenado) - 1)

        quase_ordenado[i], quase_ordenado[j] = (
            quase_ordenado[j],
            quase_ordenado[i],
        )

    lista_pequena = [8, 3, 5, 1, 9, 2, 7, 4]

    return {
        "Aleatorio_chaves_grandes": aleatorio,
        "Faixa_restrita": faixa_restrita,
        "Quase_ordenado": quase_ordenado,
        "Lista_pequena": lista_pequena,
    }


def medir(algoritmo, lista, esperado):
    """
    Mede o tempo mediano de um algoritmo.
    Retorna None quando o método não suporta aquele cenário.
    """

    tempos = []

    for _ in range(REPETICOES):
        inicio = time.perf_counter()

        try:
            resultado = algoritmo(lista.copy())
        except ValueError:
            return None

        fim = time.perf_counter()

        # Verifica se o resultado está correto.
        if resultado != esperado:
            raise AssertionError(
                f"O algoritmo {algoritmo.__name__} "
                "produziu um resultado incorreto."
            )

        tempos.append((fim - inicio) * 1000)

    return statistics.median(tempos)


def medir_custo_escolha(lista):
    """Mede somente o tempo necessário para escolher o algoritmo."""

    tempos = []

    for _ in range(REPETICOES):
        inicio = time.perf_counter()
        escolher(lista.copy())
        fim = time.perf_counter()

        tempos.append((fim - inicio) * 1000)

    return statistics.median(tempos)


def medir_seletor(lista, esperado):
    """
    Mede o tempo total do seletor, incluindo a escolha
    do algoritmo e a execução da ordenação.
    """

    tempos = []

    for _ in range(REPETICOES):
        inicio = time.perf_counter()
        resultado = ordenar(lista.copy())
        fim = time.perf_counter()

        if resultado != esperado:
            raise AssertionError(
                "O seletor produziu um resultado incorreto."
            )

        tempos.append((fim - inicio) * 1000)

    return statistics.median(tempos)


def executar():
    """Executa os testes e salva os resultados em CSV."""

    cenarios = criar_cenarios()

    pasta_resultados = RAIZ_PROJETO / "resultados"
    pasta_resultados.mkdir(parents=True, exist_ok=True)

    arquivo_csv = pasta_resultados / "resultados.csv"

    registros = []

    for nome_cenario, lista in cenarios.items():
        esperado = sorted(lista)

        print("\n" + "=" * 60)
        print(f"Cenário: {nome_cenario}")
        print(f"Quantidade de elementos: {len(lista)}")
        print("=" * 60)

        # Mede cada algoritmo fixo.
        tempos_fixos = {}

        for nome, algoritmo in ALGORITMOS.items():
            tempo = medir(algoritmo, lista, esperado)
            tempos_fixos[nome] = tempo

            if tempo is None:
                print(f"{nome}: inadequado para este cenário")

                registros.append({
                    "cenario": nome_cenario,
                    "metodo": nome,
                    "tempo_mediano_ms": "",
                    "custo_escolha_ms": "",
                    "metodo_selecionado": "",
                    "repeticoes": REPETICOES,
                    "status": "Inadequado",
                })
            else:
                print(f"{nome}: {tempo:.6f} ms")

                registros.append({
                    "cenario": nome_cenario,
                    "metodo": nome,
                    "tempo_mediano_ms": f"{tempo:.6f}",
                    "custo_escolha_ms": "",
                    "metodo_selecionado": "",
                    "repeticoes": REPETICOES,
                    "status": "Concluido",
                })

        # Mede o custo de escolha separadamente.
        custo_escolha = medir_custo_escolha(lista)

        # Identifica o algoritmo escolhido.
        metodo_escolhido = escolher(lista).__name__

        # Mede escolha + ordenação.
        tempo_total = medir_seletor(lista, esperado)

        print("\nAnálise do seletor:")
        print(f"Método escolhido: {metodo_escolhido}")
        print(f"Custo da escolha: {custo_escolha:.6f} ms")
        print(f"Tempo total: {tempo_total:.6f} ms")

        # Calcula o melhor algoritmo fixo válido.
        validos = {
            nome: tempo
            for nome, tempo in tempos_fixos.items()
            if tempo is not None
        }

        melhor_nome = min(validos, key=validos.get)
        melhor_tempo = validos[melhor_nome]

        print(
            f"Melhor algoritmo fixo: {melhor_nome} "
            f"({melhor_tempo:.6f} ms)"
        )

        diferenca = tempo_total - melhor_tempo
        print(f"Diferença para o melhor fixo: {diferenca:.6f} ms")

        # Registra também a medição do seletor no CSV.
        registros.append({
            "cenario": nome_cenario,
            "metodo": "Escolhedor",
            "tempo_mediano_ms": f"{tempo_total:.6f}",
            "custo_escolha_ms": f"{custo_escolha:.6f}",
            "metodo_selecionado": metodo_escolhido,
            "repeticoes": REPETICOES,
            "status": "Concluido",
        })

    # Salva todos os resultados.
    campos = [
        "cenario",
        "metodo",
        "tempo_mediano_ms",
        "custo_escolha_ms",
        "metodo_selecionado",
        "repeticoes",
        "status",
    ]

    with open(
        arquivo_csv,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos,
            delimiter=";",
        )

        escritor.writeheader()
        escritor.writerows(registros)

    print("\n" + "=" * 60)
    print("BENCHMARK FINALIZADO")
    print(f"Arquivo CSV: {arquivo_csv}")
    print("=" * 60)


if __name__ == "__main__":
    executar()
