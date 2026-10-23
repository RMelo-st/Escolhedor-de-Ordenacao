
def ordenar_intercalacao(v):
    if len(v) <= 1:
        return v.copy()

    meio = len(v) // 2

    esquerda = ordenar_intercalacao(v[:meio])
    direita = ordenar_intercalacao(v[meio:])

    resultado = []
    i = 0
    j = 0

    while i < len(esquerda) and j < len(direita):
        if esquerda[i] <= direita[j]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])

    return resultado
