# 💰 Edu - Educador Financeiro Inteligente

Assistente virtual construido para o Lab "Construa Seu Assistente Virtual Com
Inteligencia Artificial". O Edu ajuda uma pessoa a entender conceitos de
financas pessoais e a organizar seus gastos, usando os proprios dados do
cliente como exemplo, **sem nunca recomendar investimentos especificos**.

## Estrutura do projeto

```
assistente-virtual-ia/
  README.md
  data/                     -> base de conhecimento (mockada)
  docs/                     -> documentacao dos 6 passos do desafio
  src/                      -> aplicacao (Streamlit) e logica do agente
```

## Os 6 passos do desafio

| Passo | Onde encontrar |
|---|---|
| 1. Documentacao do agente | `docs/01-documentacao-agente.md` |
| 2. Base de conhecimento | `docs/02-base-conhecimento.md` + pasta `data/` |
| 3. Prompts | `docs/03-prompts.md` + `src/agent.py` (`SYSTEM_PROMPT`) |
| 4. Aplicacao funcional | `src/app.py` + `src/agent.py` |
| 5. Avaliacao e metricas | `docs/04-metricas.md` + `src/avaliacao.py` |
| 6. Pitch | `docs/05-pitch.md` |

## Como rodar

```bash
cd src
pip install -r requirements.txt
streamlit run app.py
```

A aplicacao funciona em **dois modos**, escolhidos automaticamente:

- **Modo fallback (padrao, sem custo):** se a variavel de ambiente
  `ANTHROPIC_API_KEY` nao estiver configurada, o agente responde usando um
  motor de regras (`fallback_response` em `src/agent.py`) que cobre os
  cenarios e edge cases documentados. Isso garante que o app seja testavel
  por qualquer pessoa, sem precisar de chave de API.
- **Modo com LLM real:** configurando `ANTHROPIC_API_KEY` (e opcionalmente
  `ANTHROPIC_MODEL`), o agente passa a usar a API da Anthropic, sempre com o
  mesmo `SYSTEM_PROMPT` e a mesma base de conhecimento como contexto.

```bash
export ANTHROPIC_API_KEY="sua_chave_aqui"
streamlit run app.py
```

## Rodando a avaliacao

```bash
cd src
python3 avaliacao.py
```

O script roda 8 casos de teste (conceitos, uso de dados do cliente, tentativa
de recomendacao de investimento, pergunta fora de escopo e pedido de dado
sensivel), salva o detalhe em `data/resultados_avaliacao.csv` e imprime um
resumo com as taxas de acerto. Resultados atuais em `docs/04-metricas.md`.
