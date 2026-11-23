import streamlit as st
from database import conectar, inicializar_banco, menu_lateral

st.set_page_config(page_title="Tigela Roxa - Dashboard", layout="wide")
inicializar_banco()
menu_lateral()

st.title("Pagina Inicial")

conn = conectar()
pedidos = conn.execute("SELECT cliente, status, valor FROM pedidos ORDER BY id DESC").fetchall()
estoque_baixo = conn.execute("SELECT item, quantidade, minimo, unidade FROM estoque WHERE quantidade < minimo").fetchall()
conn.close()

total_hoje = len(pedidos)
entregues = sum(1 for p in pedidos if p["status"] in ("Pronto", "Entregue"))
receita_dia = sum(p["valor"] for p in pedidos if p["status"] != "Cancelado")

c1, c2, c3, c4 = st.columns(4)
c1.container(border=True).metric("Pedidos hoje", total_hoje, f"{entregues} entregues/prontos")
c2.container(border=True).metric("Receita do dia", f"R$ {receita_dia:.2f}")
c3.container(border=True).metric("Receita mês", f"R$ {receita_dia + 1000:.2f}")
c4.container(border=True).metric("Estoque baixo", len(estoque_baixo), "itens abaixo do mínimo", delta_color="inverse")

st.write("")
col_esq, col_dir = st.columns(2)

with col_esq:
    with st.container(border=True):
        st.subheader("Pedidos recentes")
        cores = {"Pendente": "orange", "Preparando": "blue", "Pronto": "green", "Entregue": "gray", "Cancelado": "red"}
        for p in pedidos[:6]:
            cor = cores.get(p["status"], "gray")
            a, b = st.columns(2)
            a.write(f"**{p['cliente']}**")
            b.markdown(f":{cor}[**{p['status']}**] — R$ {p['valor']:.2f}")

with col_dir:
    with st.container(border=True):
        st.subheader("Estoque baixo")
        for item in estoque_baixo:
            with st.container(border=True):
                st.markdown(f"**{item['item']}** — :red[{item['quantidade']:g}{item['unidade']} / min. {item['minimo']:g}{item['unidade']}]")
