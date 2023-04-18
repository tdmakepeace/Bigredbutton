from bigredbase import getvar
import loginvar
import requests

def LinkPolicyVRF(vrf, policy):
    cookiekey = getvar('cookiekey')[1:-1]
    # print(f'{prot}')
    headers = ({'Content-Type': 'application/json', 'cookie': cookiekey})
    body = (""" {
  "kind": "VirtualRouter",
  "api-version": "v1",
  "meta": {
    "tenant": "default",
    "namespace": "default",
    "name": "%s"
  },
  "spec": {
    "router-mac-address": null,
    "default-ipam-policy": null,
    "ingress-security-policy":  [
      "%s"
    ],
    "egress-security-policy":  [
      "%s"
    ],
    "maximum-cps-per-network-per-distributed-services-entity": 0,
    "maximum-sessions-per-network-per-distributed-services-entity": 0,
    "flow-export-policy": [],
    "selectCPS": 0,
    "selectSessions": 0,
    "type": "tenant"
  }
}""" % (vrf, policy, policy))

    url = ('https://%s/configs/network/v1/tenant/default/virtualrouters/%s' % (loginvar.ipman, vrf))
    # print (f'{url} {body}')
    try:
        req = requests.put(url, headers=headers, data=body, verify=False)
        # print(req.headers)
        # print(req.text)
        if req.status_code == 200:
            print(f'success LinkPolicy', (policy, vrf))
            # print(req.headers)
            # print(req.text)

        elif req.status_code == 404:
            print(f'404')
        elif req.status_code == 412:
            print(f'412 - LinkPolicy - failed - probably does not exist', (policy, vrf))
        else:
            print(req.status_code, f'LinkPolicy', (policy, vrf))
            # print(req.headers)
    except requests.ConnectionError:
        print(f'Error')


def UnLinkPolicyVRF(vrf):
    cookiekey = getvar('cookiekey')[1:-1]
    # print(f'{prot}')
    headers = ({'Content-Type': 'application/json', 'cookie': cookiekey})
    body = (""" {
  "kind": "VirtualRouter",
  "api-version": "v1",
  "meta": {
    "tenant": "default",
    "namespace": "default",
    "name": "%s"
  },
  "spec": {
    "router-mac-address": null,
    "default-ipam-policy": null,
    "ingress-security-policy":  null,
    "egress-security-policy":  null,
    "maximum-cps-per-network-per-distributed-services-entity": 0,
    "maximum-sessions-per-network-per-distributed-services-entity": 0,
    "flow-export-policy": [],
    "selectCPS": 0,
    "selectSessions": 0,
    "type": "tenant"
  }
}""" % (vrf))

    url = ('https://%s/configs/network/v1/tenant/default/virtualrouters/%s' % (loginvar.ipman, vrf))
    # print (f'{url} {body}')
    try:
        req = requests.put(url, headers=headers, data=body, verify=False)
        # print(req.headers)
        # print(req.text)
        if req.status_code == 200:
            print(f'success UnLinkPolicy', (vrf))
            # print(req.headers)
            # print(req.text)

        elif req.status_code == 404:
            print(f'404')
        elif req.status_code == 412:
            print(f'412 - UnLinkPolicy - failed - probably does not exist', (vrf))
        else:
            print(req.status_code, f'UnLinkPolicy', (vrf))
            # print(req.headers)
    except requests.ConnectionError:
        print(f'Error')


def LinkPolicyNetwork(vlan, policy, network, vrf):
    cookiekey = getvar('cookiekey')[1:-1]
    # print(f'{prot}')
    headers = ({'Content-Type': 'application/json', 'cookie': cookiekey})
    body = (""" {
  "kind": "Network",
  "api-version": "v1",
  "meta": {
    "tenant": "default",
    "namespace": "default",
    "name": "%s"
  },
  "spec": {
    "ipv4-subnet": null,
    "ipv4-gateway": null,
    "ipv6-subnet": null,
    "ipv6-gateway": null,
    "ipam-policy": null,
    "orchestrators": [],
    "ingress-security-policy":  [
      "%s"
    ],
    "egress-security-policy": [
      "%s"
    ],
    "selectVlanOrIpv4": 1,
    "vxlan-vni": null,
    "virtual-router": "%s",
    "type": "bridged",
    "vlan-id": %s,
    "route-import-export": null
  }
}""" % (network, policy, policy, vrf, vlan))

    url = ('https://%s/configs/network/v1/tenant/default/networks/%s' % (loginvar.ipman, network))
    # print (f'{url} {body}')
    try:
        req = requests.put(url, headers=headers, data=body, verify=False)
        # print(req.headers)
        # print(req.text)
        if req.status_code == 200:
            print(f'success LinkPolicy', (network))
            # print(req.headers)
            # print(req.text)

        elif req.status_code == 404:
            print(f'404')
        elif req.status_code == 412:
            print(f'412 - LinkPolicy - failed - probably does not exist', (network))
        else:
            print(req.status_code, f'LinkPolicy', (network))
            # print(req.headers)
    except requests.ConnectionError:
        print(f'Error')

