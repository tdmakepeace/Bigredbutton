import json
import requests
from configparser import ConfigParser
import loginvar

def getvar(name):
    ' Global variable retrival from psm.cfg'
    c = ConfigParser()
    c.read('psm.cfg')
    return c.get('global', name)


def login():
    url = 'https://%s/v1/login' % (loginvar.ipman)
    jsonbody = json.dumps({"username": loginvar.adminuser, "password": loginvar.adminpwd, "tenant": "default"}).encode('utf8')
    headers = {'Content-Type': 'application/json'}
    #			print(jsonbody)
    #			print(body)
    #			print(headers)

    try:
        req = requests.post(url, headers=headers, data=jsonbody, verify=False)
    except requests.ConnectionError:
        print(req.status_code)

    if req.status_code == 200:
        #			print(req.headers)
        #			print(req.text)

        info = (req.headers)
        #		info = (((req.json()).get('list-meta')).get('total-count'))
        #		result = req.read()
        #		info = req.info()
        #			print(info)

        cookiePSM = info['set-cookie']
        #			print(cookiePSM)
        x = cookiePSM.index(";")
        cookiekey = cookiePSM[:x]
        #			print(x)
        #			print(cookiekey)
        y = cookiePSM.index("Expires=")

        #			print(y)
        expires = (cookiePSM[y + 8:])
        z = expires.index(";")
        cookieexpiry = expires[:z]
        #			print(cookieexpiry)

        file = open("psm.cfg", "w")
        file.write(
            f"[global]\nipman = \'{loginvar.ipman}\'\nadminuser = \'{loginvar.adminuser}\'\nadminpwd = \'{loginvar.adminpwd}\'\ncookiekey = \'{cookiekey}\'\nexpiry = \'{cookieexpiry}\'\n")
        file.close()
        return cookiekey