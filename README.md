# GraphQL

De acordo com https://graphql.org/ **GraphQL** é uma linguagem de consulta para APIs e também uma ferramenta runtime 
para atender a requisições. 

O **GraphQL** pode ser entendido como uma linguagem baseada na teoria de grafos(Graph) com capacidade de consultar e 
manipulação de dados estruturados (QL - SEQUEL - Structured English Query Languange). **GraphQL** define um padrão de como as consultas devem ser criadas e como os dados devem ser retornados, um padrão de 
permite portabilidade para qualquer linguagem ou ambiente.

O principal principal objetivo do **GraphQL** é resolver um problema comum no desenvolvimento de serviços/APIs, onde é 
um endpoint é construido para entregar um determinado conjunto de dados e é usado para a função que foi destinado.
Com a adição de mais funcionalidades o mesmo endpoint é utilizado para outra função, mas desta vez ele retorna mais 
dados do que o necessário (*overfetching*) ou menos informações que o necessário (*underfetching*). O que fazer então, pode-se:

1. Criar um novo endpoint que supre esta necessidade, gerando mais um endpoint;
1. Alterar o endpoint, passando parâmetros para definir o tipo de retorno;

A solução 1 gera difersos enpoints subutilizados e pode gerar condições de conflito de dados, aumentando tempo de teste,
desenvolvimento, manutenção e aumentando a possibilidade de bugs e códigos duplicados. A solução 2 gera um diversidade
de endpoints de múltiplos propósitos, cada um com seus próprios padrões de parâmetros e modificadores, muitas vezes 
sem documentação suficientes e acabam caindo em desuso, pois é mais fácil implementar um novo endpoint que alterar
a passsagem de parâmetros de um endpoint em questão (principalmente para um novo membro da equipe).

Com o **GraphQL** o endpoint permite retornar os parâmetros especificados, com um padrão de linguagem bem definido e 
de fácil modificação para um desenvolver que conhece o padrão. O **GraphQL** não tras nenhuma tecnologia ou metodologia 
revolucionária, o mesmo basea-se em tecnologias existentes para buscar a padronização da comunicação de dados entre 
serviços/APIs.

Além do padrão especificado pelo **GraphQL** o mesmo tras consigo a premissa de documentação dentro do código, podendo 
ser fácilmente acessada junto a API, bem como, um console de consultas para testes da consulta (como é possível fazer 
em um banco de dados, utilizando-se uma ferramenta externa, MySQL Workbench ou PgAdmin).


## Princípios do GraphQL

* Hirárquico

Uma consulta em **GraphQL** é hierárquica, campos são alinhados em outros campos e a consulta é formada do mesmo modo 
como os dados serão devolvidos.

* Centrado em produtos

O **GraphQL** é orientado de acordo com as necessidades de dados do cliente, além da linguagem e do runtime que dão 
suporte ao cliente.

* Tipagem forte

Um servidor **GraphQL** tem o sistema de tipos do GraphQL como base. No esquema, cada dado tem um tipo específico em 
relação ao qual será validado.

* Consultas especificadas pelo cliente

Um servidor **GraphQL** oferece os recursos que o cliente têm permissão para consumir.

* Introspectivo

A linguagem **GraphQL** é capaz de fazer consultas ao sistema de tipos do servidor **GraphQL**.

## Histórico

Desenvolvida em 2012 dentro do Facebook, por Lee Byron, Nick Schrock e Dan Shafer, os quais decidiram repensar nos dados
do lado do cliente, uma vez que os aplicativos da empresa apresentavam problemas de desempenho e com frequência apresentavam
falhas. Eles decidiram implementar o **GraphQL**, uma linguagem de consulta que descrevia os recursos e os requisitos dos modelos
de dados para as aplicações cliente/servidor da empresa.

A primeira especificação inicial do **GraphQL** foi lançada em julho de 2015, além de uma implementação de referência em Javascript,
chamada graphql.js.

Em setembro de 2016 deixou sua etapa de "versão preliminar", estando pronta para o ambiente de produção. Empresas que usam 
em menor ou maior grau:

* Airbnb
* Coursera
* Facebook
* Github
* IBM
* Paypal
* Pinterest
* Starbucks
* The New York Times
* Twitter

Entre outros (vide https://landscape.graphql.org/category=graph-ql-adopter&format=card-mode&grouping=category).


## O GraphQL

### GraphQL vs SQL

O GraphQL usa as ideias que foram originalmente desenvolvidas para consultar banco de dados, uma consulta GraphQL pode 
devolver dados conectados, e assim como o SQL pode inserir, atualizar e remover dados. Apesar de serem ambas linguagens
para consulta, o GraphQL e SQL são completamentes diferentes, voltadas para ambientes totalmente distintos. No SQL, as
consultas são enviadas para um banco de dados, enquanto no GraphQL as consultas vão para uma API, podendo ser armazenada
em qualquer lugar.

As sintaxes de SQL e GraphQL são também diferentes, tem-se assim:

| SQL |  GraphQL |
|:------:|:-------:|
| SELECT | query |
| Insert - Update - Delete | mutation |
| - | subscription (websocket)|

### Consulta no GraphQL

As consultas são strings simples, enviadas no corpo de requisições POST para um endpoint GraphQL:

```
{
   allEmployes {
      name
   }
}
```

O Resultado desta consulta será um JSON com os dados solicitados dentro de um campo chamado *data* ou um campo *errors* 
se algo der errado. O GraphiQL é o IDE criado pelo Facebook para permitir consultar e explorar uma API GraphQL, você pode
testar em http://snowtooth.moonhighway.com/, onde a consulta:

```
query {
  allLifts{
    name
    status
  }
}
```

retornará o seguinte JSON:

```JSON
{
  "data": {
    "allLifts": [
      {
        "name": "Astra Express",
        "status": "HOLD"
      },
      {
        "name": "Jazz Cat",
        "status": "HOLD"
      }
  } 
}
```

### Conceitos do GraphQL

A query é um tipo em GraphQL, chamada de nó raiz ou tipo raiz. Isso porque é um tipo mapeado para uma operação e as
operações representam as raízes do documento de consulta.

Quando escrevemos consultas, selecionamos os campos necessários colocando-os entre chaves, estes blocos são chamados de 
conjuntos de seleção. Os dados recebidos informado dentro do conjunto de seleção. É possível também alterar o nome dos
campos no objeto, desta forma:

```
query {
  open : liftcount(status : OPEN)
  allLifts{
    liftName : name
  }
  allTrails{
    difficulty
    night
  }
}
```

Os campos que definimos em um conjunto de seleção estão diretamente relacionados aos tipos do GraphQL, assim como *allFilms*
são tipos definidos dentro da Query. 

O GraphQL permite alinhamentos, como pode ser visualizado no exemplo acima. Isso permite retornar diversos dados não
relacionados em uma única consulta. Outra caracteristica do GraphQL é a possibilidade de filtrar o resultado, passando
argumentos na consulta.

Semelhantes a outras linguagens o  GraphQL permite uso de escalares, sendo cinco as primitivas básicas, inteiros (Int),
números de ponto flutuante (Float), strings (String), Booleanos (Boolean) e identificaores únicos (ID). IDs são representados
por strings, com a garantia do GraphQL que IDs são strings únicas.

#### Fragmentos

Os fragmentos são conjuntos de seleção que podem ser reutilizados em várias operações, por exemplo:

```
fragment nameID on Lift{
  name
  id
}

query liftsAndTrails{
  allLifts (status: CLOSED){
    status
    ...nameID
  }
}
```

#### União

O tipo união permite fazer associação entre dois tipos diferentes de objetos.

#### Interfaces

As interfaces permitam que vários tipos de objetos possam ser devolvidos por um único campo.


## Repensando a aplicação através de esquemas

Para converter suas APIs Rest para GraphQL é necessário repensar seu design, ao invés de um conjunto de endpoints, é 
necessário vê-las como coleção de tipos. Portanto é necessário pensar, discutir e definir formalmente os tipos de dados 
que deseja expotar. Esse conjunto de tipos é chamado de esquema (*schema*).

*Scheme First* é a metodologia de design que fará com que a equipe esteja igualmente ciente dos tipos de dados que compõem 
a aplicação.


## Esquema de execução

```
  _________         _________        _________         _________        _________         _________   
 /         \       /         \      /         \       /         \      /         \       /         \       
|  Nginx    | --> |   UWSGI   | -->|   Flask   | --> |  GraphQL  | -->| SQLAlchemy| --> |   MySQL   |
 \_________/       \_________/      \_________/       \_________/      \_________/       \_________/ 
```


## Instalação

### Referência de instalação

Um tutorial básico de GraphQL/SQLAlchemy/Flask pode ser encontrado aqui: https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/

### Dependências

Para suporte ao banco de dados, é necessário instalar:

* mysqlclient (cliente padrão do mysql)
* pymysql (wrapper de cliente mysql para o python)
* sqlalchemy (toolkit SQL para python - similar ao DAL)

Para suporte ao GraphQL é necessário instalar:

* graphene (mapeamento do banco de dados relacional em modelo de grafo hierarquico)
* graphene_sqlalchemy (wrapper graphene para o sqlalchemy)

Para suporte a aplicação web:

* flask  (mirco web framework para python)
* flask-graphql (extensão flask para GraphQL)

Para suporte ao deploy na internet:

* uwsgi (web server gateway interface, conexão entre o flask e o web server)
* nginx (web server / servidor de proxy reverso)



### Base de dados

A base de dados utilizada está disponível em: https://dev.mysql.com/doc/employee/en/employees-preface.html. O download 
pode ser feito diretamente de https://github.com/datacharmer/test_db.







