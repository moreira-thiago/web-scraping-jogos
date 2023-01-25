from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
from time import sleep
from datetime import datetime
from datetime import date
import pandas as pd

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# Faz a leitura da lista de campeonatos que será feito a raspagem
with open('lista_url.txt') as f:
    url_content = f.readlines()
url_content = [x.rstrip('\n') for x in url_content] 

# writer = pd.ExcelWriter('meus_dados.xlsx', engine='xlsxwriter')
# excel = pd.ExcelWriter('NOME_DO_ARQUIVO.xlsx', engine='xlsxwriter')
# file = open("Agenda.csv",'w', newline='')
# writer = csv.writer(file,delimiter=';')
# writer.writerow(['País / Liga','Data', 'Hora','Time da Casa', 'Time Visitante'])


# Recebe a dta atual do sistema e converte para o fomato dd/mm/yyyy
data_sistema = date.today()
data_em_texto = data_sistema.strftime('%d/%m/%Y')

dados_jogos = pd.DataFrame ( columns =['Pais \ Liga', 'Data' , 'Hora' , 'Casa' , 'Visitante'])   
dados_tabela = pd.DataFrame ( columns =['Pais \ Liga',  'Nome', 'Posição', 'Pontos', 'Gol Pro' , 'Gol Contra', 'F01', 'F02', 'F03', 'F04', 'F05'])   

for i in range(len(url_content)):
    url_classificacao= (url_content[i]+'classificacao')
    url_calendario = (url_content[i]+'calendario')
    #option = Options()
    #option.headless = False
    #option.headless = True
    #driver = webdriver.Chrome(options=option)

    driver.get(url_calendario)
    sleep(1)
    div_mae_calendario = driver.find_element(By.XPATH, ("/html/body/div[4]/div[1]/div/div"))
    html_content= div_mae_calendario.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    jogos = soup.find('div', class_='event--leagues')
    pais_ligas=  jogos.find('span', class_='event__title--type').text
    nome_ligas=  jogos.find('span', class_='event__title--name').text
    conjunto_time_casa= [linha.get_text() for linha in  jogos.find_all(class_='event__participant--home')]
    conjunto_time_fora= [linha.get_text() for linha in  jogos.find_all(class_='event__participant--away')]

    prefixo_nome = str(pais_ligas)+"_"+str(nome_ligas)
    print(prefixo_nome)
    for i in range(len(conjunto_time_casa)):
      prefixo_nomea = [prefixo_nome]
    conjunto_dia_jogo_ori= ["/".join (linha.get_text().split('.')) for linha in  jogos.find_all(class_='event__time')]
    conjunto_dia_jogo_edit= [linha.replace(" ",";") for linha in conjunto_dia_jogo_ori]
    conjunto_dia_jogo= [linha.replace("/;","/23;") for linha in conjunto_dia_jogo_edit]
    str_com_adiado = ["".join(linha.split(";")) for linha in conjunto_dia_jogo]    
    final_str = ["".join(linha.split("Adiado")) for linha in str_com_adiado]

    data_jogo = [linha[:-5] for linha in final_str]
    hora_jogo = [linha[8:] for linha in final_str]




    driver.get(url_classificacao)
    sleep(1)
    div_mae_classificacao = driver.find_element(By.XPATH, ("/html/body/div[4]/div[1]/div/div"))
    html_content_classificacao= div_mae_classificacao.get_attribute('outerHTML')
    soup_classificacao = BeautifulSoup(html_content_classificacao, 'html.parser')
    jogos_classificacao = soup_classificacao.find('div', class_='ui-table__body')


    conjunto_posicao_time= ["".join (linha.get_text().split('.')) for linha in  jogos_classificacao.find_all(class_='tableCellRank')]
    conjunto_nomes= [linha.get_text() for linha in  jogos_classificacao.find_all(class_='tableCellParticipant__name')]
    conjunto_gols_pro_contra= [';'.join (linha.get_text().split(':')) for linha in  jogos_classificacao.find_all(class_='table__cell--score')]
    divisao_gols = ["".join(linha.split(";")) for linha in conjunto_gols_pro_contra]
    gol_pro = [linha[:-2] for linha in divisao_gols]
    gol_contra = [linha[2:] for linha in divisao_gols]
    conjunto_pontos= [linha.get_text() for linha in  jogos_classificacao.find_all(class_='table__cell--points')]
    conjunto_forma_times= [linha.get_text().strip("?") for linha in  jogos_classificacao.find_all(class_='table__cell--form')]

    forma_01 = [linha[:-4] for linha in conjunto_forma_times] 
    forma_02 = [linha[1:-3] for linha in conjunto_forma_times] 
    forma_03 = [linha[2:-2] for linha in conjunto_forma_times] 
    forma_04 = [linha[3:-1] for linha in conjunto_forma_times] 
    forma_05 = [linha[4:] for linha in conjunto_forma_times] 



    for i in range(len(conjunto_time_casa)):
        data_jogo_format =[datetime.strptime(x,'%d/%m/%y') for x in data_jogo]
        data_atual = datetime.strptime(data_em_texto, '%d/%m/%Y')
        quantidade_dias = abs(( data_jogo_format[i]-data_atual).days)
        #print(prefixo_nome,";",data_jogo[i],";",hora_jogo[i],";",conjunto_time_casa[i],";",conjunto_time_fora[i])
        if quantidade_dias <= 8:
            #print(prefixo_nome,";",data_jogo[i],";",hora_jogo[i],";",conjunto_time_casa[i],";",conjunto_time_fora[i])
            dados_jogos = dados_jogos.append({'Pais \ Liga': prefixo_nome, 'Data': data_jogo[i], 'Hora': hora_jogo[i], 'Casa': conjunto_time_casa[i], 'Visitante': conjunto_time_fora[i]}, ignore_index=True)
            #writer.writerow([prefixo_nome,data_jogo[i],hora_jogo[i],conjunto_time_casa[i],conjunto_time_fora[i]])


    for i in range(len(conjunto_nomes)):
        #print(prefixo_nome,";",conjunto_posicao_time[i],";",conjunto_nomes[i],";",gol_pro[i],";",gol_contra[i],";",conjunto_pontos[i],";",forma_01[i],";",forma_02[i],";",forma_03[i],";",forma_04[i],";",forma_05[i])
        #writer.writerow([prefixo_nome,conjunto_nomes[i],conjunto_posicao_time[i],conjunto_pontos[i],gol_pro[i],gol_contra[i],forma_01[i],forma_02[i],forma_03[i],forma_04[i],forma_05[i]])
        dados_tabela = dados_tabela.append({'Pais \ Liga': prefixo_nome, 'Nome':conjunto_nomes[i] , 'Posição':conjunto_posicao_time[i] ,'Pontos':conjunto_pontos[i], 'Gol Pro':gol_pro[i] , 'Gol Contra':conjunto_pontos[i], 'F01':forma_01[i], 'F02':forma_02[i], 'F03':forma_03[i], 'F04':forma_04[i], 'F05':forma_05[i]}, ignore_index=True)
    
    
driver.close() 

dados_renomeado_casa = dados_jogos.rename({'Casa':'Nome'},axis=1)

dados_casa_merge = pd.merge(dados_tabela, dados_renomeado_casa[['Nome','Visitante','Data','Hora']], on=['Nome'], how="inner")

dados_renomeado_visitante = dados_casa_merge.rename({'Nome':'Casa','Visitante':'Nome'},axis=1)

dados_merge_final = pd.merge(dados_renomeado_visitante, dados_tabela[['Nome','Posição','Pontos','Gol Pro','Gol Contra','F01','F02','F03','F04','F05']], on=['Nome'], how="inner")

dados_tabela_final = dados_merge_final.rename({'Nome':'Visitante', 'Posição_x':'P_c','Pontos_x':'Pts_c', 'Gol Pro_x':'G_P_c', 'Gol Contra_x':'G_C_c', 'F01_x':'F01_c', 'F02_x':'F02_c', 'F03_x':'F03_c', 'F04_x':'F04_c', 'F05_x':'F05_c', 'Posição_y':'P_v','Pontos_y':'Pts_v', 'Gol Pro_y':'G_P_v', 'Gol Contra_y':'G_C_v', 'F01_y':'F01_v', 'F02_y':'F02_v', 'F03_y':'F03_v', 'F04_y':'F04_v', 'F05_y':'F05_v'},axis=1)

tabela_final = dados_tabela_final[['Pais \ Liga', 'Data', 'Hora', 'Casa', 'P_c', 'Pts_c', 'G_P_c', 'G_C_c', 'F01_c', 'F02_c', 'F03_c', 'F04_c', 'F05_c', 'Visitante', 'P_v', 'Pts_v', 'G_P_v', 'G_C_v', 'F01_v', 'F02_v', 'F03_v', 'F04_v', 'F05_v']]

# Usando o ExcelWriter, cria um doc .xlsx, usando engine='xlsxwriter'
writer = pd.ExcelWriter('coleta.xlsx', engine='xlsxwriter')

# Armazena cada df em uma planilha diferente do mesmo arquivo
tabela_final.to_excel(writer, sheet_name='Dados Finais')



# Fecha o ExcelWriter e gera o arquivo .xlsx
writer.save()