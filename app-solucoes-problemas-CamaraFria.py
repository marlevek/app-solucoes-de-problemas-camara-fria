import streamlit as st

st.set_page_config('Causas e Soluções de Problemas em Câmara Fria', page_icon=':material/severe_cold:')

st.title('Causas e Soluções de Problemas em Câmara Fria')

# Função para carregar as instruções de teste a partir de um arquivo txt
def carregar_instrucoes():
    try:
        with open('testes.txt', 'r', encoding='utf-8') as file:
            conteudo = file.read()

            # Dividir o conteúdo por seções
            instrucoes = conteudo.strip().split("\n\n")
            
            # Criar um dicionário para armazenar as instruções
            instrucoes_dict = {}
            for instrucao in instrucoes:
                linhas = instrucao.strip().split('\n')
                if linhas:
                    # A primeira linha deve ser o título do defeito
                    titulo = linhas[0].strip()
                    texto = '\n'.join(linhas[1:]).strip()
                    if titulo:  # Adiciona apenas se houver um título
                        instrucoes_dict[titulo] = texto
                
            # Retornar o dicionário de instruções
            return instrucoes_dict
        
    except FileNotFoundError:
        st.error('Arquivo "testes.txt" não encontrado.')
        return {}
    except Exception as e:
        st.error(f'Erro ao ler o arquivo: {str(e)}')
        return {}

# Carregar todas as instruções do arquivo
instrucoes_dict = carregar_instrucoes()

# Opções de seleção de defeito
tipo_teste = st.selectbox('Selecione o Defeito', ['Defeitos...'] + list(instrucoes_dict.keys()))

# Carregar instruções para o teste selecionado
if tipo_teste != 'Defeitos...':
    instrucoes = instrucoes_dict.get(tipo_teste)
    
    if instrucoes:
        st.subheader(f'Causas e Soluções para {tipo_teste}')
        
        # Formatar e exibir as instruções
        linhas = instrucoes.split('\n')
        
        # Variáveis para armazenar causas e soluções
        causas = []
        solucoes = []
        coletando_causas = False
        coletando_solucoes = False
        
        # Separar as causas e soluções
        for linha in linhas:
            linha = linha.strip()
            if linha.startswith('Causa:'):
                coletando_causas = True
                coletando_solucoes = False
                # Remove "Causa:" e pega as causas
                causas = [c.strip() for c in linha.replace('Causa:', '').split('\n')]
            elif linha.startswith('Solução:'):
                coletando_causas = False
                coletando_solucoes = True
                # Remove "Solução:" e pega as soluções
                solucoes = [s.strip() for s in linha.replace('Solução:', '').split('\n')]
            elif coletando_causas:
                causas.append(linha)
            elif coletando_solucoes:
                solucoes.append(linha)
        
        # Criar uma tabela formatada em Markdown
        markdown_table = '| Causa | Solução |\n'
        markdown_table += '| --- | --- |\n'
        
        # Preencher a tabela com causas e soluções
        for i in range(max(len(causas), len(solucoes))):
            causa = causas[i] if i < len(causas) else ''
            solucao = solucoes[i] if i < len(solucoes) else ''
            markdown_table += f"| {causa} | {solucao} |\n"
                
        # Exibir a tabela formatada
        st.markdown(markdown_table)
        
    else:
        st.warning('Instruções não encontradas.')
else:
    st.warning('Por favor, selecione um tipo de defeito válido.')




