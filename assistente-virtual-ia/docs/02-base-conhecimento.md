# Base de Conhecimento

Os dados ficam na pasta `data/` e sao carregados por `src/agent.py`
(funcao `build_context`), que monta um resumo textual usado como contexto
para o agente responder.

| Arquivo | Formato | Descricao |
|---|---|---|
| `transacoes.csv` | CSV | Transacoes do cliente no mes, com categoria e valor |
| `historico_atendimento.csv` | CSV | Atendimentos anteriores (para referencia de contexto) |
| `perfil_investidor.json` | JSON | Perfil de risco, objetivo e nivel de conhecimento do cliente |
| `produtos_financeiros.json` | JSON | Produtos financeiros disponiveis, com descricao e risco (apenas para explicar, nunca para recomendar) |

## Como o contexto e usado

1. `transacoes.csv` e agregado por categoria (`gastos_por_categoria`) para
   responder perguntas do tipo "onde estou gastando mais?" com numeros reais.
2. `perfil_investidor.json` personaliza o tom e o nivel de profundidade das
   explicacoes (ex: cliente iniciante recebe explicacoes mais basicas).
3. `produtos_financeiros.json` fornece as descricoes usadas quando o cliente
   pergunta sobre um tipo de investimento, sem que o agente indique qual
   escolher.
4. `historico_atendimento.csv` fica disponivel como referencia de contexto
   (proximas versoes podem usa-lo para evitar repetir explicacoes ja dadas).

A base pode ser expandida facilmente: basta adicionar novas linhas/objetos
nos arquivos existentes, sem alterar o codigo do agente.
