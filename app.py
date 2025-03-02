from flask import Flask, request, jsonify, render_template
from flask_restful import Api, Resource

from ai import ink
from sb import db, tone

app = Flask(__name__)
api = Api(app)


def makeS (s):
    s = s
    b = "Do it yourself"
    return b

class AI(Resource):

    def post(self):
        s = request.get_json()

        t = s["type"]
        p = s["prompt"]
        b = s["background"]

        c = makeS(b) # Make it using the background details


        if s["type"] == "sumup":

            d = ink.summarize({
                "query" : s["prompt"],
                "content" : c
            })

        elif s["type"] == "gen":
            d = ink.generate_questions({
                "topic" : "s Types 1",
                "scope" : s["prompt"],
                "N" : 3
            })

        elif s["type"] == "chat":
            d = ink.chat({
                "topic" : "s Types 1",
                "query" : s["prompt"],
                "content" : "On Quantum Computer"
            })

        elif s["type"] == "explain":
            d = ink.chat({
                "topic" : "s Types 1",
                "query" : s["prompt"],
                "content" : "On Quantum Computer"
            })
        
        elif t == "analyse":
            d = ink.chat({
                "topic" : "s Types 1",
                "query" : s["prompt"],
                "content" : "On Quantum Computer"
            })

        else :
            d = "Invaild"

        b = jsonify(d)
        return b

        


















api.add_resource(AI, '/ai')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
