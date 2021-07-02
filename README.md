# fii-list-by-primo-rico
Este software gera um `.csv` com uma lista de FII, que seriam boas opções de investimento, baseados nos critérios estabelecidos pelo YouTuber Primo Rico.

## VIDEO
O vídeo [COMO GANHAR R$1.500 TODOS OS MESES SEM PRECISAR TRABALHAR! | VIVER DE RENDA PASSIVA](https://www.youtube.com/watch?v=IazEN13o304) trata sobre traçar metas para investir corretamente de forma que no futuro o objetivo seja uma boa renda passiva.

Durante o vídeo são traçadas diversas estratégias levando em consideração o valor que o investidor pode poupar, os juros e índices econômicos que impactam no objetivo final e quando ele será atingido.

Ao final o YouTuber mostra como filtrar bons Fundos Imobiliários (FII) baseados em alguns critérios que ajudam escolher bons papéis.

### Quais são os critérios?
* Dividend Yield >= 4%
* P/VP entre 0,4 e 1,2
* Valor de Mercado >= 500.000.000
* Vacância <= 30%
* Liquidez >= 1.000.000/DIA

## Etapas

1. [X] Efetuar web scraping na página da [Fundamentus](https://fundamentus.com.br/) para obter os Fundos Imobiliários negociados na bolsa brasileira.
2. [X] Buscar papéis com Dividend Yield maior ou igual 4%.
3. [X] O índice Preço por Valor Patrimonial (P/VP) deve estar entre 0,4 e 1,2.
4. [X] O Valor de Mercado do fundo deve ser maior ou igual que R$ 500.000.000,00.
5. [X] A Vacância, ou seja, porcentagem de imóveis desocupados deve ser menor ou igual a 30%.
6. [X] A Liquidez, ou seja, a quantidade de negociação por dia do papel deve ser maior ou igual a R$ 1.000.000,00.
7. [X] Gerar csv a partir dos dados processados.

## Requerimentos
Python >= 3

## Instalação
Nenhuma instalação é necessária e todo pacote se encontra na biblioteca padrão.

## Utilização
`python3 fii-list.py`
