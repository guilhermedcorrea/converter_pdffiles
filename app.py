from flask import Flask, request


app = Flask(__name__)

from routes import*


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
