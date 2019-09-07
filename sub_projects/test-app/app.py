from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return "<h1>丁樊牛逼！</h1>"

api.add_resource(HelloWorld, "/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8000")