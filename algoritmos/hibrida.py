
def ordenar_hibrida(v):
    if len(v) <= 1:
        return v.copy()

    def insercao(lista):
        for i in range(1, len(lista)):
            atual = lista[i]
            j = i - 1

            while j >= 0 and lista[j] > atual:
                lista[j + 1] = lista[j]
                j -= 1

            lista[j + 1] = atual

        return lista

    def merge_sort(lista):
        if len(lista) <= 16:
            return insercao(lista.copy())

        meio = len(lista) // 2
        esquerda = merge_sort(lista[:meio])
        direita = merge_sort(lista[meio:])

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

    return merge_sort(v)
