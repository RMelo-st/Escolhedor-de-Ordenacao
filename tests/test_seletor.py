
from algoritmos.seletor import escolher
from algoritmos.insercao import ordenar_insercao
from algoritmos.contagem import ordenar_contagem
from algoritmos.hibrida import ordenar_hibrida
from algoritmos.base import ordenar_base
from algoritmos.intercalacao import ordenar_intercalacao


def test_lista_pequena():
    assert escolher([5, 3, 1]) == ordenar_insercao


def test_lista_quase_ordenada():
    lista = list(range(100))
    lista[50], lista[51] = lista[51], lista[50]

    assert escolher(lista) == ordenar_insercao


def test_faixa_pequena():
    lista = [i % 10 for i in range(100)]

    assert escolher(lista) == ordenar_contagem


def test_lista_pequena_hibrida():
    lista = list(range(50, 0, -1))

    assert escolher(lista) == ordenar_hibrida


def test_valores_positivos():
    lista = list(range(1000, 0, -1))

    assert escolher(lista) == ordenar_base


def test_faixa_grande_com_negativos():
    lista = [-(i * 10000) for i in range(100)]

    assert escolher(lista) == ordenar_intercalacao


def test_seletor_retorna_funcao():
    metodo = escolher([8, 3, 5, 1])

    assert callable(metodo)
