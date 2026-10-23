
from algoritmos.insercao import ordenar_insercao
from algoritmos.intercalacao import ordenar_intercalacao
from algoritmos.rapida import ordenar_rapida
from algoritmos.hibrida import ordenar_hibrida
from algoritmos.contagem import ordenar_contagem
from algoritmos.base import ordenar_base


algoritmos = [
    ordenar_insercao,
    ordenar_intercalacao,
    ordenar_rapida,
    ordenar_hibrida,
    ordenar_contagem,
    ordenar_base
]

casos = [
    [],
    [5],
    [7, 7, 7],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [-5, 3, -1, 0, 2],
    [8, 3, 5, 1, 9, 2]
]


def test_algoritmos():
    for algoritmo in algoritmos:
        for lista in casos:
            resultado = algoritmo(lista)
            assert resultado == sorted(lista)
            assert lista == casos[casos.index(lista)]


def test_lista_original_preservada():
    for algoritmo in algoritmos:
        lista = [5, -2, 8, 1, 0]
        original = lista.copy()

        algoritmo(lista)

        assert lista == original


def test_contagem_faixa_grande():
    try:
        ordenar_contagem([0, 1000000])
        assert False
    except ValueError:
        pass
