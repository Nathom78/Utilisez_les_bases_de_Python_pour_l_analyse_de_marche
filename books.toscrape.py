import requests
from bs4 import BeautifulSoup
import csv


# récupère les titres ou descriptions comme liste de strings
def extraire_donnees(elements):
    resultat = []
    for element in elements:
        resultat.append(element.string)
    return resultat


# charger la donnée dans un fichier csv
def charger_donnees(nom_fichier, en_tete, titres, descriptions):
    with open(nom_fichier, 'w') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(en_tete)
        # zip permet d'itérer sur deux listes à la fois
        for titre, description in zip(titres, descriptions):
            writer.writerow([titre, description])


def etl(url_product):
    # lien de la page à scrapper
    reponse = requests.get(url_product)
    page = reponse.content

    # transforme (parse) le HTML en objet BeautifulSoup
    soup = BeautifulSoup(page, "html.parser")

    # récupération des données du tableau de la page
    table = soup.find_all("tr")
    case = []
    for ligne in table:
        case.append(ligne.td.string)

    # récupération product_page_url
    product_page_url = url_product

    # récupération universal_product_code (upc)
    universal_product_code = case[0]

    # récupération title
    title = soup.find("content_inner > article > div.row > div.col-sm-6.product_main")
    print(title)
    # content_inner > article > div.row > div.col-sm-6.product_main

    # récupération price_including_tax
    price_including_tax = case[3]

    # récupération price_excluding_tax
    price_excluding_tax = case[2]

    # récupération number_available
    number_available = int(''.join(filter(str.isdigit, case[5])))

    # récupération product_description
    product_description = soup.find("article").p
    print(product_description)

    # récupération category
    # récupération review_rating
    # récupération image_url

    # récupération de tous les titres

    # récupération de toutes les descriptions
    # descriptions = soup.find_all("p", class_="gem-c-document-list__item-description")

    en_tete = ["product_page_url", "universal_product_code (upc)", "title",
               "price_including_tax", "price_excluding_tax", "number_available",
               "product_description", "category", "review_rating", "image_url", "image"]

    # titres = extraire_donnees(titres)
    # descriptions = extraire_donnees(descriptions)
    # charger_donnees("Data/data.csv", en_tete, product_page_url, universal_product_code, title,
    #                price_including_tax, price_excluding_tax, number_available,
    #                product_description, category, review_rating, image_url, image)


url = "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
etl(url)
