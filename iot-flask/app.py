import datetime

import json
import plotly

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

# a list of our mqtt topics
from books import BOOKS

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

from myServer import myServer
ms = myServer()

def getPlot():
    myPlot = [
        dict(
            data=[
                dict(
                    x=[1, 2, 3],
                    y=[10, 20, 30],
                    type='scatter'
                ),
            ],
            layout=dict(
                title='first graph'
            )
        ),
    ]
    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(myPlot)]


    return ids, myPlot

def getResponse():
    templateData = ms.getState()
    ids, myPlot = getPlot()
    graphJSON = json.dumps(myPlot, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', **templateData, ids=ids, graphJSON=graphJSON)

@app.route("/")
def hello():

    templateData = ms.getState()
    # Convert the figures to JSON
    ids, myPlot = getPlot()
    graphJSON = json.dumps(myPlot, cls=plotly.utils.PlotlyJSONEncoder)

    #return render_template('index.html', **templateData, ids=ids, graphJSON=graphJSON)
    resp = getResponse()
    return resp

@app.route("/<deviceName>/<topic>/<action>", methods=['POST'])
def old_action(deviceName, topic, action):
    
    print('app.py user action: deviceName:', deviceName, 'topic:', topic, 'action:', action)

    templateData = ms.setState(deviceName, topic, action)

    return render_template('index.html', **templateData)

@app.route('/toggleButton', methods=['POST'])
def toggleButton():
    tmp = request.form
    print('toggleButton', tmp)
    for k,v in request.form.items():
        # k will be the mqtt channel to toggle
        print(k, v)
        folder = k
        ms.setState2(folder, 'toggle')

    resp = getResponse()
    return resp

if __name__ == '__main__':
    app.run(host="0.0.0.0")

