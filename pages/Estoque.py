import streamlit as st
from database import conectar, inicializar_banco, menu_lateral

st.set_page_config(page_title="Tigela Roxa - Estoque", layout="wide")
inicializar_banco()
menu_lateral()

st.title("Estoque")

conn = conectar()
itens = conn.execute("SELECT id, item, categoria, quantidade, minimo, unidade FROM estoque").fetchall()

st.caption(f"{len(itens)} itens cadastrados")

def contar(cat):
    sub = [i for i in itens if i["categoria"] == cat]
    return len(sub), sum(1 for i in sub if i["quantidade"] < i["minimo"])

c1, c2, c3, _ = st.columns([1.0, 1.0, 1.0, 0.8])
for col, nome, cat in [(c1, "Ingredientes", "Ingrediente"), (c2, "Embalagens", "Embalagem"), (c3, "Complementos", "Complemento")]:
    tot, crit = contar(cat)
    col.container(border=True).metric(nome, tot, f"{crit} críticos", delta_color="inverse")

st.write("")
with st.container(border=True):
    if "filtro_est" not in st.session_state:
        st.session_state.filtro_est = "TODOS"

    b1, b2, b3, b4 = st.columns(4)
    if b1.button("TODOS", use_container_width=True): st.session_state.filtro_est = "TODOS"
    if b2.button("INGREDIENTES", use_container_width=True): st.session_state.filtro_est = "Ingrediente"
    if b3.button("EMBALAGENS", use_container_width=True): st.session_state.filtro_est = "Embalagem"
    if b4.button("COMPLEMENTOS", use_container_width=True): st.session_state.filtro_est = "Complemento"

    st.divider()
    h1, h2, h3, h4, h5, h6 = st.columns([2.0, 1.5, 1.0, 1.0, 1.0, 1.0])
    h1.markdown("**Item**")
    h2.markdown("**Categoria**")
    h3.markdown("**Quant.**")
    h4.markdown("**Min.**")
    h5.markdown("**STATUS**")
    h6.markdown("**Ajuste**")

    filtrados = [i for i in itens if st.session_state.filtro_est == "TODOS" or i["categoria"] == st.session_state.filtro_est]

    for i in filtrados:
        critico = i["quantidade"] < i["minimo"]
        cor = "red" if critico else "green"
        with st.container(border=True):
            col1, col2, col3, col4, col5, col6 = st.columns([2.0, 1.5, 1.0, 1.0, 1.0, 1.0])
            col1.write(i["item"])
            col2.write(i["categoria"])
            col3.write(f"{i['quantidade']:g}{i['unidade']}")
            col4.write(f"{i['minimo']:g}{i['unidade']}")
            col5.markdown(f":{cor}[**{'Critico' if critico else 'OK'}**]")
            if col6.button("+1", key=f"add_{i['id']}"):
                conn.execute("UPDATE estoque SET quantidade = quantidade + 1 WHERE id = ?", (i["id"],))
                conn.commit()
                st.rerun()
conn.close()
