from asyncore import write
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By
import csv
import pandas as pd
#url = "https://www.flashscore.com.br/futebol/inglaterra/campeonato-ingles/classificacao/"

with open('links_classificação.txt') as f:
    url_content = f.readlines()
url_content = [x.rstrip('\n') for x in url_content] 
file = open("Tabelas.csv",'w', newline='')
writer = csv.writer(file,delimiter=';')
writer.writerow(['País / Liga','Posição', 'Time', 'Gols Pros', 'Gols Contras','Pontos', 'Forma 01', 'Forma 02', 'Forma 03', 'Forma 04', 'Forma 05'])

for i in range(len(url_content)):

     option = Options()
     option.headless = False
     driver = webdriver.Chrome(options=option)
     driver.get(url_content[i])

     div_mae = driver.find_element(By.XPATH, ("/html/body/div[6]/div[1]/div/div[1]"))
 
     html_content= div_mae.get_attribute('outerHTML')
     soup = BeautifulSoup(html_content, 'html.parser')
     jogos = soup.find('div', class_='ui-table__body')
     jogos_nomes = soup.find('div', class_='container__overlay')
     pais_ligas=  jogos_nomes.find(class_='leftMenu__title--white').text
     jogos_nomes = soup.find('div', class_='container__livetable')
     nome_ligas =  jogos_nomes.find(class_='heading__name').text.strip()
     prefixo_nome = str(pais_ligas)+"_"+str(nome_ligas)
     
     conjunto_posicao_time= ["".join (linha.get_text().split('.')) for linha in  jogos.find_all(class_='tableCellRank')]
     conjunto_nomes= [linha.get_text() for linha in  jogos.find_all(class_='tableCellParticipant__name')]
     conjunto_gols_pro_contra= [';'.join (linha.get_text().split(':')) for linha in  jogos.find_all(class_='table__cell--score')]
     divisao_gols = ["".join(linha.split(";")) for linha in conjunto_gols_pro_contra]
     gol_pro = [linha[:-2] for linha in divisao_gols]
     gol_contra = [linha[2:] for linha in divisao_gols]
     conjunto_pontos= [linha.get_text() for linha in  jogos.find_all(class_='table__cell--points')]
     #conjunto_forma_times= [";".join (linha.get_text().strip("?")) for linha in  jogos.find_all(class_='table__cell--form')]
     conjunto_forma_times= [linha.get_text().strip("?") for linha in  jogos.find_all(class_='table__cell--form')]

     forma_01 = [linha[:-4] for linha in conjunto_forma_times] 
     forma_02 = [linha[1:-3] for linha in conjunto_forma_times] 
     forma_03 = [linha[2:-2] for linha in conjunto_forma_times] 
     forma_04 = [linha[3:-1] for linha in conjunto_forma_times] 
     forma_05 = [linha[4:] for linha in conjunto_forma_times] 


     for i in range(len(conjunto_nomes)):
          print(prefixo_nome,";",conjunto_posicao_time[i],";",conjunto_nomes[i],";",gol_pro[i],";",gol_contra[i],";",conjunto_pontos[i],";",forma_01[i],";",forma_02[i],";",forma_03[i],";",forma_04[i],";",forma_05[i])
          writer.writerow([prefixo_nome,conjunto_posicao_time[i],conjunto_nomes[i],gol_pro[i],gol_contra[i],conjunto_pontos[i],forma_01[i],forma_02[i],forma_03[i],forma_04[i],forma_05[i]])
       
     driver.close()
file.close()
