import streamlit as st
from openai import OpenAI

# Crear cliente de OpenAI con clave desde secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Modelo personalizado fine-tuned
MODEL_ID = "ft:gpt-3.5-turbo-0125:tu-modelo-personalizado"

st.set_page_config(page_title="Coach de Aviación", page_icon="🛬")
st.title("🛬 Coach de Competencias para Pilotos")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Actúa como un capacitador experto en competencias conductuales críticas para la aviación comercial, usando CBTA y EBT."}
    ]

for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Escribe tu pregunta como piloto...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=st.session_state.messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
