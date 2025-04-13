import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime

# Configuração inicial
st.set_page_config(page_title="ORION PDV", layout="wide")

# URLs dos dados externos
URL_GRUPO = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS0r3XE4DpzlYJjZwjc2c_pW_K3euooN9caPedtSq-nH_aEPnvx1jrcd9t0Yhg8fqXfR3j5jM2OyUQQ/pub?gid=528868130&single=true&output=csv"
URL_MARCAS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS0r3XE4DpzlYJjZwjc2c_pW_K3euooN9caPedtSq-nH_aEPnvx1jrcd9t0Yhg8fqXfR3j5jM2OyUQQ/pub?gid=832596780&single=true&output=csv"
URL_CLIENTE = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS0r3XE4DpzlYJjZwjc2c_pW_K3euooN9caPedtSq-nH_aEPnvx1jrcd9t0Yhg8fqXfR3j5jM2OyUQQ/pub?gid=1645177762&single=true&output=csv"
URL_PRODUTO = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS0r3XE4DpzlYJjZwjc2c_pW_K3euooN9caPedtSq-nH_aEPnvx1jrcd9t0Yhg8fqXfR3j5jM2OyUQQ/pub?gid=1506891785&single=true&output=csv"
URL_PGTO = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS0r3XE4DpzlYJjZwjc2c_pW_K3euooN9caPedtSq-nH_aEPnvx1jrcd9t0Yhg8fqXfR3j5jM2OyUQQ/pub?gid=1061064660&single=true&output=csv"
URL_VENDA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS0r3XE4DpzlYJjZwjc2c_pW_K3euooN9caPedtSq-nH_aEPnvx1jrcd9t0Yhg8fqXfR3j5jM2OyUQQ/pub?gid=1817416820&single=true&output=csv"

# Dados de autenticação
USUARIOS = {
    "admjesus": {
        "nome": "ADM Jesus",
        "senha_hash": hashlib.sha256("senha123".encode()).hexdigest()
    }
}

# Função de autenticação
def autenticar_usuario():
    st.title("🔐 Login - ORION PDV")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario in USUARIOS:
            hash_inserida = hashlib.sha256(senha.encode()).hexdigest()
            if hash_inserida == USUARIOS[usuario]["senha_hash"]:
                st.session_state["autenticado"] = True
                st.session_state["usuario"] = usuario
                st.success("Login realizado com sucesso!")
                st.rerun()  # Usando rerun() em vez de experimental_rerun()
            else:
                st.error("Senha incorreta.")
        else:
            st.error("Usuário não encontrado.")

# Função de cadastro de produto
def render_cadastro_produto():
    st.title("📦 Cadastro de Produto")

    try:
        grupo_df = pd.read_csv(URL_GRUPO)
        marcas_df = pd.read_csv(URL_MARCAS)
    except Exception as e:
        st.error(f"Erro ao carregar dados de grupo/marcas: {e}")
        return

    with st.form("form_cad_produto"):
        nome = st.text_input("Nome do Produto")
        grupo = st.selectbox("Grupo", grupo_df["DESCRICAO"].dropna())
        marca = st.selectbox("Marca", marcas_df["DESCRICAO"].dropna())
        preco = st.number_input("Preço", min_value=0.0)
        estoque = st.number_input("Estoque", min_value=0)
        enviar = st.form_submit_button("Salvar")

        if enviar:
            st.success("Produto cadastrado com sucesso!")
            st.json({
                "nome": nome,
                "grupo": grupo,
                "marca": marca,
                "preco": preco,
                "estoque": estoque
            })

# Função de cadastro de cliente
def render_cadastro_cliente():
    st.title("👤 Cadastro de Cliente")
    
    with st.form("form_cad_cliente"):
        nome = st.text_input("Nome do Cliente")
        documento = st.text_input("CPF/CNPJ")
        email = st.text_input("Email")
        telefone = st.text_input("Telefone")
        
        col1, col2 = st.columns(2)
        with col1:
            endereco = st.text_input("Endereço")
        with col2:
            cidade = st.text_input("Cidade")
            
        enviar = st.form_submit_button("Salvar Cliente")
        
        if enviar:
            st.success("Cliente cadastrado com sucesso!")
            st.json({
                "nome": nome,
                "documento": documento,
                "email": email,
                "telefone": telefone,
                "endereco": endereco,
                "cidade": cidade
            })

# Função de registro de venda
def render_registro_venda():
    st.title("🧾 Registrar Venda")

    try:
        cliente_df = pd.read_csv(URL_CLIENTE)
        produto_df = pd.read_csv(URL_PRODUTO)
        forma_pgto_df = pd.read_csv(URL_PGTO)
    except Exception as e:
        st.error(f"Erro ao carregar dados de venda: {e}")
        return

    with st.form("form_venda"):
        cliente = st.selectbox("Cliente", cliente_df["NOME"].dropna())
        forma_pgto = st.selectbox("Forma de Pagamento", forma_pgto_df["DESCRICAO"].dropna())

        st.markdown("---")
        st.subheader("Produtos")

        itens = []
        for i in range(3):
            col1, col2 = st.columns(2)
            with col1:
                produto = st.selectbox(f"Produto {i+1}", produto_df["DESCRICAO"], key=f"produto_{i}")
            with col2:
                qtd = st.number_input(f"Quantidade {i+1}", min_value=0, step=1, key=f"qtd_{i}")

            if qtd > 0:
                preco = float(produto_df.loc[produto_df["DESCRICAO"] == produto, "PRECO"].values[0])
                total = qtd * preco
                itens.append({"produto": produto, "quantidade": qtd, "preco_unit": preco, "total": total})

        submitted = st.form_submit_button("Finalizar Venda")

    if submitted and itens:
        total_geral = sum(item["total"] for item in itens)
        venda = {
            "cliente": cliente,
            "forma_pgto": forma_pgto,
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": total_geral,
            "itens": itens
        }

        st.success("Venda registrada com sucesso!")
        st.json(venda)

# Função de relatórios
def render_relatorios():
    st.title("📊 Relatório de Vendas")

    try:
        venda_df = pd.read_csv(URL_VENDA)
        venda_df["DATA"] = pd.to_datetime(venda_df["DATA"], errors="coerce")
    except Exception as e:
        st.error(f"Erro ao carregar dados para relatório: {e}")
        return

    col1, col2 = st.columns(2)
    with col1:
        data_ini = st.date_input("Data Inicial", datetime.today())
    with col2:
        data_fim = st.date_input("Data Final", datetime.today())

    formas = venda_df["ID_FORMA_PGTO"].dropna().unique()
    forma_selecionada = st.selectbox("Filtrar por Forma de Pagamento (opcional)", ["Todas"] + list(formas))

    if st.button("Gerar Relatório"):
        try:
            filtro = (venda_df['DATA'].dt.date >= data_ini) & (venda_df['DATA'].dt.date <= data_fim)
            if forma_selecionada != "Todas":
                filtro &= (venda_df['ID_FORMA_PGTO'] == forma_selecionada)

            relatorio = venda_df[filtro].copy()

            if not relatorio.empty:
                st.success(f"Foram encontradas {len(relatorio)} vendas no período.")
                st.dataframe(relatorio)
                total = relatorio['TOTAL'].sum()
                st.markdown(f"### 💰 Total de Vendas no Período: R$ {total:.2f}")

                csv = relatorio.to_csv(index=False).encode()
                st.download_button("📥 Baixar CSV", csv, "relatorio_vendas.csv", "text/csv")
            else:
                st.warning("Nenhuma venda encontrada para os filtros aplicados.")

        except Exception as err:
            st.error(f"Erro no processamento do relatório: {err}")

# Função do painel financeiro
def render_painel():
    st.title("📈 Painel Financeiro")

    try:
        venda_df = pd.read_csv(URL_VENDA)
        venda_df["DATA"] = pd.to_datetime(venda_df["DATA"], errors="coerce")
    except Exception as e:
        st.error(f"Erro ao carregar dados para o painel: {e}")
        return

    # Versão sem Plotly (usando gráficos nativos do Streamlit)
    st.subheader("Total por Forma de Pagamento")
    pgto_group = venda_df.groupby("ID_FORMA_PGTO")["TOTAL"].sum().reset_index()
    st.bar_chart(pgto_group.set_index("ID_FORMA_PGTO"))
    
    st.subheader("Evolução Diária de Vendas")
    diario = venda_df.groupby(venda_df["DATA"].dt.date)["TOTAL"].sum().reset_index()
    st.line_chart(diario.set_index("DATA"))
    
    total_vendas = venda_df['TOTAL'].sum()
    st.metric("Total Geral de Vendas", f"R$ {total_vendas:,.2f}")

# Função principal que gerencia todo o fluxo do aplicativo
def main():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        autenticar_usuario()
        return

    st.sidebar.title("🔹 Menu PDV")
    if st.sidebar.button("Sair"):
        st.session_state["autenticado"] = False
        st.rerun()  # Usando rerun() em vez de experimental_rerun()

    menu = st.sidebar.radio("Escolha a opção:", [
        "Cadastro Produto", "Cadastro Cliente", "Registrar Venda", "Relatórios", "Painel"])

    if menu == "Cadastro Produto":
        render_cadastro_produto()
    elif menu == "Cadastro Cliente":
        render_cadastro_cliente()
    elif menu == "Registrar Venda":
        render_registro_venda()
    elif menu == "Relatórios":
        render_relatorios()
    elif menu == "Painel":
        render_painel()

# Execução principal
if __name__ == "__main__":
    main()
