import streamlit as st

if "QWEN_API_KEY" not in st.session_state:
    st.session_state["QWEN_API_KEY"] = ""

st.set_page_config(page_title="Qwen Settings", layout="wide")

st.title("Qwen大模型api_key设置")

qwen_api_key = st.text_input("API Key", value=st.session_state["QWEN_API_KEY"], max_chars=None, key=None,
                             type="password")

saved = st.button("保存")

if saved:
    st.session_state["QWEN_API_KEY"] = qwen_api_key