#!/usr/bin/python3
"""Flask back end that shows group members and display a
donation button
Routes:
    /: display “Hello HBNB!”
    /index: display donation button

"""
from flask import Flask, request, jsonify, render_template, send_file
from flask_pymongo import PyMongo
from bson import ObjectId


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/pythonreact'
mongo = PyMongo(app)
db = mongo.db.pythonreact


@app.route('/index', strict_slashes=False)
def index():
    """Display index page
    """
    return render_template('index.html')


@app.route('/index', methods=['POST'], strict_slashes=False)
def donate():
    """Donate button
    """
    id = db.insert({
        'name': request.json['name'],
        'amount': request.json['amount']
    })
    return jsonify(str(ObjectId(id)))


@app.route('/index/<id>', methods=['GET'], strict_slashes=False)
def getDonates(id):
    """Method to show contributors
    """
    contributor = db.find_one({'_id': ObjectId(id)})
    print(contributor)
    return jsonify({
        '_id': str(ObjectId(contributor['_id'])),
        'name': contributor['name'],
        'amount': contributor['amount']
    })


@app.route('/index/download/<name>', strict_slashes=False)
def downloadFile(name):
    """Method to download CV
    """
    path = name + ".pdf"
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
