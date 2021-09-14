from selenium import webdriver
from selenium.webdriver.common.keys import Keys

search = input('O que deseja pesquisar? ')

driver = webdriver.Chrome()
driver.get("https://www.google.com")

campo = driver.find_element_by_xpath("//input[@aria-label='Pesquisar']")
campo.send_keys(search)
campo.send_keys(Keys.ENTER)

results = driver.find_element_by_xpath("//div[@id='result-stats']").text
print(results)
num_results = int(results.split("Aproximadamente ")[1].split(' resultados')[0].replace('.',''))
max_pags = num_results/10
#print('Número de páginas: %s' % (max_pags))
pag_escolhida = input("%s páginas encontradas, quer buscar até qual? " % (max_pags))

url_pag = driver.find_element_by_xpath("//a[@aria-label='Page 2']").get_attribute("href")

pag_atual = 0
start = 10
lista_resultados = []
while pag_atual <=int(pag_escolhida) - 1:
    if pag_atual == 0:
        url_pag = url_pag.replace('start=%s' % start, 'start=%s' % (start+10))
        start +=10
        driver.get(url_pag) 
    elif pag_atual == 1:
        driver.get(url_pag)
    pag_atual += 1
     

    divs = driver.find_elements_by_xpath("//div[@class='g']")
    for div in divs:
        nome = div.find_element_by_tag_name("span")
        link = div.find_element_by_tag_name("a")
        resultado = "%s;%s" % (nome.text, link.get_attribute("href"))
        print (resultado)
        lista_resultados.append(resultado)

with open("resultados.txt", "w") as arquivo:
    for resultado in lista_resultados:
        arquivo.write("%s \n" % resultado)
    arquivo.close()

print("%s resultados encontrado do Google e já salvos no arquivo" % len(lista_resultados))
