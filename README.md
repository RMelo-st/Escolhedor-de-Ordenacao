# Escolhedor de Ordenação — Projeto G2

Projeto acadêmico para comparar seis algoritmos de ordenação e implementar um seletor que escolhe um método com base nas características da lista.

## Objetivo

O projeto reúne os métodos estudados no semestre e implementa:

- `escolher(v)`: analisa a entrada e retorna uma função de ordenação.
- `ordenar(v)`: chama o seletor e executa o método escolhido.
- Benchmarks com quatro cenários.
- Testes automatizados para entradas especiais.
- Gráficos gerados a partir dos resultados medidos.

## Algoritmos

| Método | Descrição resumida |
|---|---|
| Inserção | Insere cada elemento na posição correta; funciona bem em listas pequenas ou quase ordenadas. |
| Intercalação | Merge Sort; divide a lista e intercala as partes ordenadas. |
| Rápida | Quick Sort com pivô aleatório. |
| Híbrida | Combina Merge Sort com Inserção para sublistas pequenas. |
| Contagem | Counting Sort; é eficiente quando a faixa de valores é pequena. |
| Radix Sort | Ordena números inteiros por dígitos, tratando valores negativos na implementação do projeto. |
| Escolhedor | Usa regras simples para escolher um dos seis métodos. |

## Estrutura do projeto

```text
Escolhedor-de-Ordenacao/
├── algoritmos/
├── benchmarks/
│   ├── executar_benchmarks.py
│   └── gerar_graficos.py
├── interface/
│   └── gui.py
├── resultados/
│   ├── resultados.csv
│   └── graficos/
│       ├── 01_desempenho_geral.png
│       ├── 02_custo_total_seletor.png
│       ├── 03_qualidade_escolha.png
│       └── 04_comparacao_linear.png
├── tests/
├── main.py
├── README.md
└── RELATORIO.md
```

## Requisitos

Python 3.12 ou compatível. Instale as dependências usadas pelos testes e pelos gráficos:

```powershell
python -m pip install pytest matplotlib
```

A interface usa Tkinter, que normalmente acompanha a instalação do Python para Windows.

## Como executar

### Abrir a interface gráfica

```powershell
python main.py
```

Na interface, é possível executar o seletor, comparar os seis algoritmos, executar os testes, rodar o benchmark oficial e gerar os gráficos.

### Executar os testes automatizados

```powershell
python -m pytest tests/ -v
```

Na execução registrada durante o desenvolvimento, os 18 testes passaram. Execute novamente para validar o estado atual do código.

### Refazer as medições

```powershell
python benchmarks/executar_benchmarks.py
```

O benchmark usa sete repetições e grava a mediana dos tempos em `resultados/resultados.csv`. O CSV é sobrescrito a cada execução. Os resultados podem variar conforme o computador, a versão do Python e a carga do sistema.

### Gerar os gráficos

Depois de atualizar o CSV, execute:

```powershell
python benchmarks/gerar_graficos.py
```

Os quatro PNGs são gravados em `resultados/graficos/`. Os gráficos abaixo usam os nomes de arquivo relativos para que apareçam no GitHub depois que as imagens forem adicionadas ao repositório.

## Resultados do benchmark registrado

Tempos medianos em milissegundos. Estes números são os dados registrados no CSV fornecido para esta versão do relatório.

| Cenário | Inserção | Intercalação | Rápida | Híbrida | Contagem | Radix Sort | Escolhedor |
|---|---:|---:|---:|---:|---:|---:|---:|
| Aleatório com chaves grandes | 114,9113 | 7,0176 | 5,2568 | **4,7237** | Inadequado | 7,4645 | 8,2803 |
| Faixa restrita | 118,1753 | 6,6314 | 1,9007 | 4,9567 | **0,2496** | 1,5284 | 0,8400 |
| Quase ordenado | 2,2145 | 6,2027 | 4,9839 | 3,3852 | **0,7238** | 3,3546 | 2,7802 |
| Lista pequena | **0,0034** | 0,0122 | 0,0102 | 0,0041 | 0,0048 | 0,0072 | 0,0037 |

O Counting Sort foi marcado como inadequado no cenário de chaves grandes porque a faixa de valores é excessiva para a implementação utilizada.

## Gráficos

### 1. Visão geral do desempenho

Compara os métodos em cada cenário. Este gráfico usa escala logarítmica para tornar visíveis tempos que diferem bastante entre si.

![Visão geral do desempenho dos algoritmos](resultados/graficos/01_desempenho_geral.png)

### 2. Custo total do seletor

Compara o tempo total do Escolhedor com o melhor algoritmo fixo medido em cada cenário.

![Custo total do seletor versus melhor algoritmo fixo](resultados/graficos/02_custo_total_seletor.png)

### 3. Qualidade da decisão

Compara o tempo do algoritmo que o seletor escolheu com o melhor algoritmo fixo. Esta comparação avalia a qualidade da escolha; não representa o tempo total do Escolhedor.

![Qualidade da decisão do seletor](resultados/graficos/03_qualidade_escolha.png)

### 4. Comparação em escala linear

Mostra os tempos com escala linear e eixo vertical próprio por cenário. Isso evita que os tempos pequenos desapareçam quando comparados com cenários de centenas de milissegundos.

![Comparação detalhada em escala linear](resultados/graficos/04_comparacao_linear.png)

## Observações

- O seletor é determinístico para uma mesma lista, porque suas regras dependem de características da entrada.
- O método escolhido não precisa ser o mais rápido em todos os conjuntos de dados.
- A análise da lista também custa tempo. Por isso, o desempenho total deve ser comparado com os algoritmos fixos.
- Os tempos são experimentais, não garantias universais de desempenho.
- O relatório detalhado, com as regras do seletor e a interpretação dos resultados, está em [`RELATORIO.md`](RELATORIO.md).
