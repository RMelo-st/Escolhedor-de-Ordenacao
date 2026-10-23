
from algoritmos.insercao import ordenar_insercao
from algoritmos.intercalacao import ordenar_intercalacao
from algoritmos.rapida import ordenar_rapida
from algoritmos.hibrida import ordenar_hibrida
from algoritmos.contagem import ordenar_contagem
from algoritmos.base import ordenar_base


def escolher(v):
    n = len(v)

    if n <= 16:
        return ordenar_insercao

    menor = v[0]
    maior = v[0]
    inversoes = 0

    for i in range(n):
        if v[i] < menor:
            menor = v[i]

        if v[i] > maior:
            maior = v[i]

        if i > 0 and v[i] < v[i - 1]:
            inversoes += 1

    faixa = maior - menor + 1

    if inversoes <= n // 20:
        return ordenar_insercao

    if faixa <= max(1000, n * 5):
        return ordenar_contagem

    if n < 100:
        return ordenar_hibrida

    if faixa > 0 and all(x >= 0 for x in v):
        return ordenar_base

    return ordenar_intercalacao


def ordenar(v):
    metodo = escolher(v)
    return metodo(v)
