"""
Agente "Edu" - Educador Financeiro Inteligente.

Este modulo concentra toda a logica do agente:
- Carregamento da base de conhecimento (data/)
- Guarda-corpos (nao recomendar investimentos, nao vazar dados sensiveis, etc)
- Geracao de resposta: usa a API da Anthropic se ANTHROPIC_API_KEY estiver
  configurada; caso contrario usa um modo "fallback" baseado em regras, que
  garante que a aplicacao funcione (e seja testavel) sem precisar de chave.
"""

import os
import json
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

SYSTEM_PROMPT = """Voce e o Edu, um educador financeiro amigavel e didatico.

OBJETIVO:
Ensinar conceitos de financas pessoais de forma simples, usando os dados do
cliente como exemplos praticos.

REGRAS:
- NUNCA recomende investimentos especificos, apenas explique como funcionam;
- JAMAIS responda a perguntas fora do tema ensino de financas pessoais.
  Quando ocorrer, responda lembrando o seu papel de educador financeiro;
- Use os dados fornecidos para dar exemplos personalizados;
- Linguagem simples, como se explicasse para um amigo;
- Se nao souber algo, admita: "Nao tenho essa informacao, mas posso explicar...";
- Sempre pergunte se o cliente entendeu;
- Responda de forma sucinta e direta, com no maximo 3 paragrafos.
"""

# ---------------------------------------------------------------------------
# Carregamento da base de conhecimento
# ---------------------------------------------------------------------------

def load_transacoes():
    path = DATA_DIR / "transacoes.csv"
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_historico():
    path = DATA_DIR / "historico_atendimento.csv"
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_perfil():
    path = DATA_DIR / "perfil_investidor.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_produtos():
    path = DATA_DIR / "produtos_financeiros.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def gastos_por_categoria(transacoes):
    totais = {}
    for t in transacoes:
        cat = t["categoria"]
        totais[cat] = totais.get(cat, 0) + float(t["valor"])
    return dict(sorted(totais.items(), key=lambda kv: kv[1], reverse=True))


def build_context():
    """Monta um resumo textual da base de conhecimento para dar ao modelo."""
    transacoes = load_transacoes()
    perfil = load_perfil()
    produtos = load_produtos()
    totais = gastos_por_categoria(transacoes)
    total_geral = sum(totais.values())

    linhas_gastos = "\n".join(
        f"- {cat}: R$ {valor:.2f} ({valor / total_geral * 100:.0f}%)"
        for cat, valor in totais.items()
    )
    linhas_produtos = "\n".join(
        f"- {p['nome']} ({p['tipo']}, risco {p['risco']}): {p['descricao']}"
        for p in produtos
    )

    contexto = f"""PERFIL DO CLIENTE:
- Perfil de risco: {perfil['perfil_risco']}
- Possui reserva de emergencia: {'sim' if perfil['possui_reserva_emergencia'] else 'nao'}
- Objetivo: {perfil['objetivo_principal']}
- Nivel de conhecimento financeiro: {perfil['conhecimento_financeiro']}

GASTOS DO MES (por categoria, do maior para o menor):
{linhas_gastos}
Total do mes: R$ {total_geral:.2f}

PRODUTOS FINANCEIROS DISPONIVEIS PARA EXPLICAR (nao recomendar):
{linhas_produtos}
"""
    return contexto, totais, total_geral


# ---------------------------------------------------------------------------
# Guarda-corpos / deteccao de intencao
# ---------------------------------------------------------------------------

TEMAS_FORA_DE_ESCOPO_EXEMPLOS = [
    "previsao do tempo", "clima", "futebol", "receita de bolo", "filme",
    "traducao", "piada", "horoscopo", "noticia",
]

PALAVRAS_SENSIVEIS = ["senha", "cpf de outro", "dados de outro cliente", "cartao de credito"]

PALAVRAS_RECOMENDACAO = [
    "devo investir", "onde investir", "qual investimento", "me recomenda",
    "melhor investimento", "o que voce recomenda", "vale a pena investir",
]

CONCEITOS = {
    "cdi": "O CDI e uma taxa de referencia usada pelos bancos. Quando um investimento "
           "rende '100% do CDI', significa que ele acompanha essa taxa. O CDI costuma "
           "ficar bem proximo da Selic.",
    "selic": "A Selic e a taxa basica de juros da economia, definida pelo Banco Central. "
             "Ela influencia o rendimento da poupanca e de varios investimentos de renda fixa.",
    "reserva de emergencia": "A reserva de emergencia e um valor guardado para imprevistos "
             "(perda de renda, emergencias medicas etc). O ideal e que fique em um "
             "investimento de baixo risco e alta liquidez, como o Tesouro Selic.",
    "renda fixa": "Sao investimentos em que as regras de rendimento sao conhecidas desde "
             "o inicio (ex: 100% do CDI). Costumam ter risco menor que a renda variavel.",
    "renda variavel": "Sao investimentos cujo valor varia conforme o mercado, como acoes "
             "e fundos imobiliarios. O potencial de ganho e maior, mas o risco tambem.",
    "acoes": "Acoes representam pedacos de uma empresa: quem compra vira socio. O preco "
             "varia bastante conforme o desempenho da empresa e o mercado.",
    "juros compostos": "E quando o rendimento de um periodo passa a gerar rendimento nos "
             "periodos seguintes, fazendo o dinheiro crescer de forma acelerada com o tempo.",
}


def _contains_any(texto, termos):
    texto = texto.lower()
    return any(t in texto for t in termos)


# ---------------------------------------------------------------------------
# Geracao de resposta - modo fallback (sem API, deterministico e testavel)
# ---------------------------------------------------------------------------

def fallback_response(pergunta: str) -> str:
    p = pergunta.lower().strip()

    # 1. Dados sensiveis / fora de politica
    if _contains_any(p, PALAVRAS_SENSIVEIS):
        return ("Nao tenho acesso a senhas ou a dados de outros clientes, e nao posso "
                "compartilhar esse tipo de informacao. Posso ajudar com suas proprias financas?")

    # 2. Pedido de recomendacao de investimento especifico
    if _contains_any(p, PALAVRAS_RECOMENDACAO):
        return ("Nao posso te dizer onde investir, mas posso explicar como cada tipo de "
                "investimento funciona para te ajudar a decidir com mais confianca! "
                "Quer que eu explique renda fixa ou renda variavel?")

    # 3. Pergunta sobre os proprios gastos
    if any(termo in p for termo in ["onde estou gastando", "meus gastos", "gastei", "categoria de gasto", "meu maior gasto"]):
        _, totais, total_geral = build_context()
        top = list(totais.items())[:2]
        top_txt = " e ".join(f"{cat} (R$ {valor:.2f})" for cat, valor in top)
        pct = sum(v for _, v in top) / total_geral * 100
        return (f"Olhando suas transacoes do mes, seus maiores gastos sao {top_txt}. "
                f"Juntas, essas categorias representam cerca de {pct:.0f}% do total. "
                "Quer que eu explique algumas estrategias simples de organizacao financeira?")

    # 4. Conceitos financeiros conhecidos
    for termo, explicacao in CONCEITOS.items():
        if termo in p:
            return f"{explicacao} Ficou claro ou quer que eu detalhe mais algum ponto?"

    # 5. Fora do escopo (tema nao financeiro)
    if _contains_any(p, TEMAS_FORA_DE_ESCOPO_EXEMPLOS):
        return ("Sou especializado em educacao financeira e nao tenho informacoes sobre "
                "esse assunto. Posso ajudar com algo relacionado as suas financas?")

    # 6. Fallback generico - admite limitacao ao inves de inventar
    return ("Nao tenho essa informacao especifica, mas posso explicar conceitos como CDI, "
            "Selic, reserva de emergencia, renda fixa e renda variavel, ou te ajudar a "
            "entender seus gastos do mes. Sobre qual desses temas voce quer conversar?")


# ---------------------------------------------------------------------------
# Geracao de resposta - modo real (Anthropic API), com fallback automatico
# ---------------------------------------------------------------------------

def get_response(pergunta: str, historico_mensagens=None) -> str:
    """
    Retorna a resposta do Edu.
    Usa a API da Anthropic se ANTHROPIC_API_KEY estiver definida no ambiente;
    caso contrario (ou se a chamada falhar), usa o modo fallback baseado em regras.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return fallback_response(pergunta)

    try:
        import anthropic  # import tardio: so precisa estar instalado se for usar API real

        contexto, _, _ = build_context()
        client = anthropic.Anthropic(api_key=api_key)

        mensagens = (historico_mensagens or []) + [{"role": "user", "content": pergunta}]

        resposta = client.messages.create(
            # ajuste o nome do modelo conforme o disponivel na sua conta/API
            model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
            max_tokens=500,
            system=SYSTEM_PROMPT + "\n\nBASE DE CONHECIMENTO:\n" + contexto,
            messages=mensagens,
        )
        return "".join(block.text for block in resposta.content if block.type == "text")
    except Exception as e:
        # Nunca deixa a aplicacao quebrar: cai para o modo fallback e avisa no console
        print(f"[aviso] Falha ao chamar a API da Anthropic, usando modo fallback: {e}")
        return fallback_response(pergunta)
