# BigRedButton 
This is to demo the API, and a full lockdown of a host, using either a Network or VRF policy. <br>
<br> 
Recommend that you use a VRF policy and do not touch the existing network policy. <br>
<br>

## PSM login details
In the loginvar.py file are the PSM login details, update with your PSM server.<br>

```
adminuser = 'admin'<br>
adminpwd = 'Pensando0$'<br>
ipman = '192.168.102.112'<br>
```

<br>
<br>

## Master config file 
The only file to edit is the bigredmaster.py <br>
<br>
This is where you set the action you want the script to follow. <br>

Read the python file to understand and edit.


#### Run as a one off script.

To setup:<br>
`sudo apt install python3-pip
pip3 install -r requirements.txt
python3 -m venv venv
. venv/bin/activate
`
<br>

To run:<br>
`python3 bigredmaster.py
`

<br><br>
The example, creates of updates a default isolate policy <br>
then updates every x seconds to adds a host to be blocked, and then released it <br>
<br><br>


## To run as a simple API service 

Run the base bigredmaster, remove the delete and unlink options.

`python3 bigredrest.py` <br><br>


Add host to the Isolated_Hosts Policy <br>
`curl "http://127.0.0.1:9999/api/bigred/?Policy=Isolated_Hosts&Ip=192.168.101.150" \
  -X POST \
  -H "Content-Type: application/json" 
` <br>
Delete host to the Isolated_Hosts Policy <br>
`curl "http://127.0.0.1:9999/api/bigred/?Policy=Isolated_Hosts&Ip=192.168.101.150" \
  -X DELETE \
  -H "Content-Type: application/json" 
  `
 
### There is a simple UI for walking a customer throught the process in a Demo on port 9999.
  

There is no security on this API as it is only for Demo purposes, and relys on being set up with PSM access. and only has the ablity to add and remover rules.
