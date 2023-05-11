from urllib import request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def get_collection_volume(url):
    hdr = {"User-Agent": "Mozilla/5.0"}

    req = Request(url, headers=hdr)
    page_source = urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(page_source, "html.parser")
    html = str(soup.find('html'))
    volumeIndex = html.find('totalVolume","__typename":"PriceType","unit":"')
    closingApprIndex = html.find('"',volumeIndex+46)
    return html[volumeIndex+46:closingApprIndex]

@app.route('/metaroyals_volume')
def get_metaroyals_volume():
    MRVolume = get_collection_volume('https://opensea.io/collection/metablaze-metaroyals')
    MRRoyalties = float(MRVolume)*float(0.1*0.1)
    return '%f' % MRRoyalties

@app.route('/metagoblins_volume')
def get_metagoblins_volume():
    MGVolume = get_collection_volume('https://opensea.io/collection/metablaze-metagoblins')
    MGRoyalties = float(MGVolume)*float(0.1*0.1)
    return '%f' % MGRoyalties

@app.route('/total_volume')
def get_total_volume():
    MRRoyalties = get_metaroyals_volume()
    MGRoyalties = get_metagoblins_volume()

    return '%f' % (float(MRRoyalties) + float(MGRoyalties))
