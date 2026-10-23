
from algoritmos.seletor import escolher, ordenar


def main():
    cenarios = {
        "Lista minuscula": [5, 2, 8, 1, 3],
        "Lista quase ordenada": list(range(100)),
        "Faixa estreita": [i % 10 for i in range(100)],
        "Lista invertida": list(range(100, 0, -1)),
        "Numeros negativos": [-50, 20, -10, 0, 5],
        "Valores grandes": [1000000, 500000, 2000000, 300000]
    }

    for nome, lista in cenarios.items():
        metodo = escolher(lista)
        resultado = ordenar(lista)

        print(f"\nCenario: {nome}")
        print(f"Quantidade: {len(lista)}")
        print(f"Metodo escolhido: {metodo.__name__}")
        print(f"Resultado: {resultado}")


if __name__ == "__main__":
    main()
