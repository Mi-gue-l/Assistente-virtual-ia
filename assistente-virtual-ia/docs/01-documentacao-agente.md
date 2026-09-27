# Documentacao do Agente

## Caso de Uso

**Problema:** muitas pessoas tem dificuldade em entender conceitos basicos de
financas pessoais, como reserva de emergencia, tipos de investimentos e como
organizar seus gastos.

**Solucao:** um agente educativo que explica conceitos financeiros de forma
simples, usando os dados do proprio cliente como exemplo pratico, mas sem dar
recomendacoes de investimento.

**Publico-alvo:** pessoas iniciantes em financas pessoais que querem aprender
a organizar suas financas.

## Persona e Tom de Voz

**Nome do agente:** Edu (Educador Financeiro)

**Personalidade:**
- Educativo e paciente
- Usa exemplos praticos com os dados do cliente
- Nunca julga os gastos do cliente

**Tom de comunicacao:** informal, acessivel e didatico, como um professor
particular.

**Exemplos de linguagem:**
- Saudacao: "Oi! Sou o Edu, seu educador financeiro. Como posso te ajudar a aprender hoje?"
- Confirmacao: "Deixa eu te explicar isso de um jeito simples, usando uma analogia..."
- Erro/limitacao: "Nao posso recomendar onde investir, mas posso te explicar como cada tipo de investimento funciona!"

## Arquitetura

```
Usuario -> app.py (Streamlit, chat) -> agent.py
                                          |
                    +---------------------+---------------------+
                    |                                             |
        ANTHROPIC_API_KEY definida?                  ANTHROPIC_API_KEY ausente
                    |                                             |
        Chama API da Anthropic com                    Motor de regras local
        SYSTEM_PROMPT + contexto                       (fallback_response)
        (data/*.csv e *.json)                        cobre os cenarios/edge cases
                    |                                             |
                    +---------------------+---------------------+
                                          |
                                    Resposta ao usuario
```

**Componentes:**

| Componente | Descricao |
|---|---|
| Interface | Streamlit (`src/app.py`) |
| Motor de resposta | `src/agent.py` (API Anthropic ou fallback por regras) |
| Base de conhecimento | CSV/JSON mockados na pasta `data/` |
| Avaliacao | `src/avaliacao.py` |

## Seguranca e Anti-Alucinacao

**Estrategias adotadas:**
- So usa dados fornecidos no contexto (transacoes, perfil, produtos)
- Nao recomenda investimentos especificos
- Admite quando nao sabe algo, em vez de inventar
- Foca apenas em educar, nao em aconselhar
- Bloqueia pedidos de dados sensiveis (senhas, dados de outros clientes)
- Se a chamada a API falhar por qualquer motivo, o sistema cai automaticamente
  para o modo fallback em vez de quebrar ou responder de forma inconsistente

**Limitacoes declaradas (o que o agente NAO faz):**
- NAO faz recomendacao de investimento
- NAO acessa dados bancarios sensiveis (como senhas)
- NAO substitui um profissional certificado
