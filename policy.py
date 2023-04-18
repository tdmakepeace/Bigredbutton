from bigredbase import getvar
import loginvar
import requests
#import socket
#import struct

def CreatePolicy(PolicyName, infectedhost):
    cookiekey = getvar('cookiekey')[1:-1]
    headers = ({'Content-Type': 'application/json', 'cookie': cookiekey})
    # print(PolicyName,infectedhost)
    body = """{ 
        "kind": "NetworkSecurityPolicy",
        "api-version": "v1",
        "meta": {
            "name": "%s"
        },
      "spec": {
        "attach-tenant": true,
        "rules": [
          {
            "proto-ports": [
              {
                "protocol": "ICMP",
                "ports": ""
              }
            ],
            "action": "permit",
            "from-ip-addresses": [
              "%s"
            ],
            "to-ip-addresses": [
              "any"
            ],
            "name": "Admin_Access_ICMP"
          },
          {
            "proto-ports": [
              {
                "protocol": "TCP",
                "ports": "3389"
              }
            ],
            "action": "permit",
            "from-ip-addresses": [
              "%s"
            ],
            "to-ip-addresses": [
              "any"
            ],
            "name": "Admin_Access_RDP"
          },
          {
            "proto-ports": [
              {
                "protocol": "TCP",
                "ports": "22"
              }
            ],
            "action": "permit",
            "from-ip-addresses": [
              "%s"
            ],
            "to-ip-addresses": [
              "any"
            ],
            "name": "Admin_Access_SSH"
          },
          {
            "proto-ports": [
              {
                "protocol": "any",
                "ports": ""
              }
            ],
            "action": "permit",
            "from-ip-addresses": [
              "any"
            ],
            "to-ip-addresses": [
              "any"
            ],
            "description": "Default_Allow_Net",
            "name": "Default_Allow_Net"
          }
        ]
      }
} """ % (PolicyName, infectedhost, infectedhost, infectedhost)

    url = ('https://%s/configs/security/v1/tenant/default/networksecuritypolicies' % (loginvar.ipman))
    # print(f'{url} {body}')
    try:
        req = requests.post(url, headers=headers, data=body, verify=False)
        # print(req.headers)
        # print(req.text)
        if req.status_code == 200:
            print(f'success CreatePolicy', (PolicyName))
            # print(req.headers)
            # print(req.text)

        elif req.status_code == 404:
            print(f'404')
        elif req.status_code == 412:
            print(f'412 - CreatePolicy - failed - probably already exist', (PolicyName))
        else:
            print(req.status_code, (PolicyName), f'CreatePolicy')
            # print(req.headers)
    except requests.ConnectionError:
        print(f'Error')


def UpdatePolicy(PolicyName, infectedhost):
    cookiekey = getvar('cookiekey')[1:-1]
    headers = ({'Content-Type': 'application/json', 'cookie': cookiekey})
    # print(PolicyName, infectedhost)
    body = """{ 
            "kind": "NetworkSecurityPolicy",
            "api-version": "v1",
            "meta": {
                "name": "%s"
            },
          "spec": {
            "attach-tenant": true,
            "rules": [
              {
                "proto-ports": [
                  {
                    "protocol": "ICMP",
                    "ports": ""
                  }
                ],
                "action": "permit",
                "from-ip-addresses": [
                  "%s"
                ],
                "to-ip-addresses": [
                  "any"
                ],
                "name": "Admin_Access_ICMP"
              },
              {
                "proto-ports": [
                  {
                    "protocol": "TCP",
                    "ports": "3389"
                  }
                ],
                "action": "permit",
                "from-ip-addresses": [
                  "%s"
                ],
                "to-ip-addresses": [
                  "any"
                ],
                "name": "Admin_Access_RDP"
              },
              {
                "proto-ports": [
                  {
                    "protocol": "TCP",
                    "ports": "22"
                  }
                ],
                "action": "permit",
                "from-ip-addresses": [
                  "%s"
                ],
                "to-ip-addresses": [
                  "any"
                ],
                "name": "Admin_Access_SSH"
              },
              {
                "proto-ports": [
                  {
                    "protocol": "any",
                    "ports": ""
                  }
                ],
                "action": "permit",
                "from-ip-addresses": [
                  "any"
                ],
                "to-ip-addresses": [
                  "any"
                ],
                "description": "Default_Allow_Net",
                "name": "Default_Allow_Net"
              }
            ]
          }
} """ % (PolicyName, infectedhost, infectedhost, infectedhost)

    url = ('https://%s/configs/security/v1/tenant/default/networksecuritypolicies/%s' % (loginvar.ipman, PolicyName))
    # print(f'{url} {body}')
    try:
        req = requests.put(url, headers=headers, data=body, verify=False)
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


def DeletePolicy(PolicyName):
    cookiekey = getvar('cookiekey')[1:-1]
    headers = ({'Content-Type': 'application/json', 'cookie': cookiekey})
    url = ('https://%s/configs/security/v1/tenant/default/networksecuritypolicies/%s' % (loginvar.ipman, PolicyName))
    # print(f'{url} {body}')
    try:
        req = requests.delete(url, headers=headers, verify=False)
        # print(req.headers)
        # print(req.text)
        if req.status_code == 200:
            print(f'success DeletePolicy', (PolicyName))
            # print(req.headers)
            # print(req.text)

        elif req.status_code == 404:
            print(f'404')
        elif req.status_code == 412:
            print(f'412 - DeletePolicy - failed - probably does not exist', (PolicyName))
        else:
            print(req.status_code, (PolicyName), f'UpdatePolicy')
            # print(req.headers)
    except requests.ConnectionError:
        print(f'Error')


def RetrievePolicy(PolicyName):
    cookiekey = getvar('cookiekey')[1:-1]
    headers = ({'Content-Type': 'application/json', 'cookie': cookiekey})
    url = ('https://%s/configs/security/v1/tenant/default/networksecuritypolicies/%s' % (loginvar.ipman, PolicyName))
    # print(f'{url} {body}')
    try:
        req = requests.get(url, headers=headers, verify=False)
        # print(req.headers)
        print(req.text)
        if req.status_code == 200:
            print(f'success requestPolicy', (PolicyName))
            # print(req.headers)
            # print(req.text)
            return 1

        elif req.status_code == 404:
            print(f'404')
        elif req.status_code == 412:
            print(f'412 - DeletePolicy - failed - probably does not exist', (PolicyName))
        else:
            print(req.status_code, (PolicyName), f'UpdatePolicy')
            # print(req.headers)
    except requests.ConnectionError:
        print(f'Error')


