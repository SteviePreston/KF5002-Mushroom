import requests
from bs4 import BeautifulSoup
import os

#declare with you want to scrape edible mushrooms or not (poisonous)
edible = False

def imagedown(url, folder):
    #creates new directory for storing images when starting scrape
  
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except:
        pass
    os.chdir(os.path.join(os.getcwd(), folder))
    #parse webpage 
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    #get species directories in webpage
    for a in soup.select(".info a"):
        #convert mushroom directories to link
        u = a["href"].replace("/mushrooms/", "http://www.foragingguide.com/mushrooms/")
        #print link
        print("accessing: ", u)

        r = requests.get(u)
        soup = BeautifulSoup(r.text, "html.parser")
        
        #loop through images on page 
        #for b in soup.find_all(rel="lightbox[photos]"):
        for b in soup.select(".thumb_div a"):
            imagelink = b["href"]
            print("accessing image: ", imagelink)
            name = imagelink

            #save image at link and simplify filename to relevant information
            with open(name.replace('http://static.foragingguide.com/photos/mushrooms/','').replace(' ', '-').replace('/', '').replace('.JPG','').replace('.jpg','') + '.jpg', 'wb') as f:
                im = requests.get(imagelink)
                f.write(im.content)
                print('Writing: ' ,imagelink)

if edible == True:
        imagedown('http://www.foragingguide.com/mushrooms/edible_by_common_name', 'foragingguide_edible')


if edible == False:
    imagedown('http://www.foragingguide.com/mushrooms/poisonous_by_common_name', 'foragingguide_poisonous')
