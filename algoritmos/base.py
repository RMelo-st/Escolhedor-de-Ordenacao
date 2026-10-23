def ordenar_base(v):
    if len (v) <= 1:
        return v.copy()
    negativos = [-x for x in v if x < 0]
    positivos = [x for x in v if x >= 0]
    
    def radix_sort(lista):
        if not lista:
            return lista
        maior = max(lista)
        exp = 1 

        while maior // exp > 0:
            saida = [0] * len(lista)
            contagem = [0] * 10

            for numero in lista:
                digito = (numero // exp) % 10
                contagem[0] * 10

            for numero in lista:
                digito = (numero // exp) % 10
                contagem[digito] += 1

            for i in range(1, 10):
                contagem[i] += contagem [i -1]

            for numero in reversed(lista):
                digito = (numero // exp) % 10
                contagem [digito] -= 1
                saida[contagem[digito]] = numero
            lista = saida
            exp = exp * 10
        return lista
    
    negativos = radix_sort(negativos)
    positivos = radix_sort(positivos)

    negativos = [-x for x in reversed(negativos)]
    
    return negativos + positivos

