import requests
from bs4 import BeautifulSoup as soup
from scrappyepfo.statics.captcha_reader import decode
import json

EPFO_base_url = "https://unifiedportal-epfo.epfindia.gov.in"
EPFO_URL = "https://unifiedportal-epfo.epfindia.gov.in/publicPortal/no-auth/misReport/home/loadEstSearchHome/"
MCA_URL = "http://www.mca.gov.in/mcafoportal/showCheckCompanyName.do"

def get_soup(session, url):
    response = session.get(url)
    my_soup = soup(response.text, "html.parser")
    return my_soup

def get_comp_list(company_name):
    sesh = requests.Session()
    my_soup = get_soup(sesh, EPFO_URL)
    company_list = []
    r = post_search_establishment_request(my_soup, sesh, company_name)
    company_list = get_company_list(r)
    return company_list, r, sesh

def post_search_establishment_request(my_soup, session, est_name, est_code=""):
    est_req = my_soup.find("div", {"class": "col-sm-3 col-md-2 col-lg-2"}).input['onclick'].split("'")[1]
    my_url = get_full_url(est_req)
    response = None
    i = 0
    while response is None:
        try:
            captcha = generate_and_read_captcha(my_soup, session)
        
            if len(captcha) > 4:
                print(captcha)
                response = session.post(my_url, data=json.dumps({"EstName": est_name, "EstCode": est_code, "captcha": captcha}),
                                        headers={'Content-Type': 'application/json'})
                if 'Please enter valid captcha' in str(response.content):
                    i+=1
                    print("Try: - ", i)
                    response = None
        except Exception as e:
            response = None
            print("Exception:" + str(e))
    return response

def generate_and_read_captcha(my_soup, session):
    img_src = my_soup.find("div", {"id": "captchaImg"}).find("img")['src']
    my_url = get_full_url(img_src)
    response = session.get(my_url, stream=True)
    filename = "scrappyepfo/statics/web_captcha.png"
    with open(filename,
              "wb") as f: 
        f.write(response.content)
    del response  
    return decode(filename)

def get_full_url(sub_url):
    return EPFO_base_url + sub_url

def get_company_list(establishment_response):
    my_soup = soup(establishment_response.text, "html.parser")
    name_list = []
    dataDict = { "EstablishmentID": None,
                "EstablishmentName": None,
                "EstablishmentAddress": None }

    idx = 0
    for org in my_soup.find_all("td"):
        if idx == 5 or idx == 0:
            idx = 0
            dataDict = { "EstablishmentID": None,
                        "EstablishmentName": None,
                        "EstablishmentAddress": None }
            
        if idx == 0:
            dataDict["EstablishmentID"] = org.string
        elif idx == 1:
            dataDict["EstablishmentName"] = org.string
        elif idx == 2:
            dataDict["EstablishmentAddress"] = org.string
        elif idx == 3:
            pass
        elif idx == 4:
            name_list.append(dataDict)
        idx+=1
        
    return name_list

def get_comp_list_mca(name):
    payload = {'name1':name,'checkCompanyName_0':'Search','displayCaptcha':False}
    return [{"Error" : "Not Implimented"}]
    #counter=1&name1=flipkart&name2=&name3=&name4=&name5=&name6=&activityType1=&activityType2=&displayCaptcha=false
    with requests.session() as s:
        s.headers={"User-Agent":"Mozilla/5.0"}
        s.post(MCA_URL ,data=payload)
        res=s.get(MCA_URL ,data=payload)
        my_soup = soup(res.text, "html.parser")
        _soup=soup(res.text,"lxml")
        print(_soup.prettify())
        return [True]

# get_comp_list_mca("Flipkart")