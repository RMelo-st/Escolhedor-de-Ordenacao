
def ordenar_contagem(v):
    if len(v) <= 1:
        return v.copy()

    menor = min(v)
    maior = max(v)
    faixa = maior - menor + 1

    if faixa > max(100_000, len(v) * 10):
        raise ValueError("Faixa de valores muito grande")

    contagem = [0] * faixa

    for numero in v:
        contagem[numero - menor] += 1

    resultado = []

    for i, quantidade in enumerate(contagem):
        resultado.extend([i + menor] * quantidade)

    return resultado
