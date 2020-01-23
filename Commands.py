import generate_bmbf_list
import config
from pprint import pprint
import databaseConnect
import helper
import base64
from flask import jsonify

def NewPerson(p):
    if not databaseConnect.checkAccess(p['token'], p['eid']):
        return {'result': 'You shall not pass.'}
    tmp = {}
    tmp['eid'] = p['eid']
    tmp['name'] = p['name']
    tmp['university'] = p['university']
    if 'gid' in p:
        tmp['gid'] = p['gid']
    return databaseConnect.insertPerson(tmp)

def NewEvent(e):
    if not databaseConnect.checkToken(e['token']):
        return {'result': 'You shall not pass.'}
    uid = databaseConnect.getUidFromToken(e['token'])
    tmp = {}
    tmp['organization'] = e['organization']
    tmp['measure'] = e['measure']
    tmp['template'] = e['template']
    tmp['measure_periode'] = e['measure_periode']
    tmp['startdate'] = e['startdate']
    tmp['enddate'] = e['enddate']
    id = databaseConnect.insertEvent(tmp)
    if (config.debug):
        pprint(tmp)
    e['id'] = id
    databaseConnect.InsertMapping(uid, id)
    return e

def GeneratePDF(e):
    if not databaseConnect.checkAccess(e['token'], e['eid']):
        return {'result': 'You shall not pass.'}
    cont = generate_bmbf_list.mainDB(e['eid'])
    cont = helper.renameFile(cont)
    return jsonify({'result': 'generated', "File" : "https://" + config.dns + "/docs/" + cont})


def RequestTemplates(token):
    if not databaseConnect.checkToken(token):
        return {'result': 'You shall not pass.'}
    return databaseConnect.ReadAllTemplates()

if __name__ == "__main__":
    exit(1)