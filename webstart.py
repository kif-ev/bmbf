import config
import Commands
from pprint import pprint
from flask import Flask, redirect, url_for, request, jsonify, Response, make_response, send_file

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

@app.route('/test',methods = ['POST','GET',])
def test():
    if (request.is_json == False):
        if (config.debug):
            pprint(request.data)
        return "You failed"
    content = request.get_json()
    if (config.debug):
        pprint(content)
    return "sucess"

@app.route('/bmbf',methods = ['POST','GET',])
def bmbf():
    if (request.is_json == False):
        if (config.debug):
            pprint(request.data)
        return "You failed"
    content = request.get_json()
    if (config.debug):
        pprint(content)
    if (content['type'] == "NP"):
        result = Commands.NewPerson(content)
    elif (content['type'] == "NE"):
        result = Commands.NewEvent(content)
    elif (content['type'] == "GP"):
        result = Commands.GeneratePDF(content)
    elif (content['type'] == "RT"):
        result = Commands.RequestTemplates(content['token'])
    else:
        return "You Failed!"
    if not (content['type'] == "GP"):
        return jsonify(result)
    else:
        return result

@app.route('/docs/<id>')
def get_pdf(id=None):
    if id is not None:
        return send_file(id, attachment_filename='Event.pdf')
    return

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)