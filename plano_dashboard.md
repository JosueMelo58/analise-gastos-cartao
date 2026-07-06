# 📊 Plano do Dashboard — Gastos de Cartão de Crédito

Plano de um dashboard ideal para extrair o máximo de insights do `extrato_cartao_2026.csv`, desenhado a partir dos padrões reais encontrados na análise da base.

## O que os dados pedem (achados que guiam o design)

| Achado na base | Implicação para o dashboard |
|---|---|
| Gasto médio de R$ 12.344/mês com variação de 18,3% (pico de R$ 16.070 em abril) | KPI de gasto vs. média + **alerta automático** quando o mês foge do padrão |
| E-commerce = 30,4%; top 3 categorias = 60,7% do total | Visão de **concentração** (treemap) com drill-down por categoria |
| Top 10 estabelecimentos = 64,9% do gasto | **Pareto de estabelecimentos** — poucos lojistas explicam quase tudo |
| 21 compras >R$ 500 = 22,4% do gasto | Separar **compras grandes** do gasto rotineiro (visões distintas) |
| Parcelado = 12,3%, com parcelas que avançam meses | Projeção de **compromisso futuro** das faturas |
| Assinaturas fixas ~R$ 310/mês | Painel de **recorrências** com custo anualizado |
| 29,9% do gasto no fim de semana; 37,3% após 18h; delivery 1,7x/semana | **Heatmap comportamental** dia × hora |
| Cartão adicional = 13% | Filtro/segmentação por **titular** |
| Estornos e dados sujos na origem | Aba de **qualidade de dados** (diferencial técnico) |

## Arquitetura: 4 páginas + filtros globais

**Filtros globais (persistentes em todas as páginas):** período (mês/intervalo) · categoria · titular · tipo de pagamento · toggle "excluir estornos".

### Página 1 — Visão Executiva *(responde: "como estou este mês?")*

- **KPIs:** gasto do mês (com Δ% vs. média semestral), comprometido futuro em parcelas, custo fixo de assinaturas, ticket médio
- **Linha do gasto mensal** com banda da média ±1 desvio e linha de meta de orçamento
- **Treemap de categorias** do período selecionado
- **Painel de alertas** (regras): mês >20% acima da média · nova assinatura detectada · compra individual >R$ 500 · categoria estourando o próprio histórico

### Página 2 — Categorias & Estabelecimentos *(responde: "para onde vai o dinheiro?")*

- **Pareto de estabelecimentos** (barra + % acumulado) — evidencia os 64,9% concentrados no top 10
- **Evolução mensal por categoria** (linhas, top 5 selecionáveis)
- **Ticket médio × frequência** (scatter): separa "caro e raro" (Viagem) de "barato e frequente" (Delivery) — cada quadrante pede uma estratégia de economia diferente
- **Tabela detalhada** com busca, ordenação e exportação (nível transação)

### Página 3 — Comportamento & Hábitos *(responde: "quando e como eu gasto?")*

- **Heatmap dia da semana × hora** (nº de transações e R$)
- **Semana vs. fim de semana** e por período do dia
- **Frequência de delivery** (pedidos/semana, com custo acumulado do mês)
- **Distribuição de valores** (histograma + boxplot): rotina (mediana R$ 76) vs. caudas (p95 R$ 483)
- **Compras grandes** (>R$ 500): timeline dos 21 eventos que somam 22,4% do gasto

### Página 4 — Planejamento & Compromissos *(responde: "e daqui pra frente?")*

- **Projeção de faturas futuras**: parcelas já contratadas mês a mês (barras empilhadas: contratado vs. estimado do gasto variável)
- **Assinaturas**: custo mensal, anualizado e "custo por uso" quando aplicável
- **Simulador de economia**: sliders por categoria mostrando impacto na média mensal (meta: 15%)
- **Orçamento por categoria**: realizado vs. limite definido pelo usuário (bullet charts)

### Extra — Aba "Qualidade de Dados" (diferencial de portfólio)

Duplicatas removidas, nulos imputados, formatos normalizados — o "antes e depois" do pipeline, mostrando ao recrutador que o dashboard nasce de dados tratados com critério.

## Decisões de design

- **Hierarquia de leitura:** KPIs no topo (3 segundos), gráficos principais no meio (30 segundos), detalhe/tabela embaixo (exploração livre)
- **Estornos:** excluídos por padrão dos gráficos de hábito, incluídos nos totais (toggle explícito)
- **Cores:** paleta única por categoria em todas as páginas (consistência cognitiva); vermelho reservado a alertas
- **Interatividade mínima viável:** clique em categoria filtra a página inteira (cross-filtering)

## Stack recomendada

| Opção | Quando escolher |
|---|---|
| **Streamlit + Plotly** (recomendada p/ portfólio) | Mostra Python de ponta a ponta; deploy grátis no Streamlit Cloud; código vira parte do portfólio |
| Power BI | Se a vaga pede a ferramenta; DAX para medidas de projeção |
| Dash / Looker Studio | Alternativas válidas; Looker é rápido mas limitado no simulador |

**Modelagem:** camada única `fato_transacoes` (a base limpa do notebook) + dimensões derivadas (`dim_calendario`, `dim_categoria`). Medidas-chave: `gasto_liquido`, `gasto_vs_media_%`, `comprometido_futuro`, `custo_recorrente_mensal`.

## Roadmap de implementação

1. **MVP (1–2 dias):** Página 1 com filtros globais e KPIs
2. **v2:** Páginas 2 e 3 (drill-down + comportamento)
3. **v3:** Página 4 (projeções + simulador) e alertas
4. **Polimento:** aba de qualidade, tema visual, deploy público com link no README do GitHub
