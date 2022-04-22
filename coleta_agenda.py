from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

url = "https://www.flashscore.com.br/futebol/inglaterra/campeonato-ingles/calendario"
option = Options()
option.headless = True
driver = webdriver.Chrome(options=option)
driver.get(url)
div_mae = driver.find_element(By.XPATH, ("/html/body/div[7]/div[1]/div/div[1]/div[2]/div[4]"))

html_content= div_mae.get_attribute('outerHTML')
soup = BeautifulSoup(html_content, 'html.parser')
jogos = soup.find('div', class_='event--leagues')


pais_ligas=  jogos.find('span', class_='event__title--type').text
nome_ligas=  jogos.find('span', class_='event__title--name').text

prefixo_nome = str(pais_ligas)+"_"+str(nome_ligas)
conjunto_dia_jogo= ["/".join (linha.get_text().split('.')) for linha in  jogos.find_all(class_='event__time')]
conjunto_time_casa= [linha.get_text() for linha in  jogos.find_all(class_='event__participant--home')]
conjunto_time_fora= [linha.get_text() for linha in  jogos.find_all(class_='event__participant--away')]

for i in range(len(conjunto_time_casa)):
     print(prefixo_nome,";",conjunto_dia_jogo[i],";",conjunto_time_casa[i],";",conjunto_time_fora[i])
 