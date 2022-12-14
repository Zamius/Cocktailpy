import requests
import json
from string import digits, ascii_lowercase as INITIALS
from itertools import chain
from shutil import copyfileobj
from PIL import Image

import sys
import os

#Internet connection check
try:
    internet = requests.get("https://www.httpbin.org/status/200")
except:
    print("YOU DON'T HAVE INTERNET ACCESS, CLOSING PROGRAM!")
    sys.exit()

#OS CHECK
os_ = sys.platform
if os_ == "win32":
    pass
else:
    print("#@#LINUX DETECTED, CORRECT FUNCTIONING OF THIS PROGRAM IS NOT GUARANTEED (TESTED FOR WINDOWS ONLY)#@#")

#COLOR FOR COMMAND PROMPT
class Colors:
    def r():
        os.system("color 4")
    def b():
        os.system("color 3")
    def y():
        os.system("color E")


c = Colors

def logo():
    LOGO = """
   _____                  _      _             _   _   _____    ____  
  / ____|                | |    | |           (_) | | |  __ \  |  _ \ 
 | |        ___     ___  | | __ | |_    __ _   _  | | | |  | | | |_) |
 | |       / _ \   / __| | |/ / | __|  / _` | | | | | | |  | | |  _ < 
 | |____  | (_) | | (__  |   <  | |_  | (_| | | | | | | |__| | | |_) |
  \_____|  \___/   \___| |_|\_\  \__|  \__,_| |_| |_| |_____/  |____/                                                                                                                                           
"""
    print(LOGO)
    
HELP = """[INTRO]
-h OR --help: Show this menu.

[COCKTAIL DATABASE]
-s: Search cocktail by name.
-r: Returns information for a random cocktail!
-i: Search information for a cocktail ingredient!

--byi: Returns a list of cocktails that contain a specified ingredient.
--bys INITIAL: Returns a list of cocktails starting by a letter (example: --searchby a)
--img: Download an image of a cocktail and open it.
"""

LOGO = r"""
()   ()      ()    /
  ()      ()  ()  /
   ______________/___
   \            /   /  Pythonic
    \^^^^^^^^^^/^^^/
     \     ___/   /
      \   (   )  /  
       \  (___) /        Cocktails...
        \ /    /        
         \    /
          \  /
           \/
           ||
           ||
           ||
           ||
           ||
           /\
          /;;\
     ==============
"""

#Functions for each api request and information choice
def search_cocktail(name:str, random:bool = False) -> str:
    if not random:
        URL = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={name}"
    else:
        URL = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
        
    try:
        req = requests.get(URL)
        content = json.loads(req.text)

        #Access stuff
        content = content["drinks"]

        if not content:
            os.system("color E")
            return print(f"\nNothing found for {name}!\n")
        
    except Exception as ex:
        os.system("color 4")
        return print(f"\nUh Oh, something was done wrong!\nDetails: {ex}")

    #print(content)

    #Access every dictionary in list and gather values
    for c,element in enumerate(content,start=1):
        print(f"\n\n===COCKTAIL VARIATION {c}===\n" if len(content) > 1 else "")
        #strIngredients and strMeasures
        ing = [f"strIngredient{x}" for x in range(1, 21)]
        msr = [f"strMeasure{x}" for x in range(1, 21)]
        ingredients = []
        measures = []

        #Get all possible existing ingredients in a range from 1 to 20
        for n in ing:
            try:
                current_ingredient = element[n]
                ingredients.append(current_ingredient)
            except:
                continue
        for n in msr:
            try:
                current_measure = element[n]
                measures.append(current_measure)
            except:
                continue
            
        #Remove NoneType values
        ingredients = list(filter(lambda x: x is not None, ingredients))
        measures = list(filter(lambda x: x is not None, measures))

        #Assign number on each elemnt
        for i in range(len(measures)):
            measures[i] = f"[{str(i+1)}] {measures[i]}" #Assign the number i that takes the value of each list's index and format it to the ingredients name (weird to explain)

        m_i = list(zip(measures,ingredients))
        
        #Get info
        name = element["strDrink"]
        category = element["strCategory"]
        glass:str = element["strGlass"]
        alcohol: str = ["Yes" if element["strAlcoholic"] == "Alcoholic" else "No"]
        instructions: str = element["strInstructions"]
        
        #PRINTING
        print(f"#Cocktail name: {name.title()}")
        print(f"#Category: {category}")
        print(f"#Glass: {glass}")
        print(f"#Alcoholic: {alcohol[0]}")
        print("\n###INGREDIENTS###")
        for x in m_i:
            print(f"{x[0]}-> {x[1]}")
        print(f"\n###INSTRUCTIONS###\n{instructions}")
    

#Search by initial
def search_by_initial(initial:str) -> str:
    URL = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={initial}"

    try:
        req = requests.get(URL)
        content = json.loads(req.text)

        #Access stuff
        content = content["drinks"]
        if not content:
            os.system("color E")
            return print(f"\nNothing found for {initial}!\n")
    except Exception as ex:
        c.r()
        return print(f"\nUh Oh, something was done wrong!\nDetails: {ex}")

    #Get list of values for key -> "strDrink" from json
    drinks = [dic["strDrink"] for dic in content]

    print(f"Found {len(drinks)} cocktails!\n")
    for count, cocktail in enumerate(drinks,start=1):
        print(f"[{count}] {cocktail}")

def search_ingredient(name:str) -> str:
    URL = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?i={name}"

    try:
        req = requests.get(URL)
        content = json.loads(req.text)

        #Access stuff
        content = content["ingredients"]
        if not content:
            os.system("color E")
            return print(f"\nNothing found for {name}!\n")
        
    except Exception as ex:
        c.r()
        return print(f"\nUh Oh, something was done wrong!\nDetails: {ex}")

    cn = content[0]
    name: str = cn["strIngredient"]
    desc: str = cn["strDescription"]
    type_: str = cn["strType"]
    has_alcohol: str = "Yes" if cn["strAlcohol"] == "Yes" else "No"

    print(f"NAME: {name}\n")
    print(f"###DESCRIPTION###\n")
    print(desc)
    print(f"\nType: {type_}")
    print(f"Alcoholic: {has_alcohol}")

def search_by_ingredient(ingredient:str) -> str:
    URL = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={ingredient}"

    try:
        req = requests.get(URL)
        content = json.loads(req.text)

        #Access stuff
        content = content["drinks"]
        if not content:
            os.system("color E")
            return print(f"\nNothing found for {ingredient}!\n")
        
    except Exception as ex:
        c.r()
        return print(f"\nUh Oh, something was done wrong!\nDetails: {ex}")

    
    #Get values of each dictionary in list
    values = [cnt["strDrink"] for cnt in content]

    for count, v in enumerate(values, start=1):
        print(f"[{count}] {v}")


def get_img(cocktail:str) -> str:
    URL = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={cocktail}"

    try:
        req = requests.get(URL)
        content = json.loads(req.text)

        #Access stuff
        content = content["drinks"]
        if not content:
            os.system("color E")
            return print(f"\nNothing found for {cocktail}!\n")
        
    except Exception as ex:
        c.r()
        return print(f"\nUh Oh, something was done wrong!\nDetails: {ex}")

    cocktail_name = content[0]["strDrink"]
    thumbnail_url = content[0]["strDrinkThumb"]
    file = cocktail_name + ".jpg"
    
    #Save file
    try:
        image_req = requests.get(thumbnail_url, stream=True)
        
        if image_req.status_code == 200:
            with open(file, 'wb') as fl:
                copyfileobj(image_req.raw,fl)
            print(f"\nFile saved in {os.path.join(os.getcwd(), file)}")
            img = Image.open(file).show()
        else:
            raise Exception(f"{thumbnail_url} returned status code: {image_req.status_code}")
            
    except Exception as ex:
        c.r()
        print(f"\n{ex}\n")
        return
    
    
    
    
def main():
    if len(sys.argv) == 2:
        
        #Commands here
        cmd = sys.argv[1]

        match cmd:

            #COMMANDS MENU
            case "-h":
                print(HELP)
                return

            case "--help":
                print(HELP)
                return

            #Search for cocktail by name
            case "-s":
                #Question and "left-blank" check
                while True:
                    n = input("Enter a cocktail to search: ")

                    if not n:
                        c.y()
                        print("\nYou can't leave this field empty!\n")
                        continue
                    break

                c.b()
                
                search_cocktail(n)
                return

            case "-r":
                search_cocktail("",True)
                return

            case "-i":
                #Question and "left-blank" check... again
                while True:
                    n = input("Enter an ingredient to search: ")

                    if not n:
                        c.y()
                        print("\nYou can't leave this field empty!\n")
                        continue
                    break

                c.b()
                search_ingredient(n)
                return

            case "--byi":
                #Question and "left-blank" check... again
                while True:
                    n = input("Enter ingredient: ")

                    if not n:
                        c.y()
                        print("\nYou can't leave this field empty!\n")
                        continue
                    break

                c.b()
                print(f"THE FOLLOWING COCKTAILS CAN BE MADE WITH {n.upper()}\n")
                search_by_ingredient(n)
                return

            #Search for cocktail by name (get image url)
            case "--img":
                #Question and "left-blank" check
                while True:
                    n = input("Enter a cocktail to search: ")

                    if not n:
                        c.y()
                        print("\nYou can't leave this field empty!\n")
                        continue
                    break

                c.b()
                
                get_img(n)
                return

            case _:
                c.r()
                print("This command does nothing!\n".upper())
                return
            
    #EXAMPLE: cocktaildb.py --command 3rd_argument
    elif len(sys.argv) == 3:
        cmd1 = sys.argv[1]
        cmd2 = sys.argv[2]

        #Get list of cocktails by initial ^_^
        if cmd1 == "--bys" and cmd2:
            cmd2 = cmd2.lower()

            #Error handling
            if not cmd2 in list(chain(INITIALS,digits)):
                c.r()
                print("\nPlease enter a valid letter! (Example: \"a\")\n")
                return

            search_by_initial(cmd2)
            return

    #No command given
    else:
        c.y()
        print("Type --help or -h for a list of commands!\n")
        return

if __name__ == "__main__":
    #DEFAULT COLOR and clear screen
    if os_ == "linux":
        os.system("clear")
    else:
        os.system("cls")
    c.b()
    
    NAME = sys.argv[0].split("\\")[-1]
    logo()
    print(f"WELCOME TO {NAME.upper()}!\nAPI: https://www.thecocktaildb.com/api.php\n")
    
    main()
    print("\n" + LOGO)
