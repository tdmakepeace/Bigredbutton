from bigredbase import *
from policy import *
from editrules import *
from linkingpolicy import *
import time


if __name__ == '__main__':
    login()

    # define your admin network for remote access into hosts
    # define your isolate policy
    IsolatePolicy = 'Isolated_Hosts'
    AdminNet = '192.168.102.0/24'
    VRFToDemo ="default"
    demotime = 10

    # only uncomment in initial deployement phase.
    # recomend you use the VRF concept to demo, but you can use network example
    if RetrievePolicy(IsolatePolicy) != 1:
        CreatePolicy(IsolatePolicy, AdminNet)
    else:
        UpdatePolicy(IsolatePolicy, AdminNet)
    LinkPolicyVRF(VRFToDemo, IsolatePolicy)


    # #demo to show a couple of hosts being blocked, and then unblocked
    AddToBlockPolicy(IsolatePolicy, '192.168.101.150')
    time.sleep(demotime)
    AddToBlockPolicy(IsolatePolicy, '192.168.101.151')
    time.sleep(demotime)
    DeleteFromBlockPolicy(IsolatePolicy, '192.168.101.151')
    time.sleep(demotime)
    DeleteFromBlockPolicy(IsolatePolicy, '192.168.101.150')


    # only uncomment to clean up the lab.
    time.sleep(demotime)
    UnLinkPolicyVRF(VRFToDemo)
    DeletePolicy(IsolatePolicy)


    # Link Policy to network example.
    # LinkPolicyNetwork('2', IsolatePolicy, 'VLAN101', VRFToDemo)
    # to delete policy on the network
    # LinkPolicyNetwork('2', '', '101', VRFToDemo)


