import streamlit as st
from database import inicializar_banco

st.set_page_config(page_title="Tigela Roxa", layout="centered", initial_sidebar_state="collapsed")
inicializar_banco()

st.markdown("<br><br><br>", unsafe_allow_html=True)
_, col_centro, _ = st.columns([1.0, 2.0, 1.0])

with col_centro:
    st.markdown(
        """
        <div style="background-color:#5B1E6B; padding:50px 20px; border-radius:16px; text-align:center; color:white;">
            <h1 style="margin:0; font-size:42px;">🍨</h1>
            <h2 style="margin:10px 0 0 0;">TIGELA ROXA</h2>
            <p style="opacity:0.85;">Gestão Inteligente para Açaiterias</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write("")
    if st.button("INICIAR", type="primary", use_container_width=True):
        st.switch_page("pages/Dashboard.py")
