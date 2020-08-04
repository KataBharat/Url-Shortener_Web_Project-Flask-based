from flask import Flask

def create_app(test_config=None):
    
    app = Flask(__name__) #used to create the flask app 
    app.secret_key = 'jhjgrdytjbbjkhbcrsrdiiplknbc'  # random string which is a secret key for securing messages between website and user

    from . import urlshort 
    app.register_blueprint(urlshort.bp)

    return app