import streamlit as st
import variable_store
import requests, json, pandas as pd, numpy as np
from bs4 import BeautifulSoup
from selectorlib import Extractor
from time import sleep
from bokeh.plotting import figure
def app():
    if variable_store.product != None:
        title_value = 'Price comparison for ' + variable_store.product 
        st.header(title_value)
        ams_price = scrape_ams('https://www.amazon.com/Waterproof-Case-Pelican-Storm-iM2050/dp/B00162LTII')
        st.write('Amazon Price for the product - ',ams_price['price'])
        x = [1, 2, 3]
        y = ['54', '70', '66']
        p = figure(title='simple line example',x_axis_label='Amazon        -         Walmart        -         Ebay',  y_axis_label='Cost')
        p.line(x, y, line_width=1)
        st.bokeh_chart(p, use_container_width=False)
    else:
        st.write(variable_store.product_error_msg)

def scrape_ams(url):  
    e = Extractor.from_yaml_file('selectors.yml')
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    print(e.extract(r.text))
    return e.extract(r.text)

# product_data = []
# with open("urls.txt",'r') as urllist, open('output.jsonl','w') as outfile:
#     for url in urllist.read().splitlines():
#         data = scrape(url) 
#         if data:
#             json.dump(data,outfile)
#             outfile.write("\n")
#             # sleep(5)