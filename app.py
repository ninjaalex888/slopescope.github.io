from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import re
import requests

def scrape_loveland_base():
    l = []
    url = 'http://skiloveland.com/snow-report/'
    r=requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    base = soup.find('span', {'class' : 'mid-mtn-total'})
    return base.text



def scrape_abasin_base():
    l = []
    url = 'https://www.arapahoebasin.com/snow-conditions/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    for elem in soup(text=re.compile('Base')):
        print("test \n")

        print(elem)
        print("test \n")

        if len(elem) == 4:
            return elem.parent.findPrevious('div', {"class":"ab-condition_value"}).text

app = Flask(__name__)

@app.route('/<string:index>/', methods=['GET','POST'])
def my_form_post(index):
    basin_base = scrape_abasin_base()
    loveland_base = scrape_loveland_base()
    print loveland_base
    return render_template('%s.html' % index, aBayBase=basin_base, lovelandBase = loveland_base)

if __name__ == "__main__":
    app.run(debug=True)