from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

def flatten_dict_to_list(nested_dict):
    return [nested_dict[key] for key in nested_dict if isinstance(nested_dict, dict)]

def scrape_data():
    url = "https://coinmarketcap.com/currencies/"
    page = requests.get(url)
    # print(page)

    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup.prettify())
    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    coin_data = json.loads(data.contents[0])

    # print("Extracted Coin Data:")
    # print(json.dumps(coin_data, indent=2))
    # with open('coin_data.json', 'w', encoding='utf-8') as f:
    #     json.dump(coin_data, f, ensure_ascii=False, indent=2)
    #     print("Data has been written to coin_data.json")

    listings = json.loads(coin_data['props']['initialState'])['cryptocurrency']['listingLatest']['data']

    make_keys = listings[0]
    prep_keys = flatten_dict_to_list(make_keys)
    keys = prep_keys[0]

    new_listings = [dict(zip(keys, l)) for l in listings[1:]]
    # print(len(new_listings))

    coins = {}    
    for i in new_listings:
        coins[str(i['id'])] = i['symbol']

    coin_name = []
    coin_symbol = []
    market_cap = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []
    price = []
    volume_24h = []
    volume_7d = []

    for i in new_listings:
        coin_name.append(i['name'])
        coin_symbol.append(i['symbol'])
        price.append(i['quote.USD.price'])
        percent_change_1h.append(i['quote.USD.percentChange1h'])
        percent_change_24h.append(i['quote.USD.percentChange24h'])
        percent_change_7d.append(i['quote.USD.percentChange7d'])
        market_cap.append(i['quote.USD.marketCap'])
        volume_24h.append(i['quote.USD.volume24h'])
        volume_7d.append(i['quote.USD.volume7d'])
        
    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'price', 'volume_24h', 'volume7d'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percent_change_1h'] = percent_change_1h
    df['percent_change_24h'] = percent_change_24h
    df['percent_change_7d'] = percent_change_7d
    df['market_cap'] = market_cap
    df['volume_24h'] = volume_24h
    df['volume_7d'] = volume_7d
    return df