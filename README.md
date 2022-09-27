# Projeto ELT (Extract, Load and Transform)

Este repositório possui por objetivo COMPARTILHAR alguns dos principais arquivos de um projeto ELT. Os arquivos aqui compartilhados pertencem a dois projetos distintos, pois o objetivo é mostrar o trabalho que pode ser realizado com as tecnologias selecionadas.

Embora os arquivos pertençam a dois projetos distintos, ambos utilizam dados do [Inside Airbnbn](http://insideairbnb.com/get-the-data/) e, basicamente, possuem a mesma essência:

1. Fazer o *extract* dos dados do [Inside Airbnbn](http://insideairbnb.com/get-the-data/) e fazer o *load* para um bucket aws s3.
2. Fazer o *transform* dos dados utilizando DBT conectado ao Snowflake.

## :open_book: Índice

* [Tecnologias utilizadas](#hammer-tecnologias-utilizadas)
* [Sobre o Projeto](#speech_balloon-sobre-o-projeto)
* [Planejamento](#memo-planejamento)
* [Licença](#ramen-licença)

## :hammer: Tecnologias utilizadas
As tecnologias utilizadas neste projeto:
1. Python
2. Apache-Airflow
3. Docker
4. AWS S3
5. Snowflake
6. DBT (Data Build Tool)

## :speech_balloon: Sobre o Projeto
Alguns projetos que já fiz com as tecnologias acima e com os dados disponíveis no [Inside Airbnbn](http://insideairbnb.com/get-the-data/) possuíam como objetivo:

1. Fornecer um banco de dados pronto para utilização por um grupo de engenheiros de machine learning que criaram um modelo capaz de retornar um valor (R$) de alguel/dia a partir de entradas como "área", "localização", "número de camas" e comodidades" de um imóvel hipotético.
2. Fornecer um banco de dados pronto para utilização por um grupo de engenheiros de machine learning que criaram um modelo de classificação dos comentários/avaliações dos clientes, buscando classificar os comentários como: POSITIVO, NEGATIVO ou NEUTRO.

## :memo: Planejamento
O projeto, de forma resumida, contará com as seguintes etapas (etapas já disponíveis encontram-se marcadas):

- [X] Dag para extrair dados do Inside Airbnb.
- [X] Construção de relatórios automatizados a respeito dos dados raspados do Inside Airbnb.
- [X] Dag para tratamento de dados. *Observação: Infelizmente esta etapa foi necessária (anterior aos tratamentos feitos com DBT por SQL), pois uma das colunas é a "avaliação do usuário que ficou na acomodação do airbnb". Assim, este campo é um texto aberto, contendo quebras de linhas, tags html e tudo mais que um usuário pode digitar "de forma aberta" em um campo aberto. Somente consegui colocar o .csv relativo a estas informações no SNOWFLAKE quando fiz esta etapa de tratamento utilizando regex e python.*
- [X] Dag para realizar o upload dos dados para AWS S3.
- [X] Conexão do DBT com Snowflake.
- [X] Comprtilhar o 'DBT models'.
- [X] Comprtilhar o 'DBT snapshots'.
- [X] Comprtilhar o 'DBT macros'.
- [X] Comprtilhar o 'DBT tests'.
- [X] Comprtilhar o 'DBT assets'.
- [X] Datasets prontos para utilização pela próxima equipe.

## :ramen: Licença

Este projeto está sob "Unlicense license". Para maiores detalhes sobre a licença utilizada, click [aqui](https://github.com/devmadruga/elt_projeto/blob/main/LICENSE). 
