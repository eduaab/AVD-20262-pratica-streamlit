# Registro Curado de Prompts e Interações com IA (Google Antigravity)

**Disciplina:** Análise e Visualização de Dados (AVD 2026.2) – CESAR School  
**Aluno:** Eduardo  
**Ferramenta:** Google Antigravity (Gemini 3.8 Flash / Claude Sonnet 4.6)  
**Escopo deste registro:** Conforme as diretrizes da Seção 5 da Declaração de Uso de IA, este arquivo contém exclusivamente as consultas e prompts técnicos que agregaram conteúdo real ao projeto (código, layout, visuais e performance). Conversas operacionais de ambiente, instalação de pacotes e dúvidas básicas de terminal foram omitidas.

---

## 📌 Sessão 1: Esqueleto Estrutural do `app.py` a partir do Rascunho de Layout (Aula 21)

### 👤 Aluno (Prompt Estruturado — Template de Prompt)
> **Contexto:** Sou aluno de AVD na CESAR School e estou criando uma aplicação Streamlit para analisar um dataset de 500 estudantes universitários que utilizam uma plataforma digital de aprendizado de inglês (`data/clean/dataset.csv`).  
> **Entrada:** Desenhei o rascunho do layout do primeiro dashboard em `entregas/rascunho-dashboard1.png`. Ele prevê uma barra lateral fixa à esquerda com seletores e uma área principal com abas (`st.tabs`).  
> **Restrições:** Use a biblioteca oficial do Streamlit e a Skill do Streamlit (`streamlit skills`). Separe a leitura de dados em `src/data_loader.py` com `@st.cache_data`. Gere apenas o esqueleto estrutural limpo, com placeholders nos visuais e filtros na barra lateral (multiselect de variáveis quantitativas e slider de intervalo para `Time_Spent_Platform`).  
> **Formato de saída:** Arquivo único `app.py` executável na raiz do projeto.

### 🤖 Assistente (Apoio com a Skill do Streamlit)
* Forneceu a estrutura inicial do `app.py` utilizando `st.set_page_config(layout="wide")`.
* Criou a barra lateral com `with st.sidebar:`, adicionando o `st.multiselect` para seleção das colunas quantitativas e o `st.slider` para filtrar o tempo na plataforma.
* Implementou a divisão da aplicação em abas através de `tab_kpis, tab_lab = st.tabs(...)`.
* Configurou placeholders (`st.empty` / `st.markdown`) para receber as métricas e os gráficos nas aulas seguintes.

---

## 📌 Sessão 2: Dashboard 1 — Heatmap de Correlação e Distribuição Univariada (Aula 21)

### 👤 Aluno
> No **Dashboard 1 (Laboratório de Análise)**, preciso que a área principal mostre:
> 1. Um mapa de calor de correlação de Spearman entre as variáveis selecionadas na barra lateral, em formato triangular (para não duplicar pares).
> 2. Uma grade de histogramas com a distribuição de cada variável selecionada.
> 3. Tudo precisa atualizar dinamicamente quando eu mudar as variáveis ou o slider de tempo na sidebar, além de mostrar alertas amigáveis caso o usuário selecione menos de 2 variáveis.
> Como monto essa sintaxe no Altair dentro do Streamlit?

### 🤖 Assistente (Sintaxe de Visualização com Altair)
* Auxiliou com o cálculo da correlação via Pandas (`df_filtrado[variaveis].corr(method="spearman")`) e filtragem da matriz triangular inferior.
* Estruturou o mapa de calor no Altair com `alt.Chart(corr).mark_rect()`, aplicando a escala divergente `purpleorange` e rótulos numéricos com `mark_text`.
* Construiu o loop em grade de duas colunas (`st.columns(2)`) gerando histogramas binned via `alt.Chart(...).mark_bar().encode(x=alt.X(..., bin=alt.Bin(maxbins=20)))`.
* Implementou as validações `if len(variaveis) < 2: st.warning(...)` para tratar casos de borda.

---

## 📌 Sessão 3: Dashboard 2 — Definição e Implementação dos KPIs de Produto (Aula 22)

### 👤 Aluno (Decisão Autônoma de Negócio)
> Para o **Dashboard 2**, decidi que o público-alvo será a **Equipe de Produto da Plataforma EdTech (PMs, UX e Conteúdo)**.
> Escolhi estas **3 métricas principais**:
> 1. **Ganho Médio Global (`ganho_medio`):** Para medir a eficácia pedagógica da plataforma.
> 2. **Tempo Médio de Uso (`Time_Spent_Platform`):** Para medir o engajamento dos alunos ativos.
> 3. **Taxa de Alta Frequência (`Platform_Usage_Frequency >= 4`):** Para medir o hábito de retenção semanal.
> Como calculo e exibo esses cartões de KPI no Streamlit usando `st.metric` com deltas comparativos?

### 🤖 Assistente (Sintaxe de Métricas)
* Auxiliou na sintaxe do Streamlit para dispor os cartões lado a lado com `col1, col2, col3 = st.columns(3)`.
* Implementou os cartões com `st.metric`:
  * Ganho médio formatado com duas casas decimais e delta em relação à mediana histórica da base.
  * Tempo médio em horas com informação do tamanho da amostra filtrada no delta.
  * Taxa percentual de alta frequência acompanhada da contagem absoluta de alunos com 4 ou mais dias de acesso semanal.

---

## 📌 Sessão 4: Dashboard 2 — Visuais Estratégicos e Cross-Filtering Interativo (Aula 22)

### 👤 Aluno (Escolha e Validação de Gráficos)
> Quero 3 visuais complementares para a equipe de produto:
> 1. Um gráfico de barras horizontais com o **Ganho Médio por Estilo de Aprendizagem** (`Learning_Style`).
> 2. Um **gráfico de dispersão entre Tempo na Plataforma e Ganho Médio**, colorido pela classe de desempenho.
> 3. Uma **interatividade cruzada (cross-filtering)**: ao clicar em uma barra de estilo de aprendizagem no Visual 1, quero que o gráfico de dispersão filtre e destaque apenas os alunos daquele estilo.
> 4. Um gráfico comparativo Pré vs Pós mostrando a evolução média em Vocabulário, Leitura e Fala em barras agrupadas horizontais.
> Como conecto essa seleção cruzada no Altair e monto o comparativo?

### 🤖 Assistente (Sintaxe do Cross-filtering e Layout no Altair)
* Implementou o parâmetro de seleção `clique_estilo = alt.selection_point(name="filtro_estilo", fields=["Learning_Style"])`.
* Vinculou o evento de clique nas barras horizontais ao gráfico de dispersão com `.transform_filter(clique_estilo)`.
* Combinou os dois gráficos lado a lado na mesma linha usando o operador de concatenação do Altair: `st.altair_chart(barras_estilo | dispersao_tempo, width="stretch")`.
* Estruturou o dataframe transformado e as barras horizontais agrupadas com `yOffset="Momento:N"` para o comparativo Pré vs Pós por habilidade.

---

## 📌 Sessão 5: Identidade Visual e Otimização de Performance (Aulas 22 e 23)

### 👤 Aluno
> Minha EDA utilizou tons de roxo e areia/rosa claro. Como passo essa identidade visual para o Streamlit reconhecer nos temas claro e escuro, e como garanto que os dados fiquem cacheados para não recarregar o CSV a cada clique?

### 🤖 Assistente (Configuração e Boas Práticas)
* Configurou o arquivo `.streamlit/config.toml` com `primaryColor = "#8338ec"`, fundos `#ffffff` (claro) e `#0f0c15` (escuro), com padding otimizado.
* Adicionou o decorator `@st.cache_data` na função `load_data()` em `src/data_loader.py`, garantindo tempo de resposta instantâneo ao manipular os filtros.
