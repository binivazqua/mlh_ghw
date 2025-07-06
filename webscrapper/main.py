import requests 
from bs4 import BeautifulSoup
import json
import os


# Sitio web base a stalkear
URL_ENDPOINT = "https://pizza-site-six.vercel.app/"

# Realizamos un request al sitio añadiendo la ruta deseada
res = requests.get(URL_ENDPOINT + "/recipes");

# Usamos BeautifulSoup para parsear el contenido HTML
soup = BeautifulSoup(res.text)

# Buscamos todos los elementos <a> que tengan la clase específica. Usamos el anchor para poder acceder a toda la información de la receta
anchor_list = soup.find_all("a", attrs={"class": "inline-block mt-4 px-4 py-2 bg-[#d32f2f] text-white rounded-lg hover:bg-[#b71c1c] transition-colors duration-300"})

#print(anchor_list)
#Creamos aquí afuera un dictionary para guardar las recetas
recipes = {}
# Iteramos sobre cada elemento del dataset y hacemos una búsqueda más profunda con otro request.
for anchor in anchor_list:
    # repetimos el request para acceder a la page de cada receta
    res = requests.get(URL_ENDPOINT + anchor["href"])
    recipe = BeautifulSoup(res.text)

    # Obtenemos el título de la receta
    title = recipe.h1.text

    #Obtenemos la imagen de la receta
    image = recipe.img["src"]

    # Obtenemos los ingredientes de la receta:

    # 1. Buscamos el header de ingredientes como punto de partida.
    ing_header = recipe.find("h2", attrs={"class": "text-3xl font-bold text-[#4e342e] mb-6 flex items-center"})


    # 2. Sabemos que el siguiente span contiene el texto de cada ingrediente, por lo que buscamos todos los span que estén dentro de un div con la clase "flex flex-col gap-2"
    ing_list = ing_header.next_sibling.find_all("span", attrs={"class": "text-[#4e342e] font-medium"})

    # 3. Añadimos los ingredientes a una lista
    ingredients = []
    for ing in ing_list:
        ingredients.append(ing.text)
    
    # Obtenemos el health score de la receta
    info_container = recipe.find("div", attrs={"class": "text-center p-4 bg-[#fffdf6] rounded-lg"})
    health_score_info = info_container.next_sibling.find("div", attrs= {"class": "text-2xl font-bold text-[#d32f2f] mb-2"})

    health_score = health_score_info.text

    # Imprimimos la información de la receta
    # print(f"Title: {title}")
    # print(f"Image: {image}")
    # print(f"Ingredients: {', '.join(ingredients)}")
    # print(f"Health Score: {health_score}")

    # Añadimos todos los dartos a un diccionario para mayor orden
    recipes[anchor["href"]] = {
        "title": title,
        "image": image,
        "ingredients": ingredients,
        "health_score": health_score
    }
    
output_path = os.path.join(os.path.dirname(__file__), "recipes.json")
with open(output_path, "w", encoding="utf-8") as f:
     json.dump(recipes, f, ensure_ascii=False, indent=4)

print(recipes)

    