from flask import Flask
from flask import make_response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return make_response('<h1>丁樊🐂🍺</h1>', 200)

api.add_resource(HelloWorld, "/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8000")