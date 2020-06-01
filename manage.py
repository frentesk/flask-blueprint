from flask_script import Server, Manager

from app import create_app

#from app.models.Users import User

app=create_app('default')
manager=Manager(app=app)
#StartDeleteFile()
#def make_shell_context():
#    return dict(app=app,db=db,User=User)

manager.add_command('runserver',Server(host=app.config['HOST'],port=app.config['PORT'],use_debugger=True,use_reloader=True,threaded=True))

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'x-requested-with,content-type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__=="__main__":
    manager.run(default_command='runserver')
