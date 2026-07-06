# -*- coding: utf-8 -*-
"""
Gerador de extrato de cartão de crédito fictício (jan-jun/2026).
Base mock para projeto de portfólio de Análise de Dados.
Inclui "sujeira" proposital: duplicatas, nulos, formatos inconsistentes.
"""
import csv
import random
from datetime import datetime, timedelta

random.seed(42)

# (estabelecimento, categoria, faixa_valor, cidade, peso)
MERCHANTS = [
    # Alimentação - Supermercado
    ("SUPERMERCADO PAO DE ACUCAR", "Supermercado", (80, 450), "Sao Paulo", 10),
    ("CARREFOUR HIPER", "Supermercado", (60, 520), "Sao Paulo", 8),
    ("MERCADO DIA%", "Supermercado", (25, 120), "Sao Paulo", 6),
    ("HORTIFRUTI NATURAL DA TERRA", "Supermercado", (30, 110), "Sao Paulo", 4),
    # Alimentação - Restaurantes/Delivery
    ("IFOOD *RESTAURANTE", "Delivery", (25, 95), "Sao Paulo", 14),
    ("RAPPI*RAPPI BRASIL", "Delivery", (20, 80), "Sao Paulo", 6),
    ("OUTBACK STEAKHOUSE", "Restaurante", (120, 320), "Sao Paulo", 3),
    ("MC DONALDS", "Restaurante", (25, 70), "Sao Paulo", 6),
    ("STARBUCKS BR", "Cafeteria", (15, 45), "Sao Paulo", 5),
    ("PADARIA BELLA MASSA", "Padaria", (10, 55), "Sao Paulo", 8),
    # Transporte
    ("UBER *TRIP", "Transporte", (10, 60), "Sao Paulo", 16),
    ("99APP *99APP", "Transporte", (9, 50), "Sao Paulo", 8),
    ("POSTO SHELL", "Combustivel", (100, 280), "Sao Paulo", 6),
    ("ESTACIONAMENTO ESTAPAR", "Estacionamento", (12, 45), "Sao Paulo", 4),
    # Assinaturas / Serviços digitais
    ("NETFLIX.COM", "Streaming", (44.90, 44.90), "Sao Paulo", 0),  # mensal fixo
    ("SPOTIFY", "Streaming", (21.90, 21.90), "Sao Paulo", 0),
    ("AMAZON PRIME", "Streaming", (19.90, 19.90), "Sao Paulo", 0),
    ("GOOGLE *YOUTUBEPREMIUM", "Streaming", (28.90, 28.90), "Sao Paulo", 0),
    ("APPLE.COM/BILL", "Servicos Digitais", (9.90, 59.90), "Sao Paulo", 3),
    # Saúde
    ("DROGARIA SAO PAULO", "Farmacia", (20, 180), "Sao Paulo", 7),
    ("DROGASIL", "Farmacia", (15, 150), "Sao Paulo", 5),
    ("SMARTFIT", "Academia", (119.90, 119.90), "Sao Paulo", 0),
    ("CLINICA ODONTO SORRIA", "Saude", (150, 400), "Sao Paulo", 1),
    # Compras
    ("AMAZON BR", "E-commerce", (35, 600), "Sao Paulo", 8),
    ("MERCADOLIVRE*MERCADOPAGO", "E-commerce", (25, 450), "Sao Paulo", 7),
    ("SHOPEE *SHOPEE", "E-commerce", (15, 200), "Sao Paulo", 6),
    ("MAGAZINE LUIZA", "E-commerce", (80, 900), "Sao Paulo", 3),
    ("RENNER", "Vestuario", (60, 350), "Sao Paulo", 4),
    ("C&A MODAS", "Vestuario", (50, 280), "Sao Paulo", 3),
    ("CENTAURO", "Vestuario", (90, 400), "Sao Paulo", 2),
    # Casa
    ("LEROY MERLIN", "Casa e Construcao", (45, 500), "Sao Paulo", 2),
    ("TOK STOK", "Casa e Decoracao", (60, 450), "Sao Paulo", 2),
    ("PETZ", "Pet", (40, 220), "Sao Paulo", 4),
    # Lazer / Viagem
    ("CINEMARK", "Lazer", (30, 90), "Sao Paulo", 3),
    ("INGRESSO.COM", "Lazer", (35, 120), "Sao Paulo", 2),
    ("DECOLAR.COM", "Viagem", (300, 1800), "Sao Paulo", 1),
    ("AIRBNB * HMRSTAY", "Viagem", (250, 1200), "Rio de Janeiro", 1),
    ("BOOKING.COM", "Viagem", (200, 900), "Sao Paulo", 1),
    # Educação
    ("UDEMY", "Educacao", (27.90, 89.90), "Sao Paulo", 2),
    ("ALURA CURSOS", "Educacao", (75, 75), "Sao Paulo", 0),
    ("LIVRARIA CULTURA", "Educacao", (35, 150), "Sao Paulo", 2),
]

SUBSCRIPTIONS = [
    ("NETFLIX.COM", "Streaming", 44.90, 10),
    ("SPOTIFY", "Streaming", 21.90, 5),
    ("AMAZON PRIME", "Streaming", 19.90, 15),
    ("GOOGLE *YOUTUBEPREMIUM", "Streaming", 28.90, 20),
    ("SMARTFIT", "Academia", 119.90, 5),
    ("ALURA CURSOS", "Educacao", 75.00, 8),
]

CARD_HOLDERS = ["JOSUE S SILVA", "JOSUE S SILVA - ADICIONAL"]
PAYMENT_TYPES = ["credito_a_vista", "credito_parcelado"]

START = datetime(2026, 1, 1)
END = datetime(2026, 6, 30)


def rand_datetime(day: datetime, cat: str) -> datetime:
    if cat in ("Delivery", "Restaurante"):
        hour = random.choice([11, 12, 12, 13, 19, 19, 20, 20, 21, 22])
    elif cat in ("Padaria", "Cafeteria"):
        hour = random.choice([7, 8, 8, 9, 10, 16, 17])
    elif cat == "Transporte":
        hour = random.choice([7, 8, 9, 12, 17, 18, 18, 19, 22, 23])
    else:
        hour = random.randint(8, 22)
    return day.replace(hour=hour, minute=random.randint(0, 59), second=random.randint(0, 59))


rows = []
txid = 1000

# 1) Assinaturas mensais recorrentes
for month in range(1, 7):
    for name, cat, value, day in SUBSCRIPTIONS:
        dt = datetime(2026, month, day, random.randint(0, 6), random.randint(0, 59))
        rows.append({
            "id_transacao": f"TX{txid}", "data_hora": dt,
            "estabelecimento": name, "categoria": cat, "valor": value,
            "cidade": "Sao Paulo", "pais": "BR",
            "tipo_pagamento": "credito_a_vista", "parcelas": 1,
            "titular": CARD_HOLDERS[0],
        })
        txid += 1

# 2) Compras variadas
weighted = [m for m in MERCHANTS for _ in range(m[4])]
n_days = (END - START).days + 1
target = 500 - len(rows) - 25  # reserva p/ parceladas e sujeira
for _ in range(target):
    m = random.choice(weighted)
    name, cat, (lo, hi), city, _w = m
    day = START + timedelta(days=random.randint(0, n_days - 1))
    dt = rand_datetime(day, cat)
    value = round(random.uniform(lo, hi), 2)
    holder = random.choices(CARD_HOLDERS, weights=[85, 15])[0]
    rows.append({
        "id_transacao": f"TX{txid}", "data_hora": dt,
        "estabelecimento": name, "categoria": cat, "valor": value,
        "cidade": city, "pais": "BR",
        "tipo_pagamento": "credito_a_vista", "parcelas": 1,
        "titular": holder,
    })
    txid += 1

# 3) Compras parceladas (parcelas aparecem nos meses seguintes)
big_purchases = [
    ("MAGAZINE LUIZA", "E-commerce", 2399.90, 6, datetime(2026, 1, 14)),
    ("DECOLAR.COM", "Viagem", 3240.00, 4, datetime(2026, 2, 3)),
    ("CASAS BAHIA", "E-commerce", 1899.00, 10, datetime(2026, 1, 22)),
    ("TOK STOK", "Casa e Decoracao", 1450.00, 3, datetime(2026, 3, 8)),
    ("CENTAURO", "Vestuario", 899.90, 3, datetime(2026, 4, 12)),
]
for name, cat, total, n_parc, first_dt in big_purchases:
    parc_value = round(total / n_parc, 2)
    for i in range(n_parc):
        dt = first_dt + timedelta(days=30 * i)
        if dt > END:
            break
        rows.append({
            "id_transacao": f"TX{txid}",
            "data_hora": dt.replace(hour=random.randint(9, 21), minute=random.randint(0, 59)),
            "estabelecimento": f"{name} {i+1}/{n_parc}", "categoria": cat,
            "valor": parc_value, "cidade": "Sao Paulo", "pais": "BR",
            "tipo_pagamento": "credito_parcelado", "parcelas": n_parc,
            "titular": CARD_HOLDERS[0],
        })
        txid += 1

# 4) Transações internacionais (viagem em maio)
intl = [
    ("UBER *TRIP BUENOS AIRES", "Transporte", 18.50, "Buenos Aires", "AR"),
    ("RESTAURANTE DON JULIO", "Restaurante", 320.00, "Buenos Aires", "AR"),
    ("CAFE TORTONI", "Cafeteria", 45.80, "Buenos Aires", "AR"),
    ("FARMACITY", "Farmacia", 62.30, "Buenos Aires", "AR"),
    ("MUSEO MALBA", "Lazer", 55.00, "Buenos Aires", "AR"),
]
for name, cat, value, city, country in intl:
    dt = datetime(2026, 5, random.randint(15, 19), random.randint(9, 22), random.randint(0, 59))
    rows.append({
        "id_transacao": f"TX{txid}", "data_hora": dt,
        "estabelecimento": name, "categoria": cat, "valor": value,
        "cidade": city, "pais": country,
        "tipo_pagamento": "credito_a_vista", "parcelas": 1,
        "titular": CARD_HOLDERS[0],
    })
    txid += 1

# 5) Estornos (valores negativos)
refunds = random.sample([r for r in rows if r["categoria"] == "E-commerce" and r["valor"] > 100], 3)
for r in refunds:
    dt = r["data_hora"] + timedelta(days=random.randint(3, 10))
    if dt > END:
        dt = END - timedelta(days=1)
    rows.append({
        "id_transacao": f"TX{txid}", "data_hora": dt,
        "estabelecimento": f"ESTORNO {r['estabelecimento']}", "categoria": r["categoria"],
        "valor": -r["valor"], "cidade": r["cidade"], "pais": r["pais"],
        "tipo_pagamento": r["tipo_pagamento"], "parcelas": 1,
        "titular": r["titular"],
    })
    txid += 1

rows.sort(key=lambda r: r["data_hora"])

# ---------- SUJEIRA PROPOSITAL ----------
final = []
for r in rows:
    final.append(dict(r))

# a) duplicatas exatas (8 linhas duplicadas, mesmo id)
for r in random.sample(final, 8):
    final.append(dict(r))

# b) categoria nula em ~4% das linhas
for r in random.sample(final, int(len(final) * 0.04)):
    r["categoria"] = ""

# c) cidade nula em ~2%
for r in random.sample(final, int(len(final) * 0.02)):
    r["cidade"] = ""

# d) inconsistência de caixa no estabelecimento (~5%)
for r in random.sample(final, int(len(final) * 0.05)):
    r["estabelecimento"] = r["estabelecimento"].lower()

# e) categoria com grafia inconsistente
for r in final:
    if r["categoria"] == "Supermercado" and random.random() < 0.15:
        r["categoria"] = "SUPERMERCADO"
    if r["categoria"] == "Transporte" and random.random() < 0.12:
        r["categoria"] = "transporte "  # espaço extra

final.sort(key=lambda r: r["data_hora"])

# ---------- ESCRITA DO CSV (formatos de data/valor inconsistentes) ----------
with open("extrato_cartao_2026.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id_transacao", "data_hora", "estabelecimento", "categoria",
                "valor", "cidade", "pais", "tipo_pagamento", "parcelas", "titular"])
    for r in final:
        dt = r["data_hora"]
        roll = random.random()
        if roll < 0.85:
            dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        elif roll < 0.95:
            dt_str = dt.strftime("%d/%m/%Y %H:%M")          # formato BR
        else:
            dt_str = dt.strftime("%Y-%m-%dT%H:%M:%S")        # ISO com T
        v = r["valor"]
        roll_v = random.random()
        if roll_v < 0.88:
            v_str = f"{v:.2f}"
        elif roll_v < 0.96:
            v_str = f"{v:.2f}".replace(".", ",")             # decimal BR
        else:
            v_str = f"R$ {v:.2f}"                            # com prefixo
        w.writerow([r["id_transacao"], dt_str, r["estabelecimento"], r["categoria"],
                    v_str, r["cidade"], r["pais"], r["tipo_pagamento"], r["parcelas"], r["titular"]])

print(f"Geradas {len(final)} linhas em extrato_cartao_2026.csv")
