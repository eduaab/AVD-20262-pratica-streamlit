# [IA] Antigravity (Claude Sonnet / Gemini) – Aplicação Completa com Dois Dashboards (Aulas 21 e 22)
import altair as alt
import pandas as pd
import streamlit as st

from src.data_loader import load_data

st.set_page_config(
    page_title="Analytics de Aprendizado - College English Learning",
    layout="wide",
)

st.title("Plataforma EdTech: Monitoramento e Laboratório de Dados")
st.caption(
    "Ambiente analítico para avaliação de desempenho e engajamento de 500 estudantes de inglês (Dataset Kaggle: ziya07)."
)

# Carrega os dados com cache (@st.cache_data no src/data_loader.py)
df = load_data()

# Variáveis quantitativas disponíveis no estudo
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

VARS_DEFAULT = [
    "Prior_English_Proficiency",
    "Time_Spent_Platform",
    "Vocabulary_Improvement",
    "Reading_Improvement",
    "Speaking_Improvement",
    "ganho_medio",
]

# Sidebar: Filtros globais da aplicação
with st.sidebar:
    st.header("Filtros Globais")

    # 1. Seletor de variáveis para análise exploratória
    variaveis = st.multiselect(
        "Variáveis Quantitativas (Lab)",
        options=VARS_QUANT,
        default=VARS_DEFAULT,
        help="Selecione quais variáveis quantitativas deseja analisar no Laboratório de Correlação e Distribuição.",
    )

    # 2. Filtro de intervalo: Tempo de uso na plataforma (Decisão do aluno voltada a negócio/EdTech)
    min_tempo = int(df["Time_Spent_Platform"].min())
    max_tempo = int(df["Time_Spent_Platform"].max())
    intervalo_tempo = st.slider(
        "Tempo na Plataforma (horas)",
        min_value=min_tempo,
        max_value=max_tempo,
        value=(min_tempo, max_tempo),
        step=1,
        help="Filtra os estudantes pelo tempo acumulado de dedicação aos estudos.",
    )

    # 3. Toggle para distinguir por classe de desempenho
    separar_por_classe = st.toggle(
        "Distinguir por Desempenho",
        value=False,
        help="Colore os gráficos pelo grupo de desempenho (Alto ganho vs Baixo ganho).",
    )

# Filtro global aplicado ao DataFrame
df_filtrado = df[df["Time_Spent_Platform"].between(intervalo_tempo[0], intervalo_tempo[1])]

st.caption(
    f"Base ativa: **{len(df_filtrado)}** de **{len(df)}** alunos dentro da faixa de {intervalo_tempo[0]}h a {intervalo_tempo[1]}h na plataforma."
)

# Paleta oficial da EDA do aluno
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

# Criação das Abas para os Dois Dashboards
tab_kpis, tab_lab = st.tabs(
    ["📊 Painel Executivo de Produto (KPIs)", "🔬 Laboratório: Distribuição e Correlação"]
)

# ==============================================================================
# DASHBOARD 2: Painel Executivo da Equipe de Produto (KPIs e Métricas Estratégicas)
# ==============================================================================
with tab_kpis:
    st.subheader("Indicadores de Engajamento e Eficácia de Aprendizado")
    st.markdown(
        "Painel orientado à **Equipe de Produto da EdTech**, combinando métricas de impacto pedagógico, tempo investido e hábitos de retenção."
    )

    if df_filtrado.empty:
        st.warning("Nenhum dado encontrado para o filtro atual de tempo na plataforma.")
    else:
        # 1. Linha de Métricas Principais (3 KPIs de negócio)
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

        media_ganho = df_filtrado["ganho_medio"].mean()
        tempo_medio = df_filtrado["Time_Spent_Platform"].mean()
        taxa_alta_freq = (df_filtrado["Platform_Usage_Frequency"] >= 4).mean() * 100
        qtd_alta_freq = (df_filtrado["Platform_Usage_Frequency"] >= 4).sum()

        with col_kpi1:
            st.metric(
                label="Ganho Médio Global",
                value=f"{media_ganho:.2f} pts",
                delta=f"{(media_ganho - 12.0):+.2f} pts vs mediana",
                help="Pontuação média de evolução agregada nas três habilidades (Vocabulário, Leitura e Fala).",
            )

        with col_kpi2:
            st.metric(
                label="Tempo Médio de Uso",
                value=f"{tempo_medio:.1f} h",
                delta=f"Amostra: {len(df_filtrado)} alunos",
                help="Média de horas que os alunos ativos passaram utilizando os módulos da plataforma.",
            )

        with col_kpi3:
            st.metric(
                label="Taxa de Alta Frequência",
                value=f"{taxa_alta_freq:.1f}%",
                delta=f"{qtd_alta_freq} alunos com >= 4 dias/sem",
                help="Percentual de alunos que mantêm rotina consistente de estudos (4 ou mais dias por semana).",
            )

        st.markdown("---")

        # 2. Visuais 1 e 2: Interatividade Cruzada com Altair (Cross-filtering)
        st.subheader("Análise Comportamental: Estilos de Aprendizagem e Dispersão de Uso")
        st.caption(
            "💡 **Dica de Interatividade:** Clique em uma barra no gráfico de **Estilo de Aprendizagem** à esquerda para filtrar os alunos no gráfico de dispersão à direita!"
        )

        # Seleção interativa por clique no estilo de aprendizagem
        clique_estilo = alt.selection_point(name="filtro_estilo", fields=["Learning_Style"])

        # Visual 1: Ganho Médio por Estilo de Aprendizagem (Barras Horizontais para legibilidade perfeita)
        barras_base = (
            alt.Chart(df_filtrado)
            .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4, height=36)
            .encode(
                y=alt.Y("Learning_Style:N", title=None, axis=alt.Axis(labelFontSize=12)),
                x=alt.X("mean(ganho_medio):Q", title="Ganho Médio (pts)", scale=alt.Scale(domain=[0, 16])),
                opacity=alt.condition(clique_estilo, alt.value(1.0), alt.value(0.3)),
                color=alt.value(COR_ALTO_GANHO),
                tooltip=[
                    "Learning_Style:N",
                    alt.Tooltip("mean(ganho_medio):Q", format=".2f", title="Ganho Médio"),
                    alt.Tooltip("count()", title="Qtd Alunos"),
                ],
            )
            .add_params(clique_estilo)
        )

        rotulos_estilo = (
            alt.Chart(df_filtrado)
            .mark_text(dx=18, fontSize=11, fontWeight="bold")
            .encode(
                y=alt.Y("Learning_Style:N", title=None),
                x=alt.X("mean(ganho_medio):Q"),
                text=alt.Text("mean(ganho_medio):Q", format=".1f"),
                color=alt.value("white"),
            )
        )

        barras_estilo = (barras_base + rotulos_estilo).properties(
            width=280, height=300, title="Visual 1: Ganho Médio por Estilo"
        )

        # Visual 2: Scatter plot Tempo vs Ganho filtrado pela seleção
        dispersao_tempo = (
            alt.Chart(df_filtrado)
            .mark_circle(size=75, opacity=0.8)
            .encode(
                x=alt.X("Time_Spent_Platform:Q", title="Tempo na Plataforma (horas)"),
                y=alt.Y("ganho_medio:Q", title="Ganho Médio (pts)"),
                color=alt.Color("desempenho:N", title="Desempenho", scale=CORES_CLASSE),
                tooltip=[
                    "Student_ID:Q",
                    "Learning_Style:N",
                    "Time_Spent_Platform:Q",
                    alt.Tooltip("ganho_medio:Q", format=".2f", title="Ganho"),
                    "desempenho:N",
                ],
            )
            .transform_filter(clique_estilo)
            .properties(width=460, height=300, title="Visual 2: Tempo na Plataforma vs Ganho Médio (Reativo)")
        )

        st.altair_chart(barras_estilo | dispersao_tempo, width="stretch")

        st.markdown("---")

        # 3. Visual 3: Comparativo Pré vs Pós por Habilidade
        st.subheader("Visual 3: Eficácia de Conteúdo — Avaliação Pré vs Pós por Habilidade")
        st.caption(
            "Comparativo das pontuações médias antes e depois do uso da plataforma para orientar melhorias curriculares."
        )

        dados_comp = pd.DataFrame([
            {"Habilidade": "Vocabulário", "Momento": "Pré", "Média": df_filtrado["Vocabulary_Pre"].mean()},
            {"Habilidade": "Vocabulário", "Momento": "Pós", "Média": df_filtrado["Vocabulary_Post"].mean()},
            {"Habilidade": "Leitura", "Momento": "Pré", "Média": df_filtrado["Reading_Comprehension_Pre"].mean()},
            {"Habilidade": "Leitura", "Momento": "Pós", "Média": df_filtrado["Reading_Comprehension_Post"].mean()},
            {"Habilidade": "Fala", "Momento": "Pré", "Média": df_filtrado["Speaking_Pre"].mean()},
            {"Habilidade": "Fala", "Momento": "Pós", "Média": df_filtrado["Speaking_Post"].mean()},
        ])

        barras_comp = (
            alt.Chart(dados_comp)
            .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
            .encode(
                y=alt.Y("Habilidade:N", title=None, axis=alt.Axis(labelFontSize=13)),
                yOffset="Momento:N",
                x=alt.X("Média:Q", title="Nota Média (0 a 100)", scale=alt.Scale(domain=[0, 100])),
                color=alt.Color(
                    "Momento:N",
                    scale=alt.Scale(domain=["Pré", "Pós"], range=[COR_BAIXO_GANHO, COR_ALTO_GANHO]),
                    legend=alt.Legend(title="Avaliação", orient="top", labelFontSize=12),
                ),
                tooltip=["Habilidade", "Momento", alt.Tooltip("Média:Q", format=".2f", title="Nota Média")],
            )
        )

        rotulos_comp = (
            alt.Chart(dados_comp)
            .mark_text(dx=20, fontSize=12, fontWeight="bold")
            .encode(
                y=alt.Y("Habilidade:N", title=None),
                yOffset="Momento:N",
                x=alt.X("Média:Q"),
                text=alt.Text("Média:Q", format=".1f"),
                color=alt.value("white" if separar_por_classe or True else "black"),
            )
        )

        st.altair_chart((barras_comp + rotulos_comp).properties(height=260), width="stretch")


# ==============================================================================
# DASHBOARD 1: Laboratório de Distribuição e Correlação
# ==============================================================================
with tab_lab:
    st.subheader("Laboratório de Análise Estatística")
    st.caption("Investigação estatística detalhada de correlações e distribuições univariadas.")

    col_correlacao, col_distribuicao = st.columns([1, 1.4])

    with col_correlacao:
        st.markdown("##### Correlação (Spearman)")

        if len(variaveis) < 2:
            st.warning("Selecione pelo menos 2 variáveis no painel lateral para calcular a correlação.")
        elif len(df_filtrado) < 15:
            st.warning("Poucos alunos no intervalo de tempo escolhido para calcular correlação confiável.")
        else:
            corr = (
                df_filtrado[variaveis]
                .corr(method="spearman")
                .rename_axis(index="var_y", columns="var_x")
                .stack()
                .rename("correlacao")
                .reset_index()
            )
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
                alt="Mapa de calor da correlação de Spearman",
            )

    with col_distribuicao:
        st.markdown("##### Distribuição das Variáveis")

        if not variaveis:
            st.warning("Selecione pelo menos 1 variável no painel lateral para visualizar sua distribuição.")
        elif df_filtrado.empty:
            st.warning("Nenhum aluno encontrado no intervalo de tempo selecionado.")
        else:
            if separar_por_classe and len(variaveis) % 2 == 0:
                st.markdown(LEGENDA_CLASSE)

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
