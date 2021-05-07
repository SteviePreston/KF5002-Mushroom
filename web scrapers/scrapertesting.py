import requests
from bs4 import BeautifulSoup


end_point = "http://www.foragingguide.com/mushrooms/sp/amethyst_deceiver"
response = requests.get(end_point).text
soup = BeautifulSoup(response, "lxml").select(".thumb_div a")
print("\n".join(i["href"] for i in soup))