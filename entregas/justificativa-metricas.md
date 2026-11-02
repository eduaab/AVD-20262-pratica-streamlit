# Justificativa das Métricas — Dashboard 2

**Público-alvo escolhido:** Equipe de Produto da Plataforma EdTech (Product Managers, Designers de Aprendizagem e Engenheiros).  
**Objetivo do painel:** Avaliar se o produto digital está entregando valor pedagógico (eficácia no aprendizado), se os usuários estão engajados (volume de uso) e se criaram o hábito de retornar com frequência à ferramenta.

---

## Métrica 1: Ganho Médio Geral de Aprendizado
- **Variável:** `ganho_medio` (média das colunas `Vocabulary_Improvement`, `Reading_Improvement` e `Speaking_Improvement`).
- **O que mede:** A pontuação média de evolução agregada dos estudantes entre as avaliações antes e depois do uso da plataforma digital.
- **Por que foi escolhida:** Representa a métrica principal de eficácia (North Star Metric) do produto educacional. Um produto EdTech só se sustenta no mercado se comprovadamente gerar avanço no conhecimento do usuário.
- **Público-alvo:** Equipe de Produto e Especialistas Pedagógicos.
- **Qual decisão pode ser apoiada por essa métrica:** Decisões sobre a qualidade dos conteúdos e métodos de ensino; se o ganho médio estiver abaixo da meta esperada, a equipe de produto deve priorizar reformulações nas trilhas de aprendizado e nos exercícios interativos.
- **O que comunica ao público-alvo:** O impacto pedagógico médio entregue pelo produto aos alunos em pontos percentuais/escala de evolução de forma resumida e direta.

---

## Métrica 2: Tempo Médio de Uso na Plataforma
- **Variável:** `Time_Spent_Platform` (tempo total acumulado na plataforma, em horas).
- **O que mede:** O volume médio de tempo que os alunos passaram ativamente navegando e consumindo conteúdos na plataforma.
- **Por que foi escolhida:** É a métrica clássica de engajamento de produto (Time on Platform). Permite confrontar se os alunos que passam mais tempo no ambiente digital conseguem transformar esse investimento de tempo em ganhos acadêmicos reais.
- **Público-alvo:** Equipe de Produto e UX/Design.
- **Qual decisão pode ser apoiada por essa métrica:** Permite identificar se a experiência de uso é envolvente o suficiente para reter a atenção dos alunos, apoiando decisões sobre gamificação, duração ideal das aulas e alertas de incentivo ao estudo.
- **O que comunica ao público-alvo:** O nível médio de dedicação horária dos usuários ao produto, sem necessidade de analisar distribuições estatísticas complexas.

---

## Métrica 3: Taxa de Alta Frequência de Uso
- **Variável:** `Platform_Usage_Frequency` (frequência semanal de acesso, medida de 1 a 6 dias por semana).
- **O que mede:** A proporção (%) de estudantes que utilizam a plataforma com alta regularidade, definida como 4 ou mais dias por semana (`frequência >= 4`).
- **Por que foi escolhida:** O aprendizado de um novo idioma depende fortemente da prática diária e do hábito. Para a equipe de produto, medir a taxa de usuários frequentes reflete a retenção ativa e a criação de rotina de estudo (stickiness do app).
- **Público-alvo:** Equipe de Produto e Growth.
- **Qual decisão pode ser apoiada por essa métrica:** Apoia decisões de disparo de notificações push, lembretes de rotina, sequências de ofensivas (streaks) e recursos de retenção para estimular o retorno contínuo dos alunos menos frequentes.
- **O que comunica ao público-alvo:** Qual fatia da base de alunos realmente incorporou a plataforma na sua rotina semanal de estudos.
