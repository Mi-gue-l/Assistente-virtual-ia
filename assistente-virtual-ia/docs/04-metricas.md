# Avaliacao e Metricas

## Metodologia

O script `src/avaliacao.py` roda 8 casos de teste cobrindo os principais
cenarios e edge cases descritos em `docs/03-prompts.md`, e verifica por
palavras-chave esperadas/proibidas se a resposta do agente segue as regras.
Os casos cobrem 5 categorias:

| Categoria | O que testa |
|---|---|
| `conceito` | O agente explica corretamente um conceito financeiro |
| `dados_cliente` | O agente usa dados reais das transacoes do cliente |
| `recomendacao_bloqueada` | O agente recusa recomendar investimento especifico |
| `fora_de_escopo` | O agente recusa responder assunto nao financeiro |
| `dado_sensivel` | O agente recusa compartilhar dados sensiveis/de terceiros |

## Metricas Definidas

- **Taxa de seguranca / anti-alucinacao:** % de casos de `recomendacao_bloqueada`,
  `fora_de_escopo` e `dado_sensivel` em que o agente se comportou corretamente
  (recusou, sem inventar informacao).
- **Taxa de uso correto de dados do cliente:** % de perguntas sobre gastos em
  que a resposta usou numeros reais vindos de `transacoes.csv`.
- **Taxa de cobertura de conceitos:** % de perguntas conceituais respondidas
  com a explicacao correta.

## Resultados (execucao atual, modo fallback)

```
total_casos: 8
aprovados: 8
taxa_geral: 100.0%
taxa_seguranca_anti_alucinacao: 100.0%
taxa_uso_correto_dados_cliente: 100.0%
taxa_cobertura_conceitos: 100.0%
```

O detalhe caso a caso fica salvo em `data/resultados_avaliacao.csv` toda vez
que o script e executado.

## Observacao importante

Esses numeros refletem o **modo fallback** (motor de regras), que e
deterministico. Ao rodar com uma API real configurada (`ANTHROPIC_API_KEY`),
os mesmos 8 casos podem ser reaproveitados como um "teste de regressao": basta
adaptar `fallback_response(...)` na chamada do script para `get_response(...)`
e comparar se o comportamento de seguranca se mantem com o LLM real. Isso e
importante porque, durante os testes manuais mencionados em
`docs/03-prompts.md`, diferentes LLMs tiveram taxas de seguranca diferentes
no mesmo edge case (pergunta fora de escopo).

## Proximos passos de avaliacao (nao implementados nesta versao)

- Avaliacao humana de clareza/didatica das respostas (nota de 1 a 5)
- Testes com o modo API real, comparando custo x qualidade entre modelos
- Ampliar o conjunto de casos de teste conforme novos edge cases aparecerem
