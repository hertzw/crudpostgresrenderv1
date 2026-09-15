import streamlit as st
import pandas as pd
from config import  repositorio


repositorio()
cursor = repositorio.mydb.cursor()

OPERACOES = {
    "Create": "➕ Criar",
    "Read": "📋 Listar",
    "Update": "✏️ Atualizar",
    "Delete": "🗑️ Excluir",
}

ESTILO = """
<style>
:root {
    --navy: #17304f;
    --navy-dark: #0f2238;
    --teal: #2c8c76;
    --teal-dark: #1f6a58;
    --card-bg: #ffffff;
    --text-dark: #1c2b45;
    --text-muted: #7c869c;
}

[data-testid="stAppViewContainer"] { background-color: #eef1f8; }
h1, h2, h3 { color: var(--text-dark); }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--navy) 0%, var(--navy-dark) 100%);
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .card-descricao {
    color: #ffffff !important;
}

/* Pill buttons (padrão geral) */
[data-testid="stButton"] button,
[data-testid="stFormSubmitButton"] button {
    border: none;
    border-radius: 999px;
    font-weight: 600;
    padding: 0.5rem 1.5rem;
    background: linear-gradient(135deg, var(--navy) 0%, var(--teal) 100%);
    color: #ffffff;
    box-shadow: 0 4px 10px rgba(23, 48, 79, 0.2);
    transition: transform .15s ease, box-shadow .15s ease;
}
[data-testid="stButton"] button:hover,
[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(44, 140, 118, 0.35);
    color: #ffffff;
}

/* Pills de navegação na sidebar */
[data-testid="stSidebar"] button {
    text-align: left;
    justify-content: flex-start;
}
[data-testid="stSidebar"] [data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, var(--teal) 0%, var(--teal-dark) 100%);
    color: #ffffff;
    border: none;
}
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {
    background: rgba(255, 255, 255, 0.08);
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.25);
    box-shadow: none;
}
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover {
    background: rgba(255, 255, 255, 0.18);
    color: #ffffff;
}

/* Botões de ação (ícone) na tabela do Listar */
.st-key-tabela_acoes [data-testid="stButton"] button {
    padding: 0.3rem 0.7rem;
    font-size: 0.95rem;
    box-shadow: none;
}

/* Cartões (forms e containers com borda) */
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stForm"] {
    background-color: var(--card-bg);
    border-radius: 18px;
    padding: 1.1rem 1.4rem;
    box-shadow: 0 8px 24px rgba(23, 48, 79, 0.08);
    border: 1px solid rgba(23, 48, 79, 0.06);
}

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    border-radius: 10px;
}

.card-titulo {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-dark);
    margin-bottom: 0.1rem;
}
.card-descricao {
    color: var(--text-muted);
    font-size: 0.85rem;
    margin-bottom: 0.9rem;
}
</style>
"""


def aplicar_estilo():
    st.markdown(ESTILO, unsafe_allow_html=True)


def cabecalho_cartao(titulo, descricao=None):
    st.markdown(f"<div class='card-titulo'>{titulo}</div>", unsafe_allow_html=True)
    if descricao:
        st.markdown(f"<div class='card-descricao'>{descricao}</div>", unsafe_allow_html=True)


def navegacao_lateral():
    if "operacao_atual" not in st.session_state:
        st.session_state["operacao_atual"] = "Create"

    st.sidebar.markdown("## 🗂️ CRUD Postgres")
    st.sidebar.markdown("<div class='card-descricao'>Selecione uma operação</div>", unsafe_allow_html=True)
    for chave, rotulo in OPERACOES.items():
        ativo = st.session_state["operacao_atual"] == chave
        if st.sidebar.button(
            rotulo,
            key=f"nav_{chave}",
            use_container_width=True,
            type="primary" if ativo else "secondary",
        ):
            if st.session_state["operacao_atual"] != chave:
                st.session_state["operacao_atual"] = chave
                st.rerun()

    return st.session_state["operacao_atual"]


def carregar_registros():
    repositorio.cursor.execute("select id, name, email from users order by id")
    colunas = [desc[0] for desc in repositorio.cursor.description]
    linhas = repositorio.cursor.fetchall()
    return pd.DataFrame(linhas, columns=colunas)


def tabela_selecionavel(df, key):
    st.caption("Selecione uma linha na tabela.")
    evento = st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        key=key,
    )
    linhas_selecionadas = evento.selection.rows
    if not linhas_selecionadas:
        return None
    return df.iloc[linhas_selecionadas[0]]


LARGURAS_COLUNAS = [0.6, 2, 3, 0.8, 0.8]


def tabela_com_acoes(df):
    with st.container(border=True, key="tabela_acoes"):
        cabecalho = st.columns(LARGURAS_COLUNAS)
        for coluna, titulo in zip(cabecalho, ["ID", "Nome", "Email", "✏️ Editar", "🗑️ Excluir"]):
            coluna.markdown(f"**{titulo}**")

        for _, registro in df.iterrows():
            id_registro = int(registro["id"])
            linha = st.columns(LARGURAS_COLUNAS)
            linha[0].write(id_registro)
            linha[1].write(registro["name"])
            linha[2].write(registro["email"])
            if linha[3].button("✏️", key=f"editar_{id_registro}"):
                st.session_state["id_editando"] = id_registro
                st.session_state["id_excluindo"] = None
            if linha[4].button("🗑️", key=f"excluir_{id_registro}"):
                st.session_state["id_excluindo"] = id_registro
                st.session_state["id_editando"] = None


def formulario_edicao_inline(df):
    id_editando = st.session_state.get("id_editando")
    if id_editando is None:
        return
    encontrados = df[df["id"] == id_editando]
    if encontrados.empty:
        st.session_state["id_editando"] = None
        return

    registro = encontrados.iloc[0]
    with st.form("form_editar_listagem"):
        cabecalho_cartao(f"✏️ Editando registro #{id_editando}", "Atualize os dados e salve para confirmar.")
        name = st.text_input("Nome", value=registro["name"])
        email = st.text_input("Email", value=registro["email"])
        col_salvar, col_cancelar = st.columns(2)
        salvar = col_salvar.form_submit_button("💾 Salvar")
        cancelar = col_cancelar.form_submit_button("Cancelar")

    if salvar:
        sql = "update users set name=%s, email=%s where id=%s"
        val = (name, email, id_editando)
        repositorio.cursor.execute(sql, val)
        repositorio.mydb.commit()
        st.session_state["id_editando"] = None
        st.success("Registro atualizado")
        st.rerun()
    elif cancelar:
        st.session_state["id_editando"] = None
        st.rerun()


def confirmacao_exclusao_inline(df):
    id_excluindo = st.session_state.get("id_excluindo")
    if id_excluindo is None:
        return
    encontrados = df[df["id"] == id_excluindo]
    if encontrados.empty:
        st.session_state["id_excluindo"] = None
        return

    registro = encontrados.iloc[0]
    with st.container(border=True):
        cabecalho_cartao("🗑️ Confirmar exclusão", f"{registro['name']} — {registro['email']}")
        col_confirmar, col_cancelar = st.columns(2)
        if col_confirmar.button("Confirmar exclusão", key="confirmar_exclusao_listagem"):
            sql = "delete from users where id=%s"
            val = (id_excluindo,)
            repositorio.cursor.execute(sql, val)
            repositorio.mydb.commit()
            st.session_state["id_excluindo"] = None
            st.success("Registro removido")
            st.rerun()
        if col_cancelar.button("Cancelar", key="cancelar_exclusao_listagem"):
            st.session_state["id_excluindo"] = None
            st.rerun()


# Streamlit app
def main():
    st.set_page_config(page_title="CRUD Postgres", page_icon="🗂️", layout="wide")
    aplicar_estilo()
    st.title("CRUD com Postgres")

    # Options
    option = navegacao_lateral()

    # Execute operations

    if option=="Create":
        with st.form("form_create"):
            cabecalho_cartao("➕ Novo Registro", "Preencha os campos abaixo para cadastrar um usuário.")
            name=st.text_input("Nome")
            email=st.text_input("Email")
            if st.form_submit_button("➕ Criar"):
                sql= "insert into users(name,email) values(%s,%s)"
                val= (name,email)
                repositorio.cursor.execute(sql,val)
                repositorio.mydb.commit()
                st.success("Registro salvo")

    elif option=="Read":
        st.subheader("📋 Ler Registros")
        df = carregar_registros()
        if df.empty:
            st.info("Nenhum registro cadastrado.")
        else:
            tabela_com_acoes(df)
            formulario_edicao_inline(df)
            confirmacao_exclusao_inline(df)

    elif option=="Update":
        st.subheader("✏️ Atualizar Registro")
        df = carregar_registros()
        if df.empty:
            st.info("Nenhum registro cadastrado.")
        else:
            with st.container(border=True):
                registro = tabela_selecionavel(df, key="tabela_update")
            if registro is None:
                st.info("Nenhuma linha selecionada.")
            else:
                with st.form("form_update"):
                    cabecalho_cartao(f"✏️ Editando registro #{int(registro['id'])}", "Atualize os dados e confirme.")
                    name = st.text_input("Enter New Name", value=registro["name"])
                    email = st.text_input("Enter New Email", value=registro["email"])
                    if st.form_submit_button("✏️ Update"):
                        sql="update users set name=%s, email=%s where id =%s"
                        val=(name,email,int(registro["id"]))
                        repositorio.cursor.execute(sql,val)
                        repositorio.mydb.commit()
                        st.success("Registro Salvo")
                        st.rerun()

    elif option=="Delete":
        st.subheader("🗑️ Excluir Registro")
        df = carregar_registros()
        if df.empty:
            st.info("Nenhum registro cadastrado.")
        else:
            with st.container(border=True):
                registro = tabela_selecionavel(df, key="tabela_delete")
            if registro is None:
                st.info("Nenhuma linha selecionada.")
            else:
                with st.container(border=True):
                    cabecalho_cartao("🗑️ Confirmar exclusão", f"{registro['name']} — {registro['email']}")
                    if st.button("🗑️ Delete"):
                        sql="delete from users where id =%s"
                        val=(int(registro["id"]),)
                        repositorio.cursor.execute(sql,val)
                        repositorio.mydb.commit()
                        st.success("Registro removido")
                        st.rerun()

if __name__ == "__main__":
    main()
