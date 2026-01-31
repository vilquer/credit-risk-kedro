# German Credit Risk Scorecard with Kedro 🚀

Este é um projeto de caráter técnico e fundamental, desenvolvido com o objetivo central de explorar e demonstrar as capacidades do framework Kedro e a aplicação de princípios de MLOps. O foco aqui não é apenas a performance preditiva, mas a estruturação de um pipeline de dados robusto, modular e persistente.


![kedro viz](https://github.com/vilquer/credit-risk-kedro/blob/0b9ceabdd429911285fb647b92480337defd7170/img/viz.png)

## 📋 Visão Geral do Pipeline

O projeto foi estruturado utilizando o framework **Kedro**, dividindo a lógica em camadas de dados (Data Engineering e Data Science):

1. **Raw**: Dados brutos da UCI Machine Learning Repository.
    
2. **Intermediate**: Limpeza e mapeamento de domínios (conversão de códigos técnicos para labels de negócio).
    
3. **Primary**: Seleção de atributos baseada em **Information Value (IV)**.
    
4. **Model Input**: Preparação numérica via One-Hot Encoding (Dummies).
    
5. **Models**: Treinamento de Random Forest e persistência do modelo (Pickle).
    
6. **Reporting**: Avaliação de performance focada em métricas de risco (**Gini** e **AUC**).

   ![dados](https://github.com/vilquer/credit-risk-kedro/blob/0b9ceabdd429911285fb647b92480337defd7170/img/data.png)

---

## 🛠️ Tecnologias e Metodologias

- **Linguagem:** Python 3.10
    
- **Framework de Pipeline:** [Kedro](https://kedro.org/)
    
- **Estatística de Risco:** Information Value (IV) & Weight of Evidence (WoE)
    
- **Machine Learning:** Scikit-Learn (Random Forest)
    
- **Persistência:** Apache Parquet (eficiência de storage e tipos)
    
- **Gestão:** Princípios de **Data Driven Scrum (DDS)**
    

---

## 📈 Resultados de Performance

O modelo é avaliado automaticamente, gerando um relatório em `data/08_reporting/performance_metric.json`.

|**Métrica**|**Valor Obtido**|
|---|---|
|**AUC**|0.7X|
|**GINI**|0.4X|

> **Nota:** O Gini obtido é condizente com benchmarks de mercado para o dataset German Credit, demonstrando um poder discriminatório sólido entre bons e maus pagadores.

---

## 🚀 Como Executar

1. **Instalar dependências:**
    
    Bash
    
    ```
    pip install -r src/requirements.txt
    ```
    
2. **Executar o pipeline completo:**
    
    Bash
    
    ```
    kedro run
    ```
    
3. **Visualizar o grafo do projeto:**
    
    Bash
    
    ```
    kedro viz
    ```
    

---

## 🧠 Decisões de Arquitetura (Tech Lead Insights)

- **Filtro de IV:** Implementamos uma seleção automática que remove variáveis com IV < 0.02, garantindo que o modelo foque apenas em preditores com poder estatístico.
    
- **Persistência em Parquet:** Escolhido em detrimento do CSV para garantir que os tipos de dados (especialmente após o binning) fossem preservados entre os nós.
    
- **Mapeamento de Negócio:** Priorizamos a legibilidade dos dados na camada `intermediate` para facilitar Sprints de revisão com stakeholders não técnicos.
    

---

## 👨‍💻 Autor

 [<img src="https://avatars.githubusercontent.com/u/52363892?v=4" width=115><br><sub><b>Vilquer de Oliveira</b></sub>](https://github.com/vilquer) 


_Data Scientist | Tech Lead | Especialista em IA e Engenharia de Software_
