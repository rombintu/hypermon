from . import app
from . import admin_api

from flask import request

@app.route("/")
def index():
    admin_api.clean()
    return {
        "GET": "http://<THIS_URL>:<PORT>/<OS_PROJECT_NAME>?username=<OS_USERNAME>&password=<OS_PASSWORD>"
        }

@app.route("/<project>")
def nova_by_project(project):
    admin_api.clean()
    username = request.args.get('username')
    password = request.args.get('password')
    if not project or not username or not password:
        return {"error": "Необходимо указать OS_PROJECT_NAME, OS_USERNAME, OS_PASSWORD. try / for help"}
    
    if not admin_api.auth(username, password, project):
        return {"error": "403 not auth"}
    
    try:
        mess = admin_api.connect(os_project_name=project)
        if mess:
            return {"error": mess} 
    except Exception as err:
        return {"error": err}    
    
    admin_api.load()
    admin_api.filter_hyper()
    return [hpv.__dict__ for hpv in admin_api.hypervisors]
       