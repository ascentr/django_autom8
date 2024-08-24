from bs4 import BeautifulSoup
import requests

url = 'https://webscraper.io/test-sites/tables'
#url='https://www.richardkendall.co.uk/properties?eapowquicksearch=1&limitstart=0'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
headings1 = soup.find_all('h1')
headings2 = soup.find_all('h2')
tables = soup.find_all('table')
my_table = tables[1]
rows = my_table.find_all('tr')[1:]

last_names = []
for row in rows:
  last_names.append(row.find_all('td')[2].get_text())

print(last_names)


