from bs4 import BeautifulSoup
import requests


def scrape_stock_data(symbol):

  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
  
  url = f'https://finance.yahoo.com/quote/{symbol}/'
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, 'html.parser')
  current_price = soup.find(f'fin-streamer',{'class':'livePrice yf-mgkamr'}, {'data-symbol': {symbol}})['data-value']
  previous_close_price = soup.find('span', {'class':'value yf-tx3nkj'}).text

  quote_stats = soup.find('div', {'data-testid':'quote-statistics'}, {'data-symbol':{symbol}})
  my_ul = quote_stats.find('ul')
  list_items = my_ul.find_all('li')
  dividend_yield = list_items[13].find('span', class_='value').text
  # target_item = list_items[13]

  # yield_value = target_item.find('span', class_='value').text

  # label = nth_li.find('span', class_='label').get_text(strip=True)
  # value = nth_li.find('span', class_='value').get_text(strip=True
  # dividend_yield = list_items[13].find('span', {'class':'value'}).text
  # print('current_price ==>' , current_price)
  # print('previous close price ==>', previous_close_price)
  print(symbol ,'>>>' , dividend_yield)
scrape_stock_data('AAPL')
