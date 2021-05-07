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
    counter = 0
   
    #get species directories in webpage
    for a in soup.select(".thumbinner a"):
        name= counter
        pagelink= a['href']
        url = pagelink.replace("/wiki/","https://en.wikipedia.org/wiki/")
        print("accessing wikipage: ", url)            
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        
        for link in soup.select(".fullImageLink a img"):
            imagelink = (link["src"])
            print("new image link", imagelink)
            imagelink = imagelink.replace("//","https://")
            counter= counter +1   
            if(counter % 2) ==0 :
                #save image at link and simplify filename to relevant information
                with open(str(name) + '.jpg', 'wb') as f:
                    im = requests.get(imagelink)
                    f.write(im.content)
                    print('Writing: ' ,imagelink)
                
        #convert mushroom directories to link
        #u = a["href"].replace("/mushrooms/", "http://www.foragingguide.com/mushrooms/")
        #print link
        #print("accessing: ", u)

        #r = requests.get(u)
        #soup = BeautifulSoup(r.text, "html.parser")
        
        #loop through images on page 
        #for b in soup.find_all(rel="lightbox[photos]"):
        #for b in soup.select(".thumb_div a"):
        #    imagelink = b["href"]
        #    print("accessing image: ", imagelink)
        #    name = imagelink

            #save image at link and simplify filename to relevant information
        #    with open(name.replace('http://static.foragingguide.com/photos/mushrooms/','').replace(' ', '-').replace('/', '').replace('.JPG','').replace('.jpg','') + '.jpg', 'wb') as f:
        #        im = requests.get(imagelink)
        #        f.write(im.content)
        #        print('Writing: ' ,imagelink)



if edible == True:
        imagedown('https://en.wikipedia.org/wiki/Category:Edible_fungi', 'wikipedia_edible')


if edible == False:
    imagedown('https://en.wikipedia.org/wiki/List_of_poisonous_fungus_species', 'wikipedia_poisonous')
