#!/usr/bin/env python
# coding: utf-8

# In[18]:


pip install beautifulsoup4


# In[1]:


import requests
from bs4 import BeautifulSoup


# In[20]:


pip install lxml 


# # Варіант 3

# In[2]:


URL= 'https://smallpacking.agrosem.ua/shop/'


HEADERS = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'http://localhost:8888/',
    'Accept-Language': 'en,en-US;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-GB;q=0.6',
}

def get_html(URL, params = None):
    r = requests.get(URL, headers = HEADERS, params = params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_ = 'page-numbers')[-2].text
    if soup != None:
        return pagination
      
def parse():
    html = get_html(URL)
    if html.status_code == 200:
        pages_count = int(get_pages_count(html.text))
        for page in range(1, pages_count +1):
            print(f'Парсинг сторінки {page} з {pages_count}')
            html = get_html(URL, params = {'page': page})
            
            soup = BeautifulSoup(html, 'html.parser')
            items = soup.find_all('div', class_ = 'product-from-category-container')
            
            if len(items) > 0:
                for item in items:
                    product_link = item.find('a').get('href')
                    if len(product_link) > 0:    
                        links = requests.get(product_link)
                        soup2 = BeautifulSoup(links.content, 'html.parser')
                        item = soup2.find_all('div', class_ = 'atributes-description')
                        products = []
                        products.append({
                            'title': item.find.h2.text,
                            'price': item.find('span', class_ = 'regular-price').get_text().replace("грн", "").replace(" ", ""),
                            'SKU': item.find('span',{'itemprop' : 'productID', 'class' : 'sku'}).get_text(),   
                            'weight': item.find('tr', {'class' : 'woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_vaga'}).get_text()         
                         })


                        return products

                        print(products)

                    else:
                        print('Error')

parse()

