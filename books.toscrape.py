import requests
import time
import os
from bs4 import BeautifulSoup
import csv


def get_last_digit(str1):
    c = ""
    for i in str1:
        if i.isdigit():
            c = i

    return c


# charger les données dans un fichier csv
def save_data(nom_category, en_tete, list_data):
    # nom du fichier
    file_data_name = "Data/" + nom_category + "/" + nom_category + "_book_" + time.strftime("%Y%m%d") + ".csv"
    dir_path = "Data/" + nom_category + "/"
    # création du repertoire si besoin
    os.makedirs(dir_path, exist_ok=True)

    if_exist = 0
    try:
        with open(file_data_name):
            if_exist = 1
            pass
    except IOError:
        pass

    # Savoir pour écrire l'entête ou ajouter
    if if_exist == 0:
        with open(file_data_name, 'w', newline='') as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=',')
            writer.writerow(en_tete)
            writer.writerow(list_data)
    else:
        with open(file_data_name, 'a', newline='') as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=',')
            writer.writerow(list_data)


# sauvegarder l'image
def transfert_image(url_img, file_name):
    if_exist = 0
    try:
        with open(file_name):
            if_exist = 1
            pass
    except IOError:
        pass
    # si le fichier n'existe pas déjà
    if if_exist == 0:
        # GET request
        response = requests.get(url_img)
        # Enregistrer l'image
        if response.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(response.content)
        else:
            print(response.status_code)


#  Extraire les données de la page HTML d’un seul produit
def scrap_article(url_book):
    # lien de la page produit à scrapper
    reponse = requests.get(url_book)
    if reponse.status_code == 200:
        page = reponse.content
        # transforme (parse) le HTML en objet BeautifulSoup
        soup = BeautifulSoup(page, "html.parser")

        # récupération des données du tableau de la page
        table = soup.find_all("tr")
        case = []
        for ligne in table:
            case.append(ligne.td.string)

        # récupération product_page_url
        product_page_url = url_book

        # récupération universal_product_code (upc)
        universal_product_code = case[0]

        # récupération title
        title = soup.find("div", class_="col-sm-6 product_main").h1.string

        # récupération price_including_tax
        price_including_tax = case[3]

        # récupération price_excluding_tax
        price_excluding_tax = case[2]

        # récupération number_available
        number_available = int(''.join(filter(str.isdigit, case[5])))

        # récupération product_description
        product_description = soup.find(id="product_description").find_next_sibling("p").string

        # récupération category
        breadcrumbs = soup.find(class_="breadcrumb")
        breadcrumb = breadcrumbs.find_all("li")
        puce_link = []
        for ligne in breadcrumb:
            puce_link.append(ligne.get_text(strip=True))
        category = puce_link[2]

        # récupération review_rating
        p_stars = soup.find(class_="star-rating").attrs
        review_rating = p_stars["class"][1]

        # récupération image_url
        image_url_tmp = soup.find('img')['src']
        image_url = image_url_tmp.replace('../..', "http://books.toscrape.com")

        # ligne head du tableau
        en_tete = ["product_page_url", "universal_product_code (upc)", "title",
                   "price_including_tax", "price_excluding_tax", "number_available",
                   "product_description", "category", "review_rating", "image_url"]

        # liste de la ligne des données
        data = [product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax,
                number_available, product_description, category, review_rating, image_url]

        title_reformat = title.translate({ord(c): "_" for c in " !@#$%^&*()[]{};:,./<>?|`~-=_+"})
        # nom du fichier image
        file_img_name = "Data/" + category + "/" + "book_img_" + title_reformat + ".jpg"

        # actions
        save_data(category, en_tete, data)
        transfert_image(image_url, file_img_name)
    else:
        print("Url de l'article inatteignable")


# url de l'article
# url_product = "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
# scrap un livre
# scrap_article(url_product)


def scrap_category(url_category):

    url_category_racine = url_category.replace("index.html", "")
    i = 0
    n = 0

    while True:
        i += 1
        reponse = requests.get(url_category)

        if reponse.status_code == 200:
            page = reponse.content
            # transforme (parse) le HTML en objet BeautifulSoup
            soup = BeautifulSoup(page, "html.parser")

            # Test si fichier du jour déjà existant
            category = soup.select_one("#default > div > div > div > div > div.page-header.action > h1").text
            file_name = "Data/" + category + "/" + category + "_book_" + time.strftime("%Y%m%d") + ".csv"
            if i == 1:
                if os.path.exists(file_name):
                    print(" Fichier du jour déjà existant -> suppression")
                    s = input("suppression O/N?")
                    if s == ('o' or 'O'):
                        os.remove(file_name)
                    else:
                        return 0

            # récupération du nombre total de page
            nombre_page_string = soup.find("li", class_="current").string
            n = int(get_last_digit(nombre_page_string))

            print("Extraction de la page "+str(i)+" sur "+str(n))

            # récupération des urls des livres
            all_books_h3 = soup.find_all("h3")
            all_books_url = []
            for book in all_books_h3:
                all_books_url.append(book.a["href"].replace('../../..', "http://books.toscrape.com/catalogue"))

            # Scrap all books
            for book_url in all_books_url:
                scrap_article(book_url)

            # url de la page suivante
            url_category_next = "page-"+str(i+1)+".html"
            url_category = url_category_racine + url_category_next

        else:
            print("Url de la catégorie inatteignable")

        if i >= n:
            break


scrap_category("http://books.toscrape.com/catalogue/category/books/mystery_3/index.html")

