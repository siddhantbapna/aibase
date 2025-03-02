from flask import Flask, request, jsonify, render_template
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class AI(Resource):
    def post(self):
        data = request.get_json()
        data["Hey"] = "I am sb"
        return jsonify(data)

api.add_resource(AI, '/ai')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
