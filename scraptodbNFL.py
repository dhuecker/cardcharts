import requests
from bs4 import BeautifulSoup
import pandas as pd
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime 
from datetime import datetime
import pytz

#tz = pytz.timezone*'United'

cred = credentials.Certificate("cardchar-edd6a-firebase-adminsdk-pld8f-edafff092b.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Temporarily replace quote function
def noquote(s):
    return s
pyrebase.pyrebase.quote = noquote

card = db.collection(u'cards').document(u'tom brady')

card.set({
    u'soldprice': True
}, merge=True)


def main():

    
    

    searchterm = '+brees+rookie+card'
    url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={searchterm}&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1"
    soup = get_data(url)
    products = parse(soup, searchterm)
    #temp = db.child("cards").order_by_child("title").start_at("tom brady").order_by_child("soldprice").start_at(100).limit_to_first(2).get()
    #print(temp.val())

    #export(products, searchterm)

def get_data(url):

    r = requests.get(url)
    if r.status_code != 200:
        print('Failed to get data: ', r.status_code)
    else:
        soup = BeautifulSoup(r.text, 'html.parser')
        print(soup.title.text)
    return soup

def parse(soup, searchterm):
    search = "tom brady"
    collection_id = "cards"
    i = 0
    productlist = []
    results = soup.find_all('div', {'class': 's-item__info clearfix'})
    for item in results:
        products = {
        'title': item.find('h3', {'class':'s-item__title s-item__title--has-tags'}).text,
        'soldprice': float(item.find('span', {'class':'s-item__price'}).text.replace('$','').replace(',','').strip()),
        'solddate': item.find('span', {'class': 's-item__title--tagblock__COMPLETED'}).find('span', {'class':'POSITIVE'}).text,
        
        'link': item.find('a', {'class': 's-item__link'})['href']        
        }
        temp1 = item.find('h3', {'class':'s-item__title s-item__title--has-tags'}).text
        temp2 =  float(item.find('span', {'class':'s-item__price'}).text.replace('$','').replace(',','').strip())
        temp3 = item.find('span', {'class': 's-item__title--tagblock__COMPLETED'}).find('span', {'class':'POSITIVE'}).text
     
        
        productlist.append(products)
    
        data = {"title": temp1, "soldprice":temp2, "solddate": temp3, "sitesold": "ebay"}
        db.collection(collection_id).add(data)
        i = i +1
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

