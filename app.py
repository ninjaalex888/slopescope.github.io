from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import re
import requests

def scrape():
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
    basin_base = scrape()
    return render_template('%s.html' % index, base=basin_base)

if __name__ == "__main__":
    app.run(debug=True)