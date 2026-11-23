import random
from datetime import datetime
import streamlit as st
from database import conectar, inicializar_banco, menu_lateral

st.set_page_config(page_title="Tigela Roxa - Pedidos", layout="wide")
inicializar_banco()
menu_lateral()

st.title("Gerenciar Pedidos")

with st.expander("➕ Novo Pedido"):
    with st.form("form_novo_pedido", clear_on_submit=True):
        f1, f2, f3 = st.columns(3)
        cli = f1.text_input("Nome do Cliente")
        tigela = f2.selectbox("Tigela", ["Tigela de açaí 300ml", "Tigela de açaí 500ml", "Tigela de açaí 700ml"])
        adds = f3.multiselect("Adicionais", ["Granola", "Banana", "Morango", "Leite Ninho", "Leite Condensado", "Nutella"])
        if st.form_submit_button("Registrar Pedido", type="primary") and cli:
            precos = {"Tigela de açaí 300ml": 16.0, "Tigela de açaí 500ml": 22.0, "Tigela de açaí 700ml": 28.0}
            valor = precos[tigela] + (len(adds) * 2.5)
            cod = f"#{random.randint(1000, 9999)}"
            conn = conectar()
            conn.execute(
                "INSERT INTO pedidos (codigo, cliente, item, adicionais, qtd_itens, valor, status, data_hora) VALUES (?, ?, ?, ?, ?, ?, 'Pendente', ?)",
                (cod, cli, tigela, ", ".join(adds) if adds else "Puro", 1 + len(adds), valor, datetime.now().strftime("%d/%m %H:%M"))
            )
            conn.commit()
            conn.close()
            st.rerun()

conn = conectar()
pedidos = conn.execute("SELECT codigo, cliente, data_hora, qtd_itens, status, valor FROM pedidos ORDER BY id DESC").fetchall()
conn.close()

st.caption(f"{len(pedidos)} pedidos totais")

c1, c2, c3, c4 = st.columns(4)
c1.container(border=True).metric("Pedidos pendente", sum(1 for p in pedidos if p["status"] == "Pendente"))
c2.container(border=True).metric("Pedidos em andamento", sum(1 for p in pedidos if p["status"] == "Preparando"))
c3.container(border=True).metric("Produção diária", f"R$ {sum(p['valor'] for p in pedidos if p['status'] != 'Cancelado'):.2f}")
c4.container(border=True).metric("Pedidos mensais", f"R$ {sum(p['valor'] for p in pedidos if p['status'] != 'Cancelado') + 1000:.2f}")

st.write("")
col_busca, col_filtros = st.columns([1.2, 1.0])
busca = col_busca.text_input("Buscar", placeholder="Buscar por cliente ...", label_visibility="collapsed")

if "filtro_ped" not in st.session_state:
    st.session_state.filtro_ped = "Todos"

with col_filtros:
    r1 = st.columns(3)
    for col, label in zip(r1, ["Todos", "Pronto", "Entregue"]):
        if col.button(label, use_container_width=True):
            st.session_state.filtro_ped = label
    r2 = st.columns(3)
    for col, label in zip(r2, ["Pendente", "Preparando", "Cancelado"]):
        if col.button(label, use_container_width=True):
            st.session_state.filtro_ped = label

filtrados = [
    p for p in pedidos
    if (st.session_state.filtro_ped == "Todos" or p["status"] == st.session_state.filtro_ped)
    and busca.lower() in p["cliente"].lower()
]

cores = {"Pendente": "orange", "Preparando": "blue", "Pronto": "green", "Entregue": "gray", "Cancelado": "red"}

with st.container(border=True):
    st.subheader("Pedidos recentes")
    st.caption(f"{len(filtrados)} pedidos listados")
    for p in filtrados:
        cor = cores.get(p["status"], "gray")
        esq, dir = st.columns([3.0, 1.0])
        esq.markdown(f"**{p['cliente']} {p['codigo']}** \n<small>{p['data_hora']} &nbsp;&nbsp; itens: {p['qtd_itens']}</small>", unsafe_allow_html=True)
        dir.markdown(f":{cor}[**{p['status']}**] — **R$ {p['valor']:.2f}**")
        st.divider()
