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
    - Desenvolver critérios precisos de relevância para filtrar as notícias. Por exemplo, o time pode se concentrar em notícias que mencionem avanços em sequenciamento de DNA, terapias genéticas personalizadas ou descobertas relacionadas a doenças genéticas específicas.

3. **Cargas em Batches**:
    - Armazenar as notícias relevantes em um formato estruturado e facilmente acessível para consultas e análises posteriores. Essa carga deve acontecer 1 vez por hora. Se as notícias extraídas já tiverem sido armazenadas na carga anterior, o processo deve ignorar e não armazenar as notícias novamente, os dados carregados não podem ficar duplicados.

4. **Dados transformados para consulta do público final**:
    - A partir dos dados carregados, aplicar as seguintes transformações e armazenar o resultado final para a consulta do público final:

        - 4.1 - Quantidade de notícias por ano, mês e dia de publicação;
    
        - 4.2 - Quantidade de notícias por fonte e autor;
    
        - 4.3 - Quantidade de aparições de 3 palavras-chave por ano, mês e dia de publicação (as 3 palavras-chave serão as mesmas usadas para fazer os filtros de relevância do item 2 (2. Definir Critérios de Relevância)).
    
    - Atualizar os dados transformados 1 vez por dia.

# Atenção: a parte final do projeto ainda será definida, mas já é possível começar o ETL dos dados
Possivelmente a parte final envolverá a criação de uma API com um POST para receber um alerta quando tiver notícia nova OU um GET que fornecerá as notícias coletadas por vocês.