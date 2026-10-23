
import random


def ordenar_rapida(v):
    if len(v) <= 1:
        return v.copy()

    pivo = random.choice(v)

    menores = [x for x in v if x < pivo]
    iguais = [x for x in v if x == pivo]
    maiores = [x for x in v if x > pivo]

    return (
        ordenar_rapida(menores)
        + iguais
        + ordenar_rapida(maiores)
    )
