import requests
from bs4 import BeautifulSoup
import csv


# charger les données dans un fichier csv
def save_data(nom_fichier, en_tete, list_data):
    with open(nom_fichier, 'w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(en_tete)
        writer.writerow(list_data)


# sauvegarder l'image
def transfert_image(url_img, file_name):
    # Send GET request
    response = requests.get(url_img)
    # Save the image
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
        # nom du fichier
        file_data_name = "Data/" + category + "/" + "book_" + title_reformat + ".csv"
        # nom du fichier image
        file_img_name = "Data/" + category + "/" + "book_img_" + title_reformat + ".jpg"

        save_data(file_data_name, en_tete, data)
        transfert_image(image_url, file_img_name)
    else:
        print("Url de l'article unreadable")


# url de l'article
url = "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
scrap_article(url)
