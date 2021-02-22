import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
conn = sqlite3.connect('cardcharts')
c = conn.cursor()
#c.execute('''CREATE TABLE nba(title TEXT, soldprice REAL, solddate TEXT)''')
def main():
    searchterm = 'lebron+james+rookie+card'
    url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={searchterm}&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1"
    soup = get_data(url)
    products = parse(soup)
    conn.commit()
    print('complete.')
    c.execute('''SELECT * FROM nba''')
    results = c.fetchall()
    print(results)
    #export(products, searchterm)

def get_data(url):
    r = requests.get(url)
    if r.status_code != 200:
        print('Failed to get data: ', r.status_code)
    else:
        soup = BeautifulSoup(r.text, 'html.parser')
        print(soup.title.text)
    return soup

def parse(soup):
    productlist = []
    results = soup.find_all('div', {'class': 's-item__info clearfix'})
    for item in results:
        products = {
        'title': item.find('h3', {'class':'s-item__title s-item__title--has-tags'}).text,
        'soldprice': float(item.find('span', {'class':'s-item__price'}).text.replace('$','').replace(',','').strip()),
        'solddate': item.find('span', {'class': 's-item__title--tagblock__COMPLETED'}).find('span', {'class':'POSITIVE'}).text,
        
        'link': item.find('a', {'class': 's-item__link'})['href']        
        }
        temp = item.find('h3', {'class':'s-item__title s-item__title--has-tags'}).text
        temp2 =  float(item.find('span', {'class':'s-item__price'}).text.replace('$','').replace(',','').strip())
        temp3 = item.find('span', {'class': 's-item__title--tagblock__COMPLETED'}).find('span', {'class':'POSITIVE'}).text
        c.execute('''INSERT INTO nba VALUES(?,?,?)''',(temp, temp2, temp3))
        productlist.append(products)
        #print(products)
    return productlist

def loadup(productlist):
    return

def export(productlist, seachterm):
    productsdf = pd.DataFrame(productlist)
    productsdf.to_csv(seachterm +'testoutput.csv', index=False)
    print('Saved to CSV')
    return


if __name__ == '__main__':
    main()

