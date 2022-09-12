# Projeto ELT (Extract, Load and Transform)

Este repositório possui por objetivo compartilhar alguns dos principais arquivos de um projeto ELT realizado com finalidade de estudos.


## :open_book: Índice

* [Tecnologias utilizadas](#hammer-tecnologias-utilizadas)
* [Sobre o Projeto](#speech_balloon-sobre-o-projeto)
* [Planejamento](#memo-planejamento)
* [Licença](#ramen-licença)


## :hammer: Tecnologias utilizadas
As tecnologias utilizadas neste projeto:
1. Python
2. Apache-Airflow
3. AWS S3
4. Snowflake
5. DBT (Data Build Tool)

## :speech_balloon: Sobre o Projeto
O projeto consiste em disponibilizar, a partir de um dataset do [Inside Airbnbn](http://insideairbnb.com/get-the-data/), dados tratados para dois times de engenheiros de machine learning. O objetivo de cada time de machine learning:

**Time 1**

> Deseja criar um modelo de machine learning que seja capaz de retornar um valor (R$) de alguel/dia a partir de entradas como "área", "localização", "número de camas" e comodidades" de um imóvel hipotético.

**Time 2**

> Deseja criar um modelo de classificação dos comentários/avaliações dos clientes, buscando identificar comentários como: POSITIVO, NEGATIVO ou NEUTRO.


##### Observação: Em um primeiro momento, a implementação dos modelos de machine learning não fazem parte do escopo deste projeto.


## :memo: Planejamento
O projeto, de forma resumida, contará com as seguintes etapas (etapas já disponíveis encontram-se marcadas):

- [X] Dag para extrair dados do Inside Airbnb.
- [X] Dag para realizar o upload dos dados para AWS S3.
- [ ] Com o DBT, carregar os dados da AWS S3 para o Snowflake.
- [ ] Com o DBT, realizar as transformações necessárias nos dados.
- [ ] Datasets prontos para uso pelos times de machine learning.


## :ramen: Licença

Este projeto está sob "Unlicense license". Para maiores detalhes sobre a licença utilizada, click [aqui](https://github.com/devmadruga/elt_projeto/blob/main/LICENSE). 
