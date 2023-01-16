from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
from time import sleep
from datetime import datetime
from datetime import date

with open('lista_url.txt') as f:
    url_content = f.readlines()
url_content = [x.rstrip('\n') for x in url_content] 
file = open("Agenda.csv",'w', newline='')
writer = csv.writer(file,delimiter=';')
writer.writerow(['País / Liga','Data', 'Hora','Time da Casa', 'Time Visitante'])
data_atual = date.today()
data_em_texto = data_atual.strftime('%d/%m/%Y')

for i in range(len(url_content)):

    option = Options()
    option.headless = False
    #option.headless = True
    driver = webdriver.Chrome(options=option)
    url= (url_content[i]+'calendario')
    driver.get(url)
    sleep(2)
    div_mae = driver.find_element(By.XPATH, ("/html/body/div[4]/div[1]/div/div"))
    html_content= div_mae.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    jogos = soup.find('div', class_='event--leagues')
    pais_ligas=  jogos.find('span', class_='event__title--type').text
    nome_ligas=  jogos.find('span', class_='event__title--name').text
    prefixo_nome = str(pais_ligas)+"_"+str(nome_ligas)
    conjunto_dia_jogo_ori= ["/".join (linha.get_text().split('.')) for linha in  jogos.find_all(class_='event__time')]
    conjunto_dia_jogo_edit= [linha.replace(" ",";") for linha in conjunto_dia_jogo_ori]
    conjunto_dia_jogo= [linha.replace("/;","/23;") for linha in conjunto_dia_jogo_edit]
    str_com_adiado = ["".join(linha.split(";")) for linha in conjunto_dia_jogo]    
    final_str = ["".join(linha.split("Adiado")) for linha in str_com_adiado]

    data_jogo = [linha[:-5] for linha in final_str]
    hora_jogo = [linha[8:] for linha in final_str]

    conjunto_time_casa= [linha.get_text() for linha in  jogos.find_all(class_='event__participant--home')]
    conjunto_time_fora= [linha.get_text() for linha in  jogos.find_all(class_='event__participant--away')]
    dates = data_jogo

    for i in range(len(conjunto_time_casa)):
        data_jogo_format =[datetime.strptime(x,'%d/%m/%y') for x in dates]
        data_atual = datetime.strptime(data_em_texto, '%d/%m/%Y')
        quantidade_dias = abs(( data_jogo_format[i]-data_atual).days)
        print(prefixo_nome,";",data_jogo[i],";",hora_jogo[i],";",conjunto_time_casa[i],";",conjunto_time_fora[i])
        if quantidade_dias <= 8:
            #print(prefixo_nome,";",data_jogo[i],";",hora_jogo[i],";",conjunto_time_casa[i],";",conjunto_time_fora[i])
            writer.writerow([prefixo_nome,data_jogo[i],hora_jogo[i],conjunto_time_casa[i],conjunto_time_fora[i]])
    driver.close() 
