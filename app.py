# [IA] Antigravity (Claude Sonnet / Gemini) – Estrutura base e widgets do Dashboard 1 (Aula 21)
import altair as alt
import pandas as pd
import streamlit as st

from src.data_loader import load_data

st.set_page_config(
    page_title="Avaliação de Aprendizado de Inglês - College English Learning",
    layout="wide",
)

st.title("Laboratório de Análise: Distribuição e Correlação")
st.caption(
    "Exploração de desempenho e engajamento de 500 estudantes universitários em plataforma de inglês (Dataset Kaggle: ziya07)."
)

# Carrega os dados com cache (@st.cache_data no src/data_loader.py)
df = load_data()

# Todas as variáveis quantitativas disponíveis no estudo
VARS_QUANT = [
    "Age",
    "Prior_English_Proficiency",
    "Time_Spent_Platform",
    "Vocabulary_Pre",
    "Reading_Comprehension_Pre",
    "Speaking_Pre",
    "Vocabulary_Post",
    "Reading_Comprehension_Post",
    "Speaking_Post",
    "Vocabulary_Improvement",
    "Reading_Improvement",
    "Speaking_Improvement",
    "ganho_medio",
]

# Seleção padrão inicial equilibrada
VARS_DEFAULT = [
    "Prior_English_Proficiency",
    "Time_Spent_Platform",
    "Vocabulary_Improvement",
    "Reading_Improvement",
    "Speaking_Improvement",
    "ganho_medio",
]

# Sidebar: Filtros da aplicação
with st.sidebar:
    st.header("Filtros")

    # 1. Seletor de variáveis quantitativas
    variaveis = st.multiselect(
        "Variáveis Quantitativas",
        options=VARS_QUANT,
        default=VARS_DEFAULT,
        help="Selecione quais variáveis quantitativas deseja incluir na matriz de correlação e histogramas.",
    )

    # 2. Filtro de intervalo: Tempo de uso na plataforma (decisão pedagógica e de negócio do aluno)
    min_tempo = int(df["Time_Spent_Platform"].min())
    max_tempo = int(df["Time_Spent_Platform"].max())
    intervalo_tempo = st.slider(
        "Tempo na Plataforma (horas)",
        min_value=min_tempo,
        max_value=max_tempo,
        value=(min_tempo, max_tempo),
        step=1,
        help="Filtra a base de alunos pelo tempo de dedicação à plataforma de ensino.",
    )

    # 3. Toggle para distinguir por classe de desempenho
    separar_por_classe = st.toggle(
        "Distinguir por Desempenho",
        value=False,
        help="Colore a distribuição pelo grupo de desempenho (Alto ganho vs Baixo ganho).",
    )

# Aplicação do filtro de intervalo selecionado
df_filtrado = df[df["Time_Spent_Platform"].between(intervalo_tempo[0], intervalo_tempo[1])]

st.caption(
    f"Exibindo **{len(df_filtrado)}** de **{len(df)}** alunos dentro da faixa de tempo de {intervalo_tempo[0]}h a {intervalo_tempo[1]}h."
)

# Layout do Dashboard 1: Correlação à esquerda e Distribuição à direita
col_correlacao, col_distribuicao = st.columns([1, 1.4])

# Paleta de cores definida na EDA do aluno
COR_BAIXO_GANHO = "#e9d4d0"  # Rosa claro
COR_ALTO_GANHO = "#2d223a"   # Roxo escuro
COR_HISTOGRAMA = COR_ALTO_GANHO
CORES_CLASSE = alt.Scale(
    domain=["Baixo ganho", "Alto ganho"],
    range=[COR_BAIXO_GANHO, COR_ALTO_GANHO],
)

LEGENDA_CLASSE = (
    f"**Desempenho**  \n"
    f":color[■]{{foreground=\"{COR_BAIXO_GANHO}\"}} Baixo ganho  \n"
    f":color[■]{{foreground=\"{COR_ALTO_GANHO}\"}} Alto ganho"
)

# Coluna 1: Mapa de Calor de Correlação (Spearman)
with col_correlacao:
    st.subheader("Correlação (Spearman)")

    if len(variaveis) < 2:
        st.warning("Selecione pelo menos 2 variáveis no painel lateral para calcular a correlação.")
    elif len(df_filtrado) < 15:
        st.warning("Poucos alunos no intervalo de tempo escolhido para calcular correlação confiável.")
    else:
        # Matriz de correlação de Spearman em formato longo
        corr = (
            df_filtrado[variaveis]
            .corr(method="spearman")
            .rename_axis(index="var_y", columns="var_x")
            .stack()
            .rename("correlacao")
            .reset_index()
        )
        # Triângulo inferior (remove redundâncias e a diagonal de autocorrelação = 1.0)
        ordem = {var: i for i, var in enumerate(variaveis)}
        corr = corr[corr["var_y"].map(ordem) > corr["var_x"].map(ordem)]

        base = alt.Chart(corr).encode(
            x=alt.X(
                "var_x:N",
                title=None,
                sort=variaveis[:-1],
                axis=alt.Axis(labelAngle=-45, labelFontSize=11),
            ),
            y=alt.Y("var_y:N", title=None, sort=variaveis[1:], axis=alt.Axis(labelFontSize=11)),
        )

        heatmap = base.mark_rect().encode(
            color=alt.Color(
                "correlacao:Q",
                title="Spearman",
                scale=alt.Scale(scheme="purpleorange", domain=[-1, 1]),
                legend=alt.Legend(titleFontSize=12, labelFontSize=11),
            ),
            tooltip=["var_x", "var_y", alt.Tooltip("correlacao:Q", format=".2f")],
        )

        valores = base.mark_text(fontSize=13).encode(
            text=alt.Text("correlacao:Q", format=".2f"),
            color=alt.condition(
                "abs(datum.correlacao) > 0.4", alt.value("white"), alt.value("black")
            ),
        )

        st.altair_chart(
            (heatmap + valores).properties(height=420),
            width="stretch",
            alt="Mapa de calor da correlação de Spearman entre as variáveis selecionadas",
        )

# Coluna 2: Histogramas de Distribuição
with col_distribuicao:
    st.subheader("Distribuição das Variáveis")

    if not variaveis:
        st.warning("Selecione pelo menos 1 variável no painel lateral para visualizar sua distribuição.")
    elif df_filtrado.empty:
        st.warning("Nenhum aluno encontrado no intervalo de tempo selecionado.")
    else:
        if separar_por_classe and len(variaveis) % 2 == 0:
            st.markdown(LEGENDA_CLASSE)

        # Grade de histogramas com 2 colunas
        for inicio in range(0, len(variaveis), 2):
            colunas = st.columns(2)
            for coluna, var in zip(colunas, variaveis[inicio : inicio + 2]):
                hist_chart = (
                    alt.Chart(df_filtrado[[var, "desempenho"]])
                    .mark_bar()
                    .encode(
                        x=alt.X(f"{var}:Q", bin=alt.Bin(maxbins=20), title=var),
                        y=alt.Y("count()", title="Alunos"),
                        tooltip=[alt.Tooltip("count()", title="Qtd Alunos")],
                    )
                    .properties(height=200)
                )

                if separar_por_classe:
                    hist_chart = hist_chart.encode(
                        color=alt.Color(
                            "desempenho:N",
                            title="Desempenho",
                            scale=CORES_CLASSE,
                            legend=None,
                        ),
                        tooltip=["desempenho", alt.Tooltip("count()", title="Qtd Alunos")],
                    )
                else:
                    hist_chart = hist_chart.mark_bar(color=COR_HISTOGRAMA)

                with coluna:
                    st.altair_chart(hist_chart, width="stretch", alt=f"Histograma da variável {var}")

            if separar_por_classe and len(colunas) == 2 and len(variaveis[inicio : inicio + 2]) == 1:
                colunas[1].markdown(LEGENDA_CLASSE)

# TODO: Dashboard 2 — KPIs e métricas do público-alvo (Aulas 22 e 23)
