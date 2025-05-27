import streamlit as st
from datetime import datetime
import pyperclip
import webbrowser
import os

def main():
    # Configuração da página
    st.set_page_config(
        page_title="Sistema de Baixa/RFO - Alloha Fibra",
        page_icon="📋",
        layout="wide"
    )

    # Estilos CSS personalizados
    st.markdown("""
        <style>
        .stTextArea textarea {height: 150px;}
        .stButton button {width: 100%; background-color: #0054A6; color: white;}
        .report {background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-top: 20px;}
        </style>
        """, unsafe_allow_html=True)

    # Cabeçalho
    st.title("📋 ALLOHA FIBRA - SISTEMA DE BAIXA/RFO")
    st.caption(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # Inicialização das variáveis de sessão
    if 'relatorio' not in st.session_state:
        st.session_state.relatorio = ""

    # Funções
    def gerar_relatorio():
        dados = {
            "descricao": st.session_state.get('descricao', ''),
            "chamado": st.session_state.get('chamado', ''),
            "os": st.session_state.get('os', ''),
            "endereco": st.session_state.get('endereco', ''),
            "km_falha": st.session_state.get('km_falha', ''),
            "local_medicao": st.session_state.get('local_medicao', ''),
            "causa": st.session_state.get('causa', ''),
            "acao_executada": st.session_state.get('acao_executada', ''),
            "material_usado": st.session_state.get('material_usado', ''),
            "fibra": st.session_state.get('fibra', ''),
            "fusoes": st.session_state.get('fusoes', ''),
            "localizacao": st.session_state.get('localizacao', '')
        }

        # Validação
        campos_obrigatorios = {
            "descricao": "Descrição",
            "chamado": "Chamado",
            "os": "OS",
            "endereco": "Endereço",
            "causa": "Causa da Falha"
        }

        for campo, nome in campos_obrigatorios.items():
            if not dados.get(campo, "").strip():
                st.error(f"Campo obrigatório não preenchido: {nome}")
                return None

        relatorio = f"""
        RELATÓRIO DE BAIXA/RFO - ALLOHA FIBRA
        Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
        Descrição: {dados['descricao']}
        Chamado: {dados['chamado']}
        OS: {dados['os']}
        Endereço: {dados['endereco']}
        KM da Falha: {dados['km_falha']}
        Local Medição: {dados['local_medicao']}
        Causa: {dados['causa']}
        Ação Executada: {dados['acao_executada']}
        Material Utilizado: {dados['material_usado']}
        Fibra: {dados['fibra']}
        Fusões: {dados['fusoes']}
        Localização: {dados['localizacao']}
        """

        st.session_state.relatorio = relatorio
        return relatorio

    def salvar_relatorio():
        if not st.session_state.relatorio:
            st.error("Gere o relatório primeiro!")
            return

        nome_arquivo = f"RFO_{st.session_state.get('chamado', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        os.makedirs("relatorios", exist_ok=True)
        caminho = os.path.join("relatorios", nome_arquivo)

        try:
            with open(caminho, 'w', encoding='utf-8') as f:
                f.write(st.session_state.relatorio)
            st.success(f"Relatório salvo como: {nome_arquivo}")
        except Exception as e:
            st.error(f"Erro ao salvar: {str(e)}")

    # Formulário
    with st.form("form_rfo"):
        col1, col2 = st.columns(2)

        with col1:
            st.text_input("DESCRIÇÃO*", key="descricao")
            st.text_input("CHAMADO*", key="chamado")
            st.text_input("OS*", key="os")
            st.text_input("ENDEREÇO*", key="endereco")
            st.text_input("KM DA FALHA", key="km_falha")
            st.text_input("LOCAL MEDIÇÃO", key="local_medicao")

        with col2:
            st.selectbox("CAUSA*", [
                "Acidente", "Arma de Fogo", "Atividade Terceiros",
                "Cabo Queimado", "Curto-Circuito", "Fenômenos Natureza",
                "Fibra Quebrada", "Furto", "Incêndio", "Insetos CEO",
                "Não identificado", "Outro", "Poda", "Queda Árvore",
                "Queda Poste", "Roedores", "Sabotagem", "Vandalismo"
            ], key="causa")

            st.text_area("AÇÃO EXECUTADA", key="acao_executada")
            st.text_area("MATERIAL USADO", key="material_usado")
            st.text_input("FIBRA", key="fibra")
            st.text_input("FUSÕES", key="fusoes")
            st.text_input("LOCALIZAÇÃO", key="localizacao")

        submitted = st.form_submit_button("GERAR RELATÓRIO")

    # Ações e Resultado
    if submitted:
        relatorio = gerar_relatorio()
        if relatorio:
            with st.expander("📄 VISUALIZAR RELATÓRIO", expanded=True):
                st.code(relatorio, language="text")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("📋 COPIAR RELATÓRIO"):
                    pyperclip.copy(relatorio)
                    st.success("Copiado para a área de transferência!")

            with col2:
                if st.button("📱 ENVIAR POR WHATSAPP"):
                    relatorio_url = relatorio.replace("\n", "%0A").replace(" ", "%20")
                    webbrowser.open_new_tab(f"https://wa.me/?text={relatorio_url}")

            with col3:
                if st.button("💾 SALVAR RELATÓRIO"):
                    salvar_relatorio()

            with col4:
                if st.button("🔄 LIMPAR FORMULÁRIO"):
                    for key in list(st.session_state.keys()):
                        if key not in ['_forms', '_form_data']:
                            del st.session_state[key]
                    st.experimental_rerun()

if __name__ == "__main__":
    main()
