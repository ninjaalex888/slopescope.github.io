from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import re
import requests
import json

def get_driving_times(xcord, ycord):
    coords = str(xcord)+", "+str(ycord)
    body = json.dumps({"locations": [coords, "28194 U.S. 6, Keystone, CO 80435"]})
    # print body
    # print(body)
    r = requests.post("http://www.mapquestapi.com/directions/v2/routematrix?key=ind9QjhJrKLehF3GGrIoF4UnUtUw14xm", data=body)
    output=json.loads(r.content)
    time = output['time'][1]
    hours = time / 3600
    minutes = (time % 3600) / 60
    seconds = time % 60

    return str(hours) + " Hours and " + str(minutes) + " Minutes"

def get_driving_times_loveland(xcord, ycord):
    coords = str(xcord)+", "+str(ycord)
    body = json.dumps({"locations": [coords, "Exit 216  Interstate 70 Georgetown, CO 80444"]})
    # print body
    print(body)
    r = requests.post("http://www.mapquestapi.com/directions/v2/routematrix?key=ind9QjhJrKLehF3GGrIoF4UnUtUw14xm", data=body)
    output=json.loads(r.content)
    time = output['time'][1]
    hours = time / 3600
    minutes = (time % 3600) / 60
    seconds = time % 60

    return str(hours) + " Hours and " + str(minutes) + " Minutes"


def scrape_loveland():
    l = []
    twenty_four = ''
    seventy_two = ''
    url = 'http://skiloveland.com/snow-report/'
    r=requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    base = soup.find('span', {'class' : 'mid-mtn-total'})
    strongs = soup.find_all('strong')
    for elem in strongs:
        if elem.text == '24 HOUR':
            twenty_four = elem.parent.findPrevious('span').text
            break
    for elem in strongs:
        if elem.text == '72 HOUR':
            seventy_two = elem.parent.findPrevious('span').text
            break
    return base.text, twenty_four, seventy_two



def scrape_abasin():
    l = []
    url = 'https://www.arapahoebasin.com/snow-conditions/'
    base = ''
    twenty_four = ''
    seventy_two = ''
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    for elem in soup(text=re.compile('Base')):
        if len(elem) == 4:
            base = elem.parent.findPrevious('div', {"class":"ab-condition_value"}).text
    for elem in soup(text=re.compile('Past 24 Hrs')):
        twenty_four =  elem.parent.findPrevious('div', {"class":"ab-condition_value"}).text
        break
    for elem in soup(text=re.compile('Past 72 Hrs')):
        seventy_two = elem.parent.findPrevious('div', {"class":"ab-condition_value"}).text
        break
    return base, twenty_four, seventy_two

app = Flask(__name__)

@app.route('/<string:index>/', methods=['GET','POST'])
def my_form_post(index):
    if request.method =='POST':
        dict_data = json.loads(request.data)
        if dict_data['resort'] == 'basin':
            return get_driving_times(float(dict_data['xcord']), float(dict_data['ycord']))
        elif dict_data['resort'] == 'loveland':
            return get_driving_times_loveland(float(dict_data['xcord']), float(dict_data['ycord']))
    basin_base, basin_twenty_four, basin_seventy_two = scrape_abasin()
    loveland_base, loveland_twenty_four, loveland_seventy_two = scrape_loveland()
    return render_template('%s.html' % index, aBayBase=basin_base, lovelandBase = loveland_base,
                           lovelandTwentyFour = loveland_twenty_four,lovelandSeventyTwo = loveland_seventy_two,
                           aBasinTwentyFour = basin_twenty_four, aBasinSeventyTwo = basin_seventy_two)

if __name__ == "__main__":
    app.run()
    # app.run(debug=True)
