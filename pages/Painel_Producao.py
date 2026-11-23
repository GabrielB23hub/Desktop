import streamlit as st
from database import conectar, inicializar_banco, menu_lateral

st.set_page_config(page_title="Tigela Roxa - Produção", layout="wide")
inicializar_banco()
menu_lateral()

st.title("PAINEL DE PRODUÇÃO")

conn = conectar()
fila = conn.execute("SELECT id, codigo, cliente, item, adicionais, status FROM pedidos WHERE status IN ('Pendente', 'Preparando')").fetchall()

st.caption(f"{len(fila)} pedidos")

c1, c2, _ = st.columns([1.0, 1.0, 2.0])
c1.container(border=True).metric("Pedidos pendente", sum(1 for p in fila if p["status"] == "Pendente"))
c2.container(border=True).metric("Pedidos em andamento", sum(1 for p in fila if p["status"] == "Preparando"))

st.write("")
with st.container(border=True):
    cols = st.columns(2)
    for idx, p in enumerate(fila):
        with cols[idx % 2]:
            with st.container(border=True):
                t1, t2 = st.columns(2)
                t1.markdown(f"**{p['codigo']}**")
                cor = "blue" if p["status"] == "Preparando" else "orange"
                t2.markdown(f"<div style='text-align:right'>:{cor}[**{p['status']}**]</div>", unsafe_allow_html=True)

                st.subheader(p["cliente"])
                a1, a2 = st.columns(2)
                a1.info(p["item"])
                a2.info(p["adicionais"])

                if p["status"] == "Pendente":
                    if st.button("Iniciar sessão", key=f"ini_{p['id']}", use_container_width=True):
                        conn.execute("UPDATE pedidos SET status = 'Preparando' WHERE id = ?", (p["id"],))
                        conn.commit()
                        st.rerun()
                else:
                    if st.button("Marcar como pronto", key=f"ok_{p['id']}", type="primary", use_container_width=True):
                        conn.execute("UPDATE pedidos SET status = 'Pronto' WHERE id = ?", (p["id"],))
                        conn.commit()
                        st.rerun()
conn.close()
