from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv


with open('links_agenda.txt') as f:
    url_content = f.readlines()
url_content = [x.rstrip('\n') for x in url_content] 
file = open("Agenda.csv",'w', newline='')
writer = csv.writer(file,delimiter=';')
writer.writerow(['País / Liga','País', 'Liga','Data', 'Hora','Time da Casa', 'Time Visitante'])

for i in range(len(url_content)):

    option = Options()
    option.headless = False
    driver = webdriver.Chrome(options=option)
    driver.get(url_content[i])

    div_mae = driver.find_element(By.XPATH, ("/html/body/div[6]/div[1]/div/div[1]/div[2]/div[4]"))

    html_content= div_mae.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    jogos = soup.find('div', class_='event--leagues')
    pais_ligas=  jogos.find('span', class_='event__title--type').text
    nome_ligas=  jogos.find('span', class_='event__title--name').text
    prefixo_nome = str(pais_ligas)+"_"+str(nome_ligas)
    
    conjunto_dia_jogo_ori= ["/".join (linha.get_text().split('.')) for linha in  jogos.find_all(class_='event__time')]
    conjunto_dia_jogo_edit= [linha.replace(" ",";") for linha in conjunto_dia_jogo_ori]
    conjunto_dia_jogo= [linha.replace("/;","/22;") for linha in conjunto_dia_jogo_edit]

    final_str = ["".join(linha.split(";")) for linha in conjunto_dia_jogo]
    data_jogo = [linha[:-5] for linha in final_str]
    hora_jogo = [linha[8:] for linha in final_str]

    conjunto_time_casa= [linha.get_text() for linha in  jogos.find_all(class_='event__participant--home')]
    conjunto_time_fora= [linha.get_text() for linha in  jogos.find_all(class_='event__participant--away')]

    for i in range(len(conjunto_time_casa)):
        print(prefixo_nome,";",data_jogo[i],";",hora_jogo[i],";",conjunto_time_casa[i],";",conjunto_time_fora[i])
        writer.writerow([prefixo_nome,pais_ligas,nome_ligas,data_jogo[i],hora_jogo[i],conjunto_time_casa[i],conjunto_time_fora[i]])
    driver.close() 