from bs4 import BeautifulSoup
import requests

url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

datatype_table = soup.find(class_='wikitable')
body = datatype_table.find('tbody')
rows = body.find_all('tr')[1:]
lst_mutable = []
lst_immutable = []

for row in rows:
  data0= row.find_all('td')[0].get_text().strip()
  data1= row.find_all('td')[1].get_text().strip()

  lst_mutable.append(data0) if data1 == "mutable" else lst_immutable.append(data0)

print("mutable dta types ==> ", lst_mutable)
print("immutable dta types ==> ", lst_immutable)
