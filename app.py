from flask import Flask, request, jsonify, render_template
from flask_restful import Api, Resource

from ai import ink
from sb import db, tone

app = Flask(__name__)
api = Api(app)


def makeS (s, t):
    s = s
    b = "Do it yourself"

    if t == "gen":
        b = f"""
            Scope: { db['week'][s['week']]['summary'] } 
            Number of Questions: { s.get('N', 3)}
        """

    elif t == "sumup":

        isweek = s.get("week", False)
        islec = s.get("lecture", False)

        if islec and isweek:
            b = db['week'][isweek]['lecture'][islec]["summary"]
        elif isweek:
            b = db['week'][isweek]["summary"]
        else:
            b = "Do what ever you think is appropraite"
    
    elif t == "chat":
        b = f"{b}"

    else:
        b = "Do what ever you think is appropraite"

    return b



class AI(Resource):

    def post(self):
        s = request.get_json()

        t = s["type"]
        p = s["prompt"]
        b = s["background"]

        c = makeS(b, t) # Make it using the background details

        i = { 
            "prompt" : p,
            "content" : c
        }

        link = {
            "gen" : ink.generate_questions,
            "sumup" : ink.summarize,
            "chat" : ink.chat,
            "analyse" : ink.chat,
            "explain" : ink.chat
        }

        if (link[t]):
            d = link[t](i)
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
