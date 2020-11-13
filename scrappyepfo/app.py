try:
    from scrappyepfo.data_scraper import get_comp_list, get_comp_list_mca
except:
    from data_scraper import get_comp_list, get_comp_list_mca
from fuzzywuzzy import process
import  pprint
from fastapi import FastAPI

app = FastAPI()

@app.get("/epfo/{companyName}")
async def readEpfo(companyName):
    '''api call epfo'''
    return perform_epfo(companyName)

@app.get("/mca/{companyName}")
async def readMca(companyName):
    '''api call epfo'''
    return perform_mca(companyName)

@app.get("/")
async def root():
    '''api call root'''
    return {"Status":"OK" }

@app.get("/devInfo/")
async def devInfo():
    '''api call dev'''
    data = {
        "Name" : "Sagar Paul",
        "Email" : "paul.sagar@yahoo.com",
        "Github" : "https://github.com/KB-perByte",
    }
    return data

def perform_epfo(name):
    comp_list = get_comp_list(name)
    pprint.pprint(comp_list[0])
    return comp_list[0]

def perform_mca(name):
    comp_list = get_comp_list_mca(name)
    pprint.pprint(comp_list)
    return comp_list

    




