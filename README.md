# 💳 Análise de Gastos de Cartão de Crédito

Projeto de portfólio de **Análise de Dados** de ponta a ponta: parte de um extrato bruto e sujo de cartão de crédito (jan–jun/2026), passa por um pipeline documentado de limpeza e análise exploratória em Python, e termina em um **dashboard interativo** — onde cada número exibido é rastreável até a célula do notebook que o calculou.

> **Nota:** os dados são fictícios, gerados por script (seed fixa = reprodutível) para simular um extrato real — incluindo os problemas de qualidade típicos de dados do mundo real: duplicatas, nulos e formatos inconsistentes.

## 🚀 Comece por aqui

| O que ver | Como |
|---|---|
| **Dashboard interativo** | Baixe o repositório e abra `dashboard.html` com duplo clique (não precisa de servidor) |
| **Análise completa** | `analise_gastos_cartao.ipynb` — renderiza direto aqui no GitHub |
| **Base bruta** | `extrato_cartao_2026.csv` (~510 linhas com sujeira proposital) |

## 📁 Estrutura do projeto

```
├── extrato_cartao_2026.csv         # Base BRUTA (com sujeira proposital)
├── extrato_cartao_2026_limpo.csv   # Base tratada (saída do notebook)
├── gerar_extrato.py                # Script gerador da base fictícia
├── analise_gastos_cartao.ipynb     # Notebook: limpeza → EDA → insights → rastreabilidade
├── dados_dashboard.json            # Dados limpos exportados pelo notebook (seção 8.7)
├── dashboard.html                  # Dashboard interativo (single-file, HTML+JS puro)
├── mockup_dashboard.html           # Mockup estático que precedeu o dashboard
├── plano_dashboard.md              # Plano/spec do dashboard (páginas, KPIs, decisões)
├── index.html                      # Redireciona para o dashboard (GitHub Pages)
└── assets/                         # Tailwind runtime + ícones (uso offline)
```

## 📊 Os dados

**513 transações** (após limpeza: 505 únicas) em 6 meses, 21 categorias, com assinaturas recorrentes, compras parceladas, uma viagem internacional (Buenos Aires, maio) e estornos.

| Coluna | Descrição | Problema proposital |
|---|---|---|
| `id_transacao` | Identificador único | 8 linhas duplicadas |
| `data_hora` | Data/hora da compra | 3 formatos misturados (`YYYY-MM-DD HH:MM:SS`, `DD/MM/YYYY HH:MM`, ISO com `T`) |
| `estabelecimento` | Nome do lojista | Caixa inconsistente; sufixo de parcela (`2/6`) embutido no nome |
| `categoria` | Categoria do gasto | ~4% nulos; grafias inconsistentes |
| `valor` | Valor em R$ | Texto com 3 formatos (`123.45`, `123,45`, `R$ 123.45`); negativos = estornos |
| `cidade` / `pais` | Local da compra | ~2% de cidades nulas |
| `tipo_pagamento`, `parcelas`, `titular` | Forma de pagamento e portador | — |

## 🧪 O notebook (`analise_gastos_cartao.ipynb`)

Pipeline completo em 8 seções, com cada decisão de limpeza justificada em texto:

1. **Setup** — bibliotecas e configurações
2. **Carga e primeira inspeção** — conhecendo a base antes de alterá-la
3. **Diagnóstico de qualidade** — cada problema é *medido* antes de corrigido (evidência do antes/depois)
4. **Limpeza** — datas multi-formato (com tratamento explícito do formato BR para evitar troca silenciosa de dia/mês), valores texto→float, deduplicação por chave, normalização de texto, extração de nº de parcela via regex, imputação de categoria pela moda do estabelecimento — tudo validado com `assert`
5. **Enriquecimento** — mês, dia da semana, período do dia, flags de assinatura/internacional/estorno
6. **EDA** — evolução mensal, concentração por categoria, heatmap dia×hora, assinaturas, parcelamentos, outliers
7. **Conclusões** — simulação de economia de 15% e resumo executivo gerado dinamicamente dos dados
8. **Rastreabilidade** — *todos* os números do dashboard são recalculados aqui; a seção 8.7 exporta a base limpa em CSV e JSON

## 🖥️ O dashboard (`dashboard.html`)

Single-file: HTML + JavaScript puro, com os dados limpos embutidos e assets locais — funciona offline, abre com duplo clique.

**4 páginas:**

| Página | Responde | Destaques |
|---|---|---|
| **Visão Executiva** | "Como estou este mês?" | 4 KPIs, gasto mensal, treemap de categorias, Pareto de lojistas, alertas automáticos |
| **Categorias & Lojistas** | "Para onde vai o dinheiro?" | Ranking clicável (filtra ao clicar), evolução top 5, scatter ticket×frequência, tabela com busca/ordenação/paginação |
| **Comportamento** | "Quando e como eu gasto?" | Heatmap dia×hora, período do dia, semana vs. FDS, histograma, maiores compras |
| **Planejamento** | "E daqui pra frente?" | Projeção de parcelas jul–dez, assinaturas, simulador de economia com meta de 15% |

**Filtros globais** (recalculam todas as páginas em tempo real): intervalo de meses, categorias (multi-seleção), titular, tipo de pagamento e toggle de estornos.

**Arquitetura:** `notebook (seção 8.7) → dados_dashboard.json → embutido no HTML → agregações em JS no navegador`. Como o dashboard agrega as mesmas 505 transações limpas que o notebook, os números conferem por construção — ex.: total do semestre R$ 74.067, top 3 categorias = 60,7%, CV mensal 18,3%.

## 💡 Principais insights da análise

1. Gasto de **R$ 74.067 no semestre** (média R$ 12.344/mês), com pico de +30% em abril puxado por parcelamentos e e-commerce.
2. **Concentração alta:** top 3 categorias = 60,7% do gasto; top 10 estabelecimentos = 64,9%. Apenas **21 compras acima de R$ 500 respondem por 22,4%** do total — o orçamento é dirigido por poucos eventos, não pelo cafezinho.
3. **Assinaturas** somam R$ 310/mês fixos (R$ 3,7 mil/ano) — gasto invisível clássico.
4. **Parcelamentos** comprometem 12,3% das faturas; após junho ainda restam R$ 760 contratados.
5. **Comportamento:** 37% do uso após as 18h e 30% do gasto no fim de semana; delivery 1,7×/semana.
6. O plano simulado (reduzir 40% da alimentação fora + cancelar 2 streamings + planejar parceladas) atinge a **meta de 15% de economia mensal**.

## 🛠️ Stack

Python (pandas, numpy, matplotlib, seaborn) · Jupyter · HTML/CSS (Tailwind) + JavaScript vanilla

## 🔁 Como reproduzir

```bash
# 1. (Opcional) Regenerar a base bruta — seed fixa garante reprodutibilidade
python gerar_extrato.py

# 2. Rodar o notebook (produz a base limpa e o dados_dashboard.json)
jupyter nbconvert --to notebook --execute --inplace analise_gastos_cartao.ipynb

# 3. Abrir o dashboard: duplo clique em dashboard.html
```

Dependências: `pip install pandas numpy matplotlib seaborn jupyter`

## 🗺️ Atualizações futuras

- 🤖 **Agente de IA conversacional** — "converse com seu extrato": perguntas em linguagem natural respondidas via *function calling* sobre as mesmas ferramentas de análise do notebook, com guardrails contra alucinação de números e suíte de avaliação automática *(em desenvolvimento)*
- 📈 Versão SQL das análises
- 🚨 Detecção de anomalias para alerta de fraude
- ☁️ Deploy do dashboard via GitHub Pages

## Partes do Dashboard

<img width="2482" height="1295" alt="image" src="https://github.com/user-attachments/assets/2e170352-8c43-456f-843f-324ecbf9bcc3" />
<img width="2482" height="1201" alt="image" src="https://github.com/user-attachments/assets/a1b0d012-2ed7-44ce-ab56-13692324cd8a" />
<img width="2486" height="1207" alt="image" src="https://github.com/user-attachments/assets/44a8bb27-03f0-4cf9-b628-61d4d25e5e1c" />
<img width="2477" height="1262" alt="image" src="https://github.com/user-attachments/assets/4779008e-be6b-461a-bd29-08f9c78c5389" />



