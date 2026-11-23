import pandas as pd
import streamlit as st
from database import conectar, inicializar_banco, menu_lateral

st.set_page_config(page_title="Tigela Roxa - Relatório", layout="wide")
inicializar_banco()
menu_lateral()

st.title("Relatorio")
st.caption("resumo do dia")

conn = conectar()
pedidos = conn.execute("SELECT status, valor FROM pedidos").fetchall()
conn.close()

tot_ped = len(pedidos)
entregues = sum(1 for p in pedidos if p["status"] in ("Pronto", "Entregue"))
rec_dia = sum(p["valor"] for p in pedidos if p["status"] != "Cancelado")
rec_mes = rec_dia + 1000.0

c1, c2, c3, c4 = st.columns(4)
c1.container(border=True).metric("Total de pedidos", tot_ped)
c2.container(border=True).metric("Pedidos entregues", entregues)
c3.container(border=True).metric("Receita diaria", f"R$ {rec_dia:.2f}")
c4.container(border=True).metric("Receita mensal", f"R$ {rec_mes:.2f}")

st.write("")
df_dias = pd.DataFrame({
    "Dias": [f"Dia {i:02d}" for i in range(1, 21)],
    "Dinheiro ($)": [45, 62, 88, 50, 40, 95, 55, 38, 68, 110, 42, 75, 58, 92, 48, 65, 105, 35, 72, rec_dia]
})

with st.container(border=True):
    st.subheader("Receita mensal")
    st.bar_chart(df_dias, x="Dias", y="Dinheiro ($)", color="#5B1E6B", use_container_width=True)
