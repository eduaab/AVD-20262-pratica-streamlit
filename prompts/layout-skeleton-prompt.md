# Template: rascunho de layout → esqueleto do app

Prompt utilizado para a geração do esqueleto inicial da aplicação na Aula 21.

## Contexto
Sou estudante da CESAR School na disciplina Análise e Visualização de Dados (AVD 2026.2).
Estou desenvolvendo uma aplicação Streamlit para analisar o desempenho de 500 estudantes universitários que utilizam uma plataforma digital de aprendizado de língua inglesa (dataset Kaggle: College English Learning). O repositório segue a estrutura padrão com as pastas `data/`, `notebooks/`, `src/`, `entregas/` e `prompts/`.

## Entrada
- Rascunho visual do layout: imagem em `entregas/rascunho-dashboard1.png`.
- Dataset: `data/clean/dataset.csv` contendo colunas como `Prior_English_Proficiency`, `Time_Spent_Platform`, `Vocabulary_Pre`, `Vocabulary_Post`, `Vocabulary_Improvement`, `Reading_Improvement`, `Speaking_Improvement`, `ganho_medio`, `desempenho`, etc.
- Descrição do layout pretendido: Barra lateral (sidebar) com multiselect de variáveis quantitativas e filtro de intervalo numérico (slider) para tempo de uso na plataforma. Área principal organizada com abas (`st.tabs`), contendo o painel executivo de KPIs e o Laboratório de Análise (correlação e histogramas de distribuição).

## Restrições
- Utilizar a biblioteca Streamlit oficial e seguir as boas práticas da Skill do Streamlit.
- O carregamento de dados deve ser modularizado via `src/data_loader.py` utilizando cache `@st.cache_data`.
- Manter marcações de apoio no código: `# [IA] <ferramenta> – <finalidade>`.
- Gerar o esqueleto estrutural com containers e placeholders organizados, pronto para receber os visuais.

## Formato de saída
- Código limpo em arquivo único `app.py` na raiz do projeto, pronto para execução via `streamlit run app.py`.
