from flask import Flask, render_template, request, make_response
import requests
import json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
@app.route('/index')
@app.route('/index/')
def home():
    return render_template('index.html')


@app.route('/listall')
@app.route('/listall/')
@app.route('/listall/<string:format>')
def listAll(format = None):
    k = request.args.get('top', default=-1, type=int)
    if k <= -1:
        k = None
    if format == None:
        format = 'json'
    else:
        format = format.lower()
    if requests.get('http://restapi:5000/listAll').text.strip() == '{}':
        return render_template('index.html', stuff = "The database is empty")
    if format == 'csv':
        r = requests.get('http://restapi:5000/listAll/csv?top='+str(k))
        b = r.text.replace('\\n','<br>')
        return render_template('index.html', stuff = b[1:-2])
    if format == 'json':
        r = requests.get('http://restapi:5000/listAll/json?top='+str(k))
        r = r.text
        return render_template('index.html', stuff = r)


@app.route('/listclose')
@app.route('/listclose/')
@app.route('/listclose/<string:format>')
def listclose(format = None):
    k = request.args.get('top', default=-1, type=int)
    if k <= -1:
        k = None
    if format == None:
        format = 'json'
    else:
        format = format.lower()
    if requests.get('http://restapi:5000/listAll').text.strip() == '{}':
        return render_template('index.html', stuff = "The database is empty")
    if format == 'csv':
        r = requests.get('http://restapi:5000/listCloseOnly/csv?top='+str(k))
        b = r.text.replace('\\n','<br>')
        return render_template('index.html', stuff = b[1:-2])
    if format == 'json':
        r = requests.get('http://restapi:5000/listCloseOnly/json?top='+str(k))
        r = r.text
        return render_template('index.html', stuff = r)

@app.route('/listopen')
@app.route('/listopen/')
@app.route('/listopen/<string:format>')
def listOpen(format = None):
    k = request.args.get('top', default=-1, type=int)
    if k <= -1:
        k = None
    if format == None:
        format = 'json'
    else:
        format = format.lower()
    if requests.get('http://restapi:5000/listAll').text.strip() == '{}':
        return render_template('index.html', stuff = "The database is empty")
    if format == 'csv':
        r = requests.get('http://restapi:5000/listOpenOnly/csv?top='+str(k))
        b = r.text.replace('\\n','<br>')
        return render_template('index.html', stuff = b[1:-2])
    if format == 'json':
        r = requests.get('http://restapi:5000/listOpenOnly/json?top='+str(k))
        r = r.text
        return render_template('index.html', stuff = r)

# @app.route('/listclose/<string:format>')
# def listcloses(format = None):
#     if format == None:
#         format = 'json'
#     if format == 'json':
#         # if format == 'he':
#         #     return "ho"
#         # if format == None:
#         #     format = ""
#         r = requests.get('http://restapi:5000/listCloseOnly/csv')
#         b = r.text.replace('\\n','<br>')
#         return make_response(b[1:-2])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
