
from algoritmos.seletor import ordenar, escolher


def test_lista_vazia():
    assert ordenar([]) == []


def test_um_elemento():
    assert ordenar([5]) == [5]


def test_elementos_iguais():
    assert ordenar([7, 7, 7, 7]) == [7, 7, 7, 7]


def test_lista_ordenada():
    assert ordenar([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]


def test_lista_invertida():
    assert ordenar([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


def test_valores_negativos():
    assert ordenar([-5, 3, -1, 0, 2]) == [-5, -1, 0, 2, 3]


def test_lista_original_preservada():
    lista = [5, -2, 8, 1, 0]
    original = lista.copy()

    ordenar(lista)

    assert lista == original


def test_escolher_retorna_metodo():
    metodo = escolher([5, 3, 1])

    assert callable(metodo)
    assert metodo([5, 3, 1]) == [1, 3, 5]
