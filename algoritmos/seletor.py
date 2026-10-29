
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
    negativos = False

    for i in range(n):
        if v[i] < menor:
            menor = v[i]

        if v[i] > maior:
            maior = v[i]

        if v[i] < 0:
            negativos = True

        if i > 0 and v[i] < v[i - 1]:
            inversoes += 1

    if inversoes <= n // 20:
        return ordenar_insercao

    if n < 100:
        return ordenar_hibrida

    faixa = maior - menor + 1

    if faixa < n:
        return ordenar_contagem

    if not negativos:
        return ordenar_base

    return ordenar_intercalacao


def ordenar(v):
    metodo = escolher(v)
    return metodo(v)
