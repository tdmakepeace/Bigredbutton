from bigredbase import getvar
import loginvar
import requests
import json
import socket
import struct
import os


def AddToBlockPolicy(PolicyName,updateIP):
    cookiekey = getvar('cookiekey')[1:-1]
    headers = ({'Content-Type': 'application/json', 'cookie': cookiekey})
    url = ('https://%s/configs/security/v1/tenant/default/networksecuritypolicies/%s' % (loginvar.ipman, PolicyName))
    # print(f'{url} {body}')
    try:
        req = requests.get(url, headers=headers, verify=False)
        # print(req.headers)
        # print(req.text)
        currentrules = req.json()
        # print(a["spec"])
        # b=(a["spec"])
        # c=(b["rules"])
        # print(c)
        # # d= c.json()
        # print("tes", c)

        # prefilename = 'prejson.json'
        # with open(prefilename, "w") as file:
        #  json.dump(currentrules, file)

        rulesheader='''{ 
            "kind": "NetworkSecurityPolicy",
            "api-version": "v1",
            "meta": {
                "name": "%s",
                "tenant": "default",
                "namespace": "default"
            },
          "spec": {
            "attach-tenant": true,
            "rules": '''
        rulessuffix='''            } }'''

        postfilename = 'postjson.json'
        f = open(postfilename, "w")
        f.write(rulesheader)
        f.close()


        ipint = str(struct.unpack('>I',  socket.inet_aton(updateIP))[0])
        blocknameout=(ipint+"_Block_Outbound")
        blocknamein=(ipint+"_Block_Inbound")

        lst = []
        with open(postfilename, mode='a') as f:
            for each in currentrules["spec"]["rules"]:
                # print(each["name"])
                if (each["name"]) !=  "Default_Allow_Net":
                    lst.append(each)
                # print(each)

            lst.append({'proto-ports': [{'protocol': 'any', 'ports': ''}], 'action': 'deny', 'from-ip-addresses': [updateIP], 'to-ip-addresses': ['any'], 'description': 'Block_Outbound_Traffic', 'name': blocknameout } )
            lst.append({'proto-ports': [{'protocol': 'any', 'ports': ''}], 'action': 'deny', 'from-ip-addresses': ['any'], 'to-ip-addresses': [updateIP], 'description': 'Block_Inbound_Traffic', 'name': blocknamein } )
            # Adds the detault rule back on the end.
            lst.append({'proto-ports': [{'protocol': 'any', 'ports': ''}], 'action': 'permit', 'from-ip-addresses': ['any'], 'to-ip-addresses': ['any'], 'description': 'Default_Allow_On_VRF', 'name': 'Default_Allow_Net'})
            json.dump(lst, f)

        f = open(postfilename, "a")
        f.write(rulessuffix)
        f.close()

        if req.status_code == 200:
            # print(f'')
            # print(f'')
            # print(f'success requestPolicy', (PolicyName))
            # # print(req.headers)
            # print(req.text)

            url = ('https://%s/configs/security/v1/tenant/default/networksecuritypolicies/%s' % (
            loginvar.ipman, PolicyName))
            # print(f'{url} {body}')

            with open(postfilename, "r") as file:
                contents = file.read()
                # print(contents)

            try:
                req = requests.put(url, headers=headers, data=contents, verify=False)
                # print(req.headers)
                # print(req.text)
                if req.status_code == 200:
                    print(f'success UpdatePolicy', (PolicyName))
                    # print(req.headers)
                    # print(req.text)

                elif req.status_code == 404:
                    print(f'404')
                elif req.status_code == 412:
                    print(f'412 - UpdatePolicy - failed - probably does not exist', (PolicyName))
                else:
                    print(req.status_code, (PolicyName), f'UpdatePolicy')
                    # print(req.headers)
            except requests.ConnectionError:
                print(f'Error')


        elif req.status_code == 404:
            print(f'404')
        elif req.status_code == 412:
            print(f'412 - DeletePolicy - failed - probably does not exist', (PolicyName))
        else:
            print(req.status_code, (PolicyName), f'UpdatePolicy')
            # print(req.headers)
    except requests.ConnectionError:
        print(f'Error')



def DeleteFromBlockPolicy(PolicyName,updateIP):
    cookiekey = getvar('cookiekey')[1:-1]
    headers = ({'Content-Type': 'application/json', 'cookie': cookiekey})
    url = ('https://%s/configs/security/v1/tenant/default/networksecuritypolicies/%s' % (loginvar.ipman, PolicyName))
    # print(f'{url} {body}')
    try:
        req = requests.get(url, headers=headers, verify=False)
        # print(req.headers)
        # print(req.text)
        currentrules = req.json()
        # print(a["spec"])
        # b=(a["spec"])
        # c=(b["rules"])
        # print(c)
        # # d= c.json()
        # print("tes", c)

        # prefilename = 'prejson.json'
        # with open(prefilename, "w") as file:
        #  json.dump(a, file)

        rulesheader='''{ 
            "kind": "NetworkSecurityPolicy",
            "api-version": "v1",
            "meta": {
                "name": "%s",
                "tenant": "default",
                "namespace": "default"
            },
          "spec": {
            "attach-tenant": true,
            "rules": '''
        rulessuffix='''            } }'''
        postfilename = 'postjson.json'
        f = open(postfilename, "w")
        f.write(rulesheader)
        f.close()

        # for each in a["spec"]["rules"]:
        #     print(each["name"])
        #     print(each)
        #     x=str(each)
        #     f.write(x)
        #     f.write(''',''')
        # f.write(y)
        ipint = str(struct.unpack('>I',  socket.inet_aton(updateIP))[0])
        blocknameout=(ipint+"_Block_Outbound")
        blocknamein=(ipint+"_Block_Inbound")
        deletelist = [blocknamein, blocknameout, "Default_Allow_Net"]

        lst = []
        with open(postfilename, mode='a') as f:
            for each in currentrules["spec"]["rules"]:
                # print(each["name"])

                if (each["name"]) in deletelist:
                    print("row removed")
                else:
                    lst.append(each)
                    # print(each)

            lst.append({'proto-ports': [{'protocol': 'any', 'ports': ''}], 'action': 'permit', 'from-ip-addresses': ['any'], 'to-ip-addresses': ['any'], 'description': 'Default_Allow_On_VRF', 'name': 'Default_Allow_Net'})
            json.dump(lst, f)

        f = open(postfilename, "a")
        f.write(rulessuffix)
        f.close()

        if req.status_code == 200:
            # print(f'')
            # print(f'')
            print(f'success requestPolicy', (PolicyName))
            # print(req.headers)
            # print(req.text)

            url = ('https://%s/configs/security/v1/tenant/default/networksecuritypolicies/%s' % (
            loginvar.ipman, PolicyName))
            # print(f'{url} {body}')

            with open(postfilename, "r") as file:
                contents = file.read()
                # print(contents)

            try:
                req = requests.put(url, headers=headers, data=contents, verify=False)
                # print(req.headers)
                # print(req.text)
                if req.status_code == 200:
                    print(f'success UpdatePolicy', (PolicyName))
                    # print(req.headers)
                    # print(req.text)

                elif req.status_code == 404:
                    print(f'404')
                elif req.status_code == 412:
                    print(f'412 - UpdatePolicy - failed - probably does not exist', (PolicyName))
                else:
                    print(req.status_code, (PolicyName), f'UpdatePolicy')
                    # print(req.headers)
            except requests.ConnectionError:
                print(f'Error')


        elif req.status_code == 404:
            print(f'404')
        elif req.status_code == 412:
            print(f'412 - DeletePolicy - failed - probably does not exist', (PolicyName))
        else:
            print(req.status_code, (PolicyName), f'UpdatePolicy')
            # print(req.headers)
    except requests.ConnectionError:
        print(f'Error')

