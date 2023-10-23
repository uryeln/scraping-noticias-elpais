import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import re

url = "https://elpais.com/tecnologia/"

def extrairDados(artigo):
    categoria = artigo.find("header", class_="c_h").find("a").text
    titulo = artigo.find("h2", class_="c_t").text.strip()

    # Autor
    autor_tag = artigo.find("div", class_="c_a")
    if autor_tag:
        autor_a = autor_tag.find("a", class_="c_a_a")
        autor = autor_a.text if autor_a else "Autor não disponível"
    else:
        autor = "Autor não disponível"

    # Data
    data_tag = artigo.find("time")
    data = data_tag["datetime"] if data_tag else "Data e hora não disponíveis"

    # Resumo
    resumo_tag = artigo.find("p", class_="c_d")
    resumo = resumo_tag.text.strip() if resumo_tag else "Resumo não disponível"

    return {
        "Categoria": categoria,
        "Título": titulo,
        "Autor": autor,
        "Data e Hora": data,
        "Resumo": resumo
    }

dadosArtigosLista = []

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

tabs = soup.find("nav", class_="cs_m").find_all("a")

# Percorra cada aba
for tab in tabs:
    tab_url = tab["href"]

    # urljoin para criar uma URL completa
    full_url = urljoin(url, tab_url)

    response = requests.get(full_url)
    tab_soup = BeautifulSoup(response.text, "html.parser")

    artigos = tab_soup.find_all("article", class_="c")

    for artigo in artigos:
        artigosDados = extrairDados(artigo)
        dadosArtigosLista.append(artigosDados)

arquivo = pd.DataFrame(dadosArtigosLista)

# Salve os dados em CSV
arquivo.to_csv("tecnologia.csv", index=False)
