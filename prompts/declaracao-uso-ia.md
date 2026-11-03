# Declaração de Uso de Inteligência Artificial Generativa
**Disciplina:** Análise e Visualização de Dados (AVD 2026.2) – CESAR School  
**Atividade:** Dashboards com Streamlit (Aulas 21 a 23)  
**Aluno:** Eduardo  
**Repositório:** [https://github.com/eduaab/AVD-20262-pratica-streamlit](https://github.com/eduaab/AVD-20262-pratica-streamlit)  
**Data:** 02/11/2026  

---

> **Nota de Privacidade e Proteção de Dados (LGPD):**  
> A via formal assinada digitalmente deste documento (`DECLARACAO_IA.pdf`) foi anexada de forma restrita e segura na submissão do Google Classroom, resguardando a exposição pública de dados pessoais e certificados criptográficos neste repositório.

---

## 1. Declaração Geral

- [x] **Utilizei IA generativa, somente nas situações permitidas, e registrei todos os usos nas seções abaixo.**

---

## 2. Ferramentas Utilizadas

| Ferramenta | Versão / Ambiente | Em que parte da atividade |
| :--- | :--- | :--- |
| **Google Antigravity** | Claude Sonnet 4.6 / Gemini 3.8 Flash | Esqueleto do `app.py`, sintaxe dos gráficos no Altair (Dashboards 1 e 2), depuração de layout e suporte ao deploy. |
| **Streamlit Skills** | Skill oficial via CLI (`streamlit skills`) | Boas práticas de arquitetura, cache (`@st.cache_data`), widgets e containers do Streamlit. |

---

## 3. Registro de Usos (Transcrição Anexada)

- **Arquivo no repositório:** [`prompts/transcricao_conversa.md`](transcricao_conversa.md)
- **Link direto no GitHub:** [https://github.com/eduaab/AVD-20262-pratica-streamlit/blob/main/prompts/transcricao_conversa.md](https://github.com/eduaab/AVD-20262-pratica-streamlit/blob/main/prompts/transcricao_conversa.md)

O arquivo acima registra o diálogo completo mantido com a ferramenta de IA durante o projeto, evidenciando as decisões autônomas do aluno e as consultas técnicas realizadas.

---

## 4. Trechos de Código com Apoio de IA

| Arquivo / Parte | Teve apoio de IA? | Tipo de Apoio |
| :--- | :---: | :--- |
| **`app.py` (esqueleto)** | ☑ Sim ☐ Não | Estruturação inicial via Skill do Streamlit e configuração de cache com `@st.cache_data`. |
| **Dashboard 1 (correlação + distribuição)** | ☑ Sim ☐ Não | Sintaxe do Altair para heatmap triangular (Spearman), grade de histogramas e lógica do slider de tempo. |
| **Dashboard 2 (KPIs e gráficos)** | ☑ Sim ☐ Não | Sintaxe de `st.metric`, seleção interativa no Altair (cross-filtering) e gráfico de barras horizontais agrupadas. |
| **Deploy e Configuração** | ☑ Sim ☐ Não | Ajuste de contraste visual no `.streamlit/config.toml` e conferência de dependências. |

---

## 5. Reflexão Individual

Utilizei a IA generativa apenas como ferramenta de suporte técnico e consulta, principalmente para auxiliar na sintaxe de bibliotecas de código (como Streamlit e Altair), no entendimento de erros e na geração da estrutura básica do esqueleto da aplicação.

Em nenhum momento a IA tomou decisões analíticas ou conceituais pelo projeto. Todas as definições estratégicas e escolhas mais importantes foram tomadas exclusivamente por mim: a definição do público-alvo voltado à equipe de produto da EdTech, a escolha das variáveis que realmente faziam sentido filtrar na barra lateral e a seleção das métricas de negócio e dos gráficos que compõem o painel executivo.

A IA atuou no máximo me auxiliando a compreender as possibilidades técnicas e a agilizar a codificação visual, mas cada escolha, cálculo e interpretação dos dados passou pela minha validação crítica, garantindo que o painel refletisse fielmente os objetivos da minha análise exploratória.
