#!/usr/bin/env python
# coding: utf-8

# In[18]:


pip install beautifulsoup4


# In[174]:


import requests
from bs4 import BeautifulSoup


# In[20]:


pip install lxml 


# # Варіант №1
# Парсинг сторінки зі списком продуктів. Код працює, але з неї можна отримати лише 2 показники — назву й ціну

# In[ ]:


URL = 'https://smallpacking.agrosem.ua/shop/'


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
    
    
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_ = 'product-from-category-container') 

    products = []
    for item in items:
        products.append({
                'title': item.find('span', class_ = 'pruduct-name-bottom').get_text(),
                'price': item.find('span', class_ = 'regular-price').get_text().replace("грн", "").replace(" ", "")
         })
    return products 
    
    
    
def parse():
    html = get_html(URL)
    if html.status_code == 200:
        products = []
        pages_count = int(get_pages_count(html.text))
        for page in range(1, pages_count +1):
            print(f'Парсинг сторінки {page} з {pages_count}')
            html = get_html(URL, params = {'page': page})
            products.extend(get_content(html.text))
 
        print(products)

    else:
        print('Error')

parse()


# # Варіант 2
# Намагалась отримати ще 2 параметри (SKU і вагу), які находяться на сторінці конкретного (кожного продукту). Тобто в коді треба врахувати переходи ще на сторінки продуктів. Не вийшло це зробити. Намагалась писати окрему функцію для goods, але тоді незрозуміло, що треба ще додати в def parse()

# In[ ]:


URL = 'https://smallpacking.agrosem.ua/shop/'


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
    
    
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_ = 'product-from-category-container')
    
    for item in items:
        product_link = item.find('a').get('href')

    return product_link 
    

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        pages_count = int(get_pages_count(html.text))
        for page in range(1, pages_count +1):
            print(f'Парсинг сторінки {page} з {pages_count}')
            html = get_html(URL, params = {'page': page})
            
            soup2 = BeautifulSoup(product_link, 'html.parser')
            goods = soup2.find_all('div', class_ = 'atributes-description')
            products = []
            for good in goods:
                products.append({
                    'title': good.find.h2.text,
                    'price': good.find('span', class_ = 'regular-price').get_text().replace("грн", "").replace(" ", ""),
                    'SKU': good.find('span',{'itemprop' : 'productID', 'class' : 'sku'}).get_text(),   
                    'weight': good.find('tr', {'class' : 'woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_vaga'}).get_text()         
         })
        
            
        return products
 
        print(products)

    else:
        print('Error')

parse()

