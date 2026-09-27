# Pitch (roteiro de ~3 minutos)

## 1. Problema (30s)
Muita gente adia decisoes financeiras simples - montar uma reserva de
emergencia, entender onde o dinheiro esta indo, entender o que e CDI ou
Selic - porque o vocabulario financeiro parece complicado e as vezes a unica
ajuda disponivel vem junto com uma tentativa de venda de produto.

## 2. Solucao (60s)
O Edu e um educador financeiro virtual: ele conversa com a pessoa, usa os
proprios dados dela (gastos do mes, perfil de risco) como exemplo pratico, e
explica conceitos financeiros em linguagem simples - sem nunca recomendar um
investimento especifico. Isso tira o agente do papel de "vendedor" e coloca
no papel de professor, o que aumenta a confianca do usuario.

Na pratica: a pessoa pergunta "onde estou gastando mais?" e o Edu responde
com os numeros reais dela; pergunta "o que e CDI?" e recebe uma explicacao
clara; e se tentar pedir uma recomendacao de investimento, o Edu explica o
funcionamento do produto mas deixa a decisao com a pessoa.

## 3. Como funciona (40s)
A aplicacao roda em Streamlit e usa uma base de conhecimento simples (CSV/JSON
com transacoes, perfil e produtos). O motor de resposta funciona em dois
modos: com uma API de IA generativa configurada, ou em um modo local baseado
em regras que garante que os comportamentos de seguranca (nunca recomendar,
nunca vazar dado sensivel, nunca inventar informacao) funcionem mesmo sem
custo de API - o que tambem tornou possivel testar e medir a qualidade do
agente de forma automatizada.

## 4. Por que e inovador / valor (30s)
Diferente de um chatbot generico, o Edu combina tres coisas: personalizacao
com dados reais do cliente, guarda-corpos claros contra recomendacao e
alucinacao, e um processo de avaliacao mensuravel (100% de acerto nos 8 casos
de teste cobrindo seguranca e uso de dados). E um primeiro passo simples para
mostrar como IA generativa pode educar, em vez de apenas responder.
