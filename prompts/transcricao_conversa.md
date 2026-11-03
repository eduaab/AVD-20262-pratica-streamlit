# Registro de Prompts e Interações Técnicas com IA (Google Antigravity)

**Disciplina:** Análise e Visualização de Dados (AVD 2026.2) – CESAR School  
**Aluno:** Eduardo  
**Ferramentas:** Google Antigravity (Gemini 3.8 Flash) | Streamlit Skills  
**Data:** Novembro de 2026  
**Finalidade:** Documentação técnica das consultas de código, arquitetura de layout e sintaxe de visualização para a aplicação Streamlit, em conformidade com as diretrizes da Seção 5 da Declaração de Uso de IA.

---

## 📌 Interação 1: Início da Atividade e Esqueleto a partir do Layout (Aula 21)

### 👤 Aluno
> "Estou iniciando a atividade de criar a aplicação no Streamlit com dois dashboards baseados na minha EDA com 500 estudantes de inglês. Desenhei o rascunho de layout com uma barra lateral de filtros e a área principal dividida em duas abas (uma para o laboratório de análise e outra para os KPIs). Como podemos montar o esqueleto inicial do app.py no Streamlit seguindo as boas práticas da biblioteca?"

### 🤖 Assistente (Antigravity)
> Analisei a estrutura da sua análise exploratória e os requisitos da atividade. Para construir uma aplicação limpa e escalável no Streamlit:
> 
> 1. **Configuração de Página:** Iniciamos com `st.set_page_config(layout="wide")` para que os dashboards aproveitem toda a largura da tela.
> 2. **Barra Lateral (`st.sidebar`):** Criamos os filtros globais com `st.multiselect` para seleção das variáveis quantitativas e `st.slider` dinâmico para delimitar o intervalo de tempo de dedicação na plataforma.
> 3. **Organização em Abas (`st.tabs`):** Estruturamos a navegação principal com:
>    ```python
>    tab_kpis, tab_lab = st.tabs(["📊 Painel Executivo (KPIs)", "🔬 Laboratório: Distribuição e Correlação"])
>    ```
> 4. **Placeholders:** Deixamos recipientes organizados em cada aba para receber os cartões e as visualizações das próximas aulas.

---

## 📌 Interação 2: Validação dos Dados da EDA e Carregamento com Cache (Aula 21)

### 👤 Aluno
> "No notebook, a gente não modificou nada no CSV. O CSV permaneceu igual a como ele já estava, porque não havia duplicadas nem muitos erros faltando. Então, o CSV original já era o CSV limpo. Verifique isso para mim para ter certeza de como salvar e carregar no app."

### 🤖 Assistente (Antigravity)
> Verifiquei tudo detalhadamente no seu notebook e no arquivo original, e você está coberto de razão!
> 
> * **Zero Linhas Removidas:** O dataset tem exatamente 500 linhas do início ao fim da análise.
> * **Zero Valores Nulos (`NaN`):** Não há dados ausentes em nenhuma das 17 colunas originais.
> * **Zero Linhas Duplicadas:** A base é consistente e íntegra.
> 
> O que foi feito no notebook foi a criação das colunas enriquecidas (`ganho_medio` e classes de `desempenho`). Para a aplicação:
> 1. No notebook, salvamos o dataframe tratado com `df.to_csv("data/clean/dataset.csv", index=False)`.
> 2. Criamos o módulo `src/data_loader.py` com o decorador `@st.cache_data`:
>    ```python
>    @st.cache_data
>    def load_data(path="data/clean/dataset.csv"):
>        return pd.read_csv(path)
>    ```
>    Isso garante que o Streamlit leia os dados da memória após a primeira carga, deixando a resposta aos filtros instantânea.

---

## 📌 Interação 3: Dashboard 1 — Correlação de Spearman e Histogramas (Aula 21)

### 👤 Aluno
> "Me explique melhor para eu entender as decisões do Dashboard 1. Quero entender como estruturar o mapa de calor de correlação de Spearman e os histogramas no Altair para responderem aos filtros da barra lateral."

### 🤖 Assistente (Antigravity)
> O Dashboard 1 funciona como o **"Laboratório Estatístico"**: ele foi pensado para investigação livre de relações e distribuições.
> 
> * **Heatmap Triangular no Altair:** Calculamos a correlação com `df_filtrado[variaveis].corr(method="spearman")`. Para não poluir a tela repetindo os mesmos pares espelhados, filtramos apenas a parte triangular da matriz. No Altair, desenhamos com `mark_rect()` usando escala divergente e sobrepomos os valores numéricos com `mark_text()`.
> * **Grade de Histogramas:** Criamos um loop que divide o espaço em duas colunas (`st.columns(2)`) e gera histogramas com agrupamento automático (`bin=alt.Bin(maxbins=20)`).
> * **Tratamento de Exceções:** Adicionamos verificações como `if len(variaveis) < 2: st.warning(...)` para guiar o usuário caso ele desmarque as variáveis na barra lateral.

---

## 📌 Interação 4: Definição da Métrica de Negócio e Tempo de Uso (Aula 21/22)

### 👤 Aluno
> "Eu acho que a melhor métrica para esse contexto seria ver o tempo de uso da plataforma. Se a gente pensar na parte de negócios, a gente quer saber se, ao usar mais tempo a nossa plataforma, a pessoa estaria ou não aprendendo, para identificar erros, melhorias e esse tipo de coisa. Então, a minha decisão seria o tempo de uso da plataforma, e eu quero saber o que você acha dessa minha escolha."

### 🤖 Assistente (Antigravity)
> A sua escolha foi excelente, e o seu raciocínio de negócio foi impecável!
> 
> 1. **Hipótese Central de EdTech:** Em qualquer plataforma de aprendizado digital, a premissa fundamental é: *"quanto mais tempo o aluno investe na ferramenta, maior deve ser a retenção e o ganho de conhecimento"*.
> 2. **Poder Analítico no Painel:** Usar o tempo de uso da plataforma no slider permite confrontar diretamente o volume de horas estudadas com a evolução real nas notas, identificando tanto alunos engajados quanto casos que demandam intervenção pedagógica.

---

## 📌 Interação 5: Dashboard 2 — Definição dos KPIs e Público-Alvo (Aula 22)

### 👤 Aluno
> "Quero escolher ganho médio, tempo médio de uso e taxa de alta frequência. Além disso, seria para a equipe de produto da plataforma EdTech."

### 🤖 Assistente (Antigravity)
> Excelente direcionamento! Focar na **Equipe de Produto da Plataforma EdTech** traz um propósito estratégico muito forte para o painel: entender eficácia, engajamento e retenção.
> 
> As 3 métricas que você escolheu cobrem os pilares fundamentais do produto:
> 1. **Ganho Médio (`ganho_medio`):** Mede a eficácia do conteúdo pedagógico.
> 2. **Tempo Médio de Uso (`Time_Spent_Platform`):** Mede o nível de engajamento dos usuários ativos.
> 3. **Taxa de Alta Frequência (`Platform_Usage_Frequency >= 4`):** Mede a retenção e a formação de hábito semanal de estudo.
> 
> Para exibi-los no topo do Dashboard 2, utilizamos `col1, col2, col3 = st.columns(3)` com `st.metric()`, incluindo deltas comparativos contextuais.

---

## 📌 Interação 6: Dashboard 2 — Visuais e Seleção Cruzada no Altair (Aula 22)

### 👤 Aluno
> "Gostei muito da ideia de analisar o ganho por estilo de aprendizagem e a dispersão do tempo de uso vs ganho, além do comparativo de notas antes e depois. Quero aprovar esses três visuais para o Dashboard 2. Como conectamos o estilo de aprendizagem com o gráfico de dispersão para ter filtro interativo no Altair?"

### 🤖 Assistente (Antigravity)
> Para implementar a interatividade cruzada (*cross-filtering*) no Altair dentro do Streamlit:
> 
> 1. Criamos um objeto de seleção por clique no gráfico de barras:
>    ```python
>    clique_estilo = alt.selection_point(name="filtro_estilo", fields=["Learning_Style"])
>    ```
> 2. No gráfico de dispersão, aplicamos o filtro vinculado a esse clique:
>    ```python
>    dispersao = base.transform_filter(clique_estilo)
>    ```
> 3. Concatenamos os dois gráficos lado a lado usando o operador horizontal:
>    ```python
>    st.altair_chart(barras_estilo | dispersao_tempo, width="stretch")
>    ```
> Dessa forma, ao clicar na barra de um estilo de estudo (ex: "Visual"), o gráfico de dispersão ao lado filtra na hora apenas os alunos daquele perfil.

---

## 📌 Interação 7: Refinamento Visual das Barras Horizontais (Aula 22/23)

### 👤 Aluno
> "Uma correção: no visual 3 do site, era para ser um gráfico de barras horizontais. Parece um gráfico de barras horizontais, mas ele está bugado, como se fosse vertical. Temos que ajeitar isso."

### 🤖 Assistente (Antigravity)
> O problema era que o Altair estava particionando as habilidades em colunas verticais estreitas.
> 
> Reestruturei o código para um verdadeiro gráfico de barras horizontais emparelhadas:
> * **Eixo Vertical (Y):** As três habilidades avaliadas (Vocabulário, Leitura e Fala).
> * **Eixo Horizontal (X):** As notas médias (0 a 100), com as barras de Pré e Pós posicionadas lado a lado para cada habilidade através de `yOffset="Momento:N"`.
> * **Rótulos Diretos:** Adicionamos o valor exato da média na extremidade de cada barra com `mark_text`, garantindo contraste adequado tanto no modo claro quanto no escuro.
