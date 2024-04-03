# Projeto - Extração de Dados I

## Sistema de Monitoramento de Avanços no Campo da Genômica

### Contexto:

O grupo trabalha no time de engenharia de dados na HealthGen, uma empresa especializada em genômica e pesquisa de medicina personalizada. A genômica é o estudo do conjunto completo de genes de um organismo, desempenha um papel fundamental na medicina personalizada e na pesquisa biomédica. Permite a análise do DNA para identificar variantes genéticas e mutações associadas a doenças e facilita a personalização de tratamentos com base nas características genéticas individuais dos pacientes.

A empresa precisa se manter atualizada sobre os avanços mais recentes na genômica, identificar oportunidades para pesquisa e desenvolvimento de tratamentos personalizados e acompanhar as tendências em genômica que podem influenciar estratégias de pesquisa e desenvolvimento. Pensando nisso, o time de dados apresentou uma proposta de desenvolvimento de um sistema que coleta, analisa e apresenta as últimas notícias relacionadas à genômica e à medicina personalizada, e também estuda o avanço do campo nos últimos anos.

O time de engenharia de dados tem como objetivo desenvolver e garantir um pipeline de dados confiável e estável. As principais atividades são:

1. **Consumo de dados com a News API**:

   - Implementar um mecanismo para consumir dados de notícias de fontes confiáveis e especializadas em genômica e medicina personalizada, a partir da News API:
     [https://newsapi.org/](https://newsapi.org/)

2. **Definir Critérios de Relevância**:

   - Desenvolver critérios precisos de relevância para filtrar as notícias. Por exemplo, o time pode se concentrar em notícias que mencionem avanços em sequenciamento de DNA, terapias genéticas personalizadas ou descobertas relacionadas a doenças genéticas específicas. Escolher 3 palavras-chave como critério de relevância.

3. **Cargas em Batches**:

   - Armazenar as notícias relevantes em um formato estruturado e facilmente acessível para consultas e análises posteriores. Essa carga deve acontecer 1 vez por hora. Se as notícias extraídas já tiverem sido armazenadas na carga anterior, o processo deve ignorar e não armazenar as notícias novamente, os dados carregados não podem ficar duplicados.

4. **Dados transformados para consulta do público final**:

   - A partir dos dados carregados, aplicar as seguintes transformações e armazenar o resultado para a consulta do público final:

     - 4.1 - Quantidade de notícias por ano, mês e dia de publicação;

     - 4.2 - Quantidade de notícias por fonte e autor;

     - 4.3 - Quantidade de aparições das 3 palavras-chave por ano, mês e dia de publicação definidas no item 2

   - Atualizar esses dados transformados 1 vez por dia.

5. **Classificação da relevância do artigo** (opcional):

    - Um dos principais problemas dos pesquisadores da HealthGen é saber quais artigos publicados são os mais relevantes e deveriam ser lidos primeiro. Pensando nisso, os cientistas de dados criaram um modelo de ML para que retorna um score de 1 a 10 indicando o quão prioritário é aquele artigo, sendo os que recebem o valor 1 os mais importantes. Esse modelo irá ficar alocado na API e deve retornar o score previsto.

6. **API para consulta do público final**:

    - Além das atividades principais, existe a necessidade de disponibilizar essas informações. Para isso crie uma API que contém as seguintes funções:

        - retornar todas as notícias
        - retornar notícia por id
        - receber outras notícias que não foram mapeadas pela API original
        - retornar a quantidade de notícias por ano, mês e dia de publicação do item 4.1
        - retornar a quantidade de notícias por fonte e autor do item 4.2
        - retornar a quantidade de aparições das 3 palavras-chave por ano, mês e dia de publicação  do item 4.3
        - receber e calcular a relevância de um artigo. Considere o modelo de ML como uma função random que retorna os valores esperados (opcional).
        - retornar notícias por score de relevância (opcional)
        - retornar notícias por data de publicação (opcional)


7. **Outros Incrementos Opcionais**
   
   - Salvar e resgatar as informações em um banco de dados à sua escolha 
   - Adição de autenticação básica no webhook [exemplo 1](https://peter-nhan.github.io/posts/Webhook-Python-Curl-DNAC/) [exemplo 2](https://dev.to/koladev/building-a-web-service-whatsapp-cloud-api-flask-webhook-configuration-part-2-l1k)
   - Deploy do webhook utilizando qualquer ferramenta. Algumas sugestões: ngrok, [Render](https://render.com/), Heroku

