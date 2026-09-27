import streamlit as st
from agent import get_response, load_perfil, build_context

st.set_page_config(page_title="Edu - Educador Financeiro", page_icon="💰")

st.title("💰 Edu - Educador Financeiro Inteligente")
st.caption("Assistente virtual que ensina financas pessoais com base nos seus dados. "
           "Nao recomenda investimentos especificos.")

with st.sidebar:
    st.subheader("Perfil do cliente")
    perfil = load_perfil()
    st.write(f"**Perfil de risco:** {perfil['perfil_risco']}")
    st.write(f"**Reserva de emergencia:** {'sim' if perfil['possui_reserva_emergencia'] else 'nao'}")
    st.write(f"**Objetivo:** {perfil['objetivo_principal']}")
    st.divider()
    st.caption(
        "Modo: **API real** (ANTHROPIC_API_KEY configurada)" if __import__("os").getenv("ANTHROPIC_API_KEY")
        else "Modo: **fallback local** (baseado em regras, sem custo de API)"
    )
    with st.expander("Ver base de conhecimento usada"):
        contexto, _, _ = build_context()
        st.text(contexto)

if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {"role": "assistant", "content": "Oi! Sou o Edu, seu educador financeiro. Como posso te ajudar a aprender hoje?"}
    ]

for m in st.session_state.mensagens:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

pergunta = st.chat_input("Pergunte algo sobre suas financas...")
if pergunta:
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    resposta = get_response(pergunta)

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
    with st.chat_message("assistant"):
        st.markdown(resposta)
