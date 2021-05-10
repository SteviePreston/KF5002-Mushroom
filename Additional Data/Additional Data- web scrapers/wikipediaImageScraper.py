import requests
from bs4 import BeautifulSoup
import os
from requests.exceptions import ConnectionError

#declare with you want to scrape edible mushrooms or not (poisonous)
edible = True

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
    #gets all categories
    categories = soup.select(".mw-category-group")
    #iterate through catefories
    for cat in categories:
        try:
            #find the h3 text
            catTitle = cat.find("h3").text
            #discard unwanted categories, which are identified by their catTitle
            if catTitle != "*" and catTitle != " ":
            #iterate through wanted categories
                for a in cat.find_all('a', href=True):
                    #get pagelink and turn it into usable url
                    pagelink= a['href']
                    url = pagelink.replace("/wiki/","https://en.wikipedia.org/wiki/")
                    print("accessing wikipage: ", url)
                    
                    r = requests.get(url)
                    soup = BeautifulSoup(r.text, "html.parser")
                    try:
                        for link in soup.find("tbody").find_all("a", "image"):
                            imagelink = (link['href'])
                            imagelink = imagelink.replace("/wiki/","https://en.wikipedia.org/wiki/")
                            print(imagelink)
                            try:
                                #access imagelink and create soup of image page
                                url = imagelink
                                r = requests.get(url)
                                soup = BeautifulSoup(r.text, "html.parser")

                                for link in soup.select(".fullImageLink a img"):
                                    
                                    imagelink = (link["src"])
                                    print("new image link", imagelink)
                                    imagelink = imagelink.replace("//","https://")
                                    name= imagelink
                                #save image at link and simplify filename to relevant information
                                    with open(name.replace('https://en.wikipedia.org/wiki/','').replace(' ', '-').replace('/', '').replace('.JPG','').replace('.jpg','') + '.jpg', 'wb') as f:
                                        im = requests.get(imagelink)
                                        f.write(im.content)
                                        print('Writing: ' ,imagelink)

                            except requests.exceptions.ConnectionError as e:
                                pass
                            except Exception as e:
                                logger.error(e)
                                randomtime = random.randint(1,5)
                                logger.warn('ERROR - Retrying again website %s, retrying in %d secs' % (url, randomtime))
                                time.sleep(randomtime)
                                continue
                    except AttributeError as AE:
                        pass
        except ConnectionError as CE:
            pass            

        

                
                   

if edible == True:
        imagedown('https://en.wikipedia.org/wiki/Category:Edible_fungi', 'wikipedia_edible')


if edible == False:
    imagedown('https://en.wikipedia.org/wiki/List_of_poisonous_fungus_species', 'wikipedia_poisonous')
