import requests
from bs4 import BeautifulSoup
import os

#declare with you want to scrape edible mushrooms or not (poisonous)
edible = True

def imagedown(url, folder):
    #creates new directory for storing images when starting scrape
    if page < 1:
        try:
            os.mkdir(os.path.join(os.getcwd(), folder))
        except:
            pass
        os.chdir(os.path.join(os.getcwd(), folder))
    #parse webpage 
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    #get image directories in webpage
    for a in soup.select(".image a"):
        #convert image directories to link
        u = a["href"].replace("/../", "https://www.mushroom.world/")
        #print link
        print(u)
        name = u
        #save image at link and simplify filename to relevant information
        with open(name.replace('https://www.mushroom.world/data/fungi/','').replace(' ', '-').replace('/', '').replace('.JPG','').replace('.jpg','') + '.jpg', 'wb') as f:
            im = requests.get(u)
            f.write(im.content)
            print('Writing: ' ,u)

if edible == True:
    #sets initial page of scape to 0
    page = 0
    #8 pages of edible mushrooms
    max_pages = 8
    while page <= max_pages: 
        imagedown('http://www.mushroom.world/mushrooms/edible?page='+str(page), 'edible')
        page = page+1

if edible == False:
    #sets initial page of scape to 0
    page = 0
    #4 pages of poisonous mushrooms
    max_pages = 4
    while page <= max_pages: 
        imagedown('http://www.mushroom.world/mushrooms/poisonous?page='+str(page), 'poisonous')
        page = page+1


