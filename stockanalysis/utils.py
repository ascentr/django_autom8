from bs4 import BeautifulSoup
import requests

def scrape_stock_data(symbol):

  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
  
  url = f'https://finance.yahoo.com/quote/{symbol}/'
  try:
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
      soup = BeautifulSoup(response.content, 'html.parser')
      current_price = soup.find(f'fin-streamer',{'class':'livePrice yf-mgkamr'}, {'data-symbol': {symbol}})['data-value']
      previous_close_price = soup.find('span', {'class':'value yf-tx3nkj'}).text
      price_changed = soup.find(f'fin-streamer', {'class':'priceChange yf-mgkamr'}, {'data-symbol': {symbol}}).span.text
      percentage_changed = soup.find(f'fin-streamer',{'data-testid':'qsp-price-change-percent'}   ,{'data-symbol': {symbol}}).span.text

      # price_changed = soup.find(f'fin-streamer', {'class':'priceChange yf-mgkamr'}, {'data-symbol': {symbol}})['data-value']
      # percentage_changed = soup.find(f'fin-streamer',{'data-testid':'qsp-price-change-percent'}   ,{'data-symbol': {symbol}})['data-value']
      week_52_range = soup.find('fin-streamer', {'data-field':'fiftyTwoWeekRange'}, {'data-symbol': {symbol}}).text
      week_52_low, week_52_high = week_52_range.split(' - ') 
      market_cap = soup.find('fin-streamer', {'data-field':'marketCap'}, {'data-symbol': {symbol}}).text
      pe_ratio = soup.find('fin-streamer', {'data-field':'trailingPE' },{'data-symbol': {symbol}})['data-value']
      dividend_yield = soup.find('fin-streamer', { }, {'data-symbol': {symbol}})

      #find the forward yield
      quote_stats = soup.find('div', {'data-testid':'quote-statistics'})
      target_ul = quote_stats.find('ul')
      list_items = target_ul.find_all('li')
      dividend_yield = list_items[13].find('span', class_='value').text

      stock_response = {
        'current_price' : current_price ,
        'previous_close_price' : previous_close_price ,
        'price_changed':price_changed ,
        'percentage_changed': percentage_changed,
        'week_52_low':week_52_low,
        'week_52_high':week_52_high,
        'market_cap':market_cap,
        'pe_ratio':pe_ratio,
        'dividend_yield':dividend_yield,
      }
      return stock_response

  except Exception as e:
    print(f"Data Scraping Error :{e}")
    return None