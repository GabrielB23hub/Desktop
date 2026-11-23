import sqlite3
from datetime import datetime

DB_NAME = "tigela_roxa.db"

def conectar():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def menu_lateral():
    import streamlit as st
    conn = conectar()
    row = conn.execute("SELECT nome_loja FROM config_loja WHERE id = 1").fetchone()
    nome_loja = row["nome_loja"] if row else "Tigela Roxa"

    with st.sidebar:
        st.markdown(f"### 🍨 {nome_loja.upper()}")
        novo_nome = st.text_input("Personalizar Açaiteria", value=nome_loja, label_visibility="collapsed")
        if novo_nome and novo_nome != nome_loja:
            conn.execute("UPDATE config_loja SET nome_loja = ? WHERE id = 1", (novo_nome,))
            conn.commit()
            st.rerun()
        st.divider()
        st.page_link("pages/Dashboard.py", label="Pagina Inicial", icon="🏠")
        st.page_link("pages/Gerenciador_Pedidos.py", label="Pedidos", icon="📋")
        st.page_link("pages/Painel_Producao.py", label="Produção", icon="🥣")
        st.page_link("pages/Estoque.py", label="Estoque", icon="📦")
        st.page_link("pages/Relatorio.py", label="Relatorio", icon="📊")
    conn.close()

def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS config_loja (
            id INTEGER PRIMARY KEY,
            nome_loja TEXT NOT NULL
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO config_loja (id, nome_loja) VALUES (1, 'Tigela Roxa')")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL,
            cliente TEXT NOT NULL,
            item TEXT NOT NULL,
            adicionais TEXT NOT NULL,
            qtd_itens INTEGER DEFAULT 1,
            valor REAL NOT NULL,
            status TEXT DEFAULT 'Pendente',
            data_hora TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            categoria TEXT NOT NULL,
            quantidade REAL NOT NULL,
            minimo REAL NOT NULL,
            unidade TEXT NOT NULL
        )
    """)

    qtd_pedidos = cursor.execute("SELECT COUNT(*) AS total FROM pedidos").fetchone()["total"]
    if qtd_pedidos == 0:
        agora = datetime.now().strftime("%d/%m %H:%M")
        pedidos_iniciais = [
            ("#3666", "Marcel", "Tigela de açaí 500ml", "Morango, Leite Ninho", 2, 32.00, "Preparando", agora),
            ("#0133", "Leonid", "Tigela de açaí 300ml", "Granola, Banana", 1, 18.00, "Pendente", agora),
            ("#0670", "João", "Tigela de açaí 700ml", "Nutella, Paçoca", 3, 45.00, "Pendente", agora),
            ("#1234", "Outro Prof.", "Tigela de açaí 500ml", "Puro", 1, 22.00, "Pendente", agora),
            ("#4567", "Zé", "Tigela de açaí 300ml", "Leite Condensado", 2, 20.00, "Pronto", agora),
        ]
        cursor.executemany(
            "INSERT INTO pedidos (codigo, cliente, item, adicionais, qtd_itens, valor, status, data_hora) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            pedidos_iniciais
        )

    qtd_estoque = cursor.execute("SELECT COUNT(*) AS total FROM estoque").fetchone()["total"]
    if qtd_estoque == 0:
        estoque_inicial = [
            ("Polpa de Açai", "Ingrediente", 8, 15, "kg"),
            ("Granola", "Complemento", 3, 5, "kg"),
            ("Banana", "Complemento", 30, 20, "unid"),
            ("Leite condensado", "Complemento", 12, 6, "latas"),
            ("Nutella", "Complemento", 1, 2, "potes"),
            ("Tigela P", "Embalagem", 45, 30, "unid"),
            ("Tigela M", "Embalagem", 28, 30, "unid"),
        ]
        cursor.executemany(
            "INSERT INTO estoque (item, categoria, quantidade, minimo, unidade) VALUES (?, ?, ?, ?, ?)",
            estoque_inicial
        )

    conn.commit()
    conn.close()
