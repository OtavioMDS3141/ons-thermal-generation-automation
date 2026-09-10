import os
import datetime
import requests
import pandas as pd


# ==========================================
# USINAS DE INTERESSE
# ==========================================

USINAS_INTERESSE = ["UTE JARAQUI","TAMBAQUI","PIRARUCU","TUCUNARE","PORAQUE","APARECIDA","UTE MAUA 3","MAUA BLOCO 3"]

# ==========================================
# DOWNLOAD DOS ARQUIVOS
# ==========================================

def baixar_planilhas_ons(ano, mes):
    pasta_destino = () #INSERIR PASTA DE DESTINO
    os.makedirs(pasta_destino, exist_ok=True)
    data_atual = datetime.date(ano, mes, 1)

    while data_atual.month == mes:
        ano_str = data_atual.strftime("%Y")
        mes_str = data_atual.strftime("%m")
        dia_str = data_atual.strftime("%d")
        data_subpasta = f"{ano_str}_{mes_str}_{dia_str}"
        data_arquivo = f"{dia_str}-{mes_str}-{ano_str}"
        url = (f"https://sdro.ons.org.br/SDRO/DIARIO/{data_subpasta}/HTML/09_ProducaoTermicaUsina_{data_arquivo}.xlsx")
        nome_arquivo = (f"09_ProducaoTermicaUsina_{data_arquivo}.xlsx")
        caminho_salvar = os.path.join(pasta_destino, nome_arquivo)

        if os.path.exists(caminho_salvar):
            print(f"{nome_arquivo} já existe.")
            data_atual += datetime.timedelta(days=1)
            continue

        print(f"Baixando {nome_arquivo}...", end="")

        try:
            resposta = requests.get(url, timeout=20)
            if resposta.status_code == 200:
                with open(caminho_salvar, "wb") as f:
                    f.write(resposta.content)
                print(" ✅ Sucesso")
            elif resposta.status_code == 404:
                print(" ❌ Não encontrado")
            else:
                print(f" ⚠️ Status {resposta.status_code}")

        except Exception as e:
            print(f" ⚠️ Erro: {e}")
        
        data_atual += datetime.timedelta(days=1)

    return pasta_destino

# ==========================================
# GERA O RESUMO
# ==========================================

def gerar_resumo(pasta_destino):
    lista_dataframes = []
    arquivos = sorted(os.listdir(pasta_destino))

    for arquivo in arquivos:
        if not arquivo.endswith(".xlsx"):
            continue
        if arquivo.startswith("Resumo"):
            continue
        caminho = os.path.join(pasta_destino, arquivo)
        print(f"Lendo {arquivo}")

        try:
            df = pd.read_excel(caminho,header=20)
            df = df.dropna(subset=["Usina"])
            data = (arquivo.replace("09_ProducaoTermicaUsina_","").replace(".xlsx",""))
            df_temp = df[["Usina","Verificado (MWmed)"]].copy()
            df_temp["Data"] = data
            df_temp.rename(columns={"Verificado (MWmed)": "Geracao"}, inplace=True)
            df_temp["Usina"] = (df_temp["Usina"].astype(str).str.strip())
            lista_dataframes.append(df_temp)

        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")

    if not lista_dataframes:
        print("Nenhum dado encontrado.")
        return

    df_base = pd.concat(lista_dataframes, ignore_index=True)

    # Todas as usinas

    df_resumo = df_base.pivot_table(index="Usina", columns="Data", values="Geracao", aggfunc="sum",fill_value=0)

    # Apenas usinas selecionadas

    df_selecionadas = (df_resumo.reindex(USINAS_INTERESSE))

    arquivo_saida = os.path.join(pasta_destino, "Resumo_Producao_Mensal.xlsx")

    with pd.ExcelWriter(arquivo_saida, engine="openpyxl") as writer:
        df_base.to_excel(writer, sheet_name="Base_Completa", index=False)
        df_resumo.to_excel(writer, sheet_name="Resumo_Usinas")
        df_selecionadas.to_excel(writer, sheet_name="Usinas_Selecionadas")

    print("\n✅ Resumo criado com sucesso!")
    print(arquivo_saida)

# ==========================================
# EXECUÇÃO
# ==========================================

ANO_DESEJADO = int(input("Digite o ano desejado: "))
MES_DESEJADO = int(input("Digite o mês desejado: "))

pasta_destino = baixar_planilhas_ons(ANO_DESEJADO, MES_DESEJADO)

gerar_resumo(pasta_destino)
