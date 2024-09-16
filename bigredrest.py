from bigredbase import *
from policy import *
from editrules import *
from linkingpolicy import *
from flask import Flask, render_template, request, send_from_directory
from flask_restful import Resource, Api
from wtforms import Form, StringField, validators
from urllib.parse import unquote


webhost='0.0.0.0'
webport=9999
IsolatePolicy = 'Isolated_Hosts'
AdminNet = '192.168.102.0/24'
VRFToDemo = "default"
demotime = 10

app = Flask(__name__, static_url_path='/static')
api = Api(app)



@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route("/", methods=['GET', 'POST'])
def index():
    login()
    form = HostIP(request.form)
    Host = form.Host.data
    if request.method == 'POST' :
        if "Setup" in request.form:
            login()
            if RetrievePolicy(IsolatePolicy) != 1:
                CreatePolicy(IsolatePolicy, AdminNet)
                return render_template('home.html',  form=form)
                pass
            else:
                UpdatePolicy(IsolatePolicy, AdminNet)
                return render_template('home.html',  form=form)
                pass
        elif "Link" in request.form:
            if RetrievePolicy(IsolatePolicy) != 1:
                CreatePolicy(IsolatePolicy, AdminNet)
                LinkPolicyVRF(VRFToDemo, IsolatePolicy)
                return render_template('home.html', form=form)
                pass
            else:
                LinkPolicyVRF(VRFToDemo, IsolatePolicy)
                return render_template('home.html', form=form)
                pass

        elif "Block" in request.form and form.validate():
            if RetrievePolicy(IsolatePolicy) != 1:
                CreatePolicy(IsolatePolicy, AdminNet)
                LinkPolicyVRF(VRFToDemo, IsolatePolicy)
                AddToBlockPolicy(IsolatePolicy, Host)
                return render_template('home.html', form=form)
                pass
            else:
                AddToBlockPolicy(IsolatePolicy, Host)
                return render_template('home.html', form=form)
                pass


        elif "UnBlock" in request.form and form.validate():
            if RetrievePolicy(IsolatePolicy) != 1:
                return render_template('home.html', form=form)
                pass
            else:
                DeleteFromBlockPolicy(IsolatePolicy, Host)
                return render_template('home.html', form=form)
                pass


        elif "UnLink" in request.form:
            if RetrievePolicy(IsolatePolicy) != 1:
                return render_template('home.html', form=form)
                pass
            else:
                UnLinkPolicyVRF(VRFToDemo)
                return render_template('home.html', form=form)
                pass

        elif "Delete" in request.form:
            if RetrievePolicy(IsolatePolicy) != 1:
                return render_template('home.html', form=form)
                pass
            else:
                UnLinkPolicyVRF(VRFToDemo)
                DeletePolicy(IsolatePolicy)
                return render_template('home.html', form=form)
                pass
        else:
            return render_template('home.html', form=form)
            pass # unknown
    elif request.method == 'GET':
        return render_template('home.html',  form=form)

    else:
        return render_template('home.html', form=form)


# todo: API section testing.
"""
Example code to use restful structure for greenlake example.

Add "Flask_restful"  to requirements. 
add "from flask_restful import Resource, Api" To import

curl "http://127.0.0.1:9999/api/bigred/?Policy=Isolated_Hosts&Ip=192.168.101.150" \
  -X POST \
  -H "Content-Type: application/json" 

curl "http://127.0.0.1:9999/api/bigred/?Policy=Isolated_Hosts&Ip=192.168.101.150" \
  -X DELETE \
  -H "Content-Type: application/json" 
"""

# This is for the Palo FW that encodes the string
class bigredapicode(Resource):
    def post(self,test):
        login()
        #print(test)
        #print('-----')
        Policy = (test[(test.index("Policy="))+7:(test.index("&"))])
        Ip = (test[(test.index("Ip="))+3:])
        #Policy = test.get('Policy', None)
        #print(Policy)
        #Policy = request.args.get('Policy', None)
        #print(Policy)
        #Ip = request.args.get('Ip', None)
        #print(Ip)
        response = AddToBlockPolicy(Policy, Ip)
        return response

    def delete(self):
        login()
        Policy = request.args.get('Policy', None)
        Ip = request.args.get('Ip', None)
        response = DeleteFromBlockPolicy(Policy, Ip)
        return response 

# This is for the other devices that do not encode the uri
class bigredapi(Resource):
    def post(self):
        login()
        Policy = request.args.get('Policy', None)
        #print(Policy)
        Ip = request.args.get('Ip', None)
        response = AddToBlockPolicy(Policy, Ip)
        return response

    def delete(self):
        login()
        Policy = request.args.get('Policy', None)
        Ip = request.args.get('Ip', None)
        response = DeleteFromBlockPolicy(Policy, Ip)
        return response
        


api.add_resource(bigredapi, '/api/bigred/')
api.add_resource(bigredapicode, '/api/bigred/<test>')

class HostIP(Form):
    Host = StringField('Host IP', [validators.IPAddress(ipv4=True, message="Enter a valid IP Address")])


if __name__ == '__main__':
    app.run(debug=True, host=webhost, port=webport)
