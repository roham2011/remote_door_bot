from flask import Flask 
from config.config import HOST , test

app = Flask(__name__)



if __name__ == "__main__" :
    print (__name__)
    print (Flask)
    test()
    app.run(host=HOST , port = 5027 , debug = True)