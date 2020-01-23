import mysql.connector
import config
from pprint import pprint
import datetime
import helper


dbConnectCfg = {
    'user' : config.db_user ,
    'password' : config.db_password,
    'host' : config.db_host,
    'port' : config.db_port,
    'database' : config.db_scheme
}

alltemplates = "select * from " + config.db_prefix + "templates;"
allevents = "select * from " + config.db_prefix + "events;"

def QueryDB(query):
    cnx = mysql.connector.connect(**dbConnectCfg)
    cursor = cnx.cursor()

    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    cnx.close()
    if (config.debug):
        pprint(result)
    return result

def QueryDBParameter(query, par):
    cnx = mysql.connector.connect(**dbConnectCfg)
    cursor = cnx.cursor()
    par_esc = []
    for t in par:
        par_esc.append(helper.MySQLEscape(t))
    cursor.execute(query, par_esc)
    result = cursor.fetchall()
    cursor.close()
    cnx.close()
    if (config.debug):
        pprint(result)
    return result

def QueryDBParameterWOO(query, par):
    cnx = mysql.connector.connect(**dbConnectCfg)
    cursor = cnx.cursor()
    par_esc = []
    for t in par:
        par_esc.append(helper.MySQLEscape(t))
    result = cursor.execute(query, par_esc)
    cnx.commit()
    cursor.close()
    cnx.close()
    if (config.debug):
        pprint(result)
    return result

def ReadAllTemplates():
    templates = QueryDB(alltemplates)
    result = []
    for t in templates:
        temp = {}
        temp['id'] = t[0]
        temp['filename'] = t[1]
        result.append(temp)
    return result

def ReadSpecificTemplate(id):
    SQLReq = "select filename from " + config.db_prefix + "templates where id = %s ;"
    template = QueryDBParameter(SQLReq, (id,))[0]
    if (config.debug):
        pprint(template)
    result = {}
    result['id'] = id
    result['filename'] = template[0]
    return result

def ReadAllEvents():
    events = QueryDB(allevents)
    result = []
    for t in events:
        temp = {}
        temp['id'] = t[0];
        temp['organization'] = t[1]
        temp['measure'] = t[2]
        temp['template'] = ReadSpecificTemplate(t[3])
        temp['measure_periode'] = t[4]
        result.append(temp)
    return result

def GetGroupsByEID(eid):
    SQLReq = "select distinct ugid from " + config.db_prefix + "groups where event = %s ;"
    persons = QueryDBParameter(SQLReq, (eid,))
    if (config.debug):
        pprint('Grouplist in GetGroupsByEID')
        pprint(persons)
    tmp = []
    for x in persons:
        if config.debug:
            pprint("X in GetGroupsByEID: " + str(x[0]))
        tmp.append(x[0])
    if (config.debug):
        pprint(tmp)
    return tmp

def GetParticipantsByEIDGID(eid, gid):
    SQLReq = "select * from " + config.db_prefix + "participants where event = %s and grp = %s ;"
    persons = QueryDBParameter(SQLReq, (eid, gid,))
    result = []
    for t in persons:
        tmp = {}
        tmp['id'] = t[0]
        tmp['name'] = t[2]
        tmp['university'] = t[3]
        result.append(tmp)
    if config.debug:
        pprint(result)
    return result

def ReadPersonsWOG(eid):
    SQLReq = "select * from " + config.db_prefix + "participants where event = %s ;"
    persons = QueryDBParameter(SQLReq, (eid,))
    result = []
    for t in persons:
        tmp = {}
        tmp['id'] = t[0]
        tmp['name'] = t[2]
        tmp['university'] = t[3]
        result.append(tmp)
    return result

def checkGrp(id):
    SQLReq = "select ugid from " + config.db_prefix + "groups where event = %s ;"
    persons = QueryDBParameter(SQLReq, (id,))
    if len(persons) > 0:
        return True
    else:
        return False

def ReadEventWG(id):
    SQLReq = "select * from " + config.db_prefix + "events where id = %s ;"
    event = QueryDBParameter(SQLReq, (id,))[0]
    t = event
    temp = {}
    temp['id'] = t[0];
    temp['organization'] = t[1]
    temp['measure'] = t[2]
    temp['template'] = ReadSpecificTemplate(t[3])
    temp['measure_periode'] = t[4]
    temp['type'] = 'g'
    pers = {}
    for x in GetGroupsByEID(id):
        if config.debug:
            pprint("X in ReadEventWG:" + str(x))
        pers[str(x)] = GetParticipantsByEIDGID(id, x)
    temp['groups'] = pers
    temp['days'] = ReadListOfDays(id)
    if config.debug:
        pprint(temp)
    return temp

def ReadEventWOG(id):
    SQLReq = "select * from " + config.db_prefix + "events where id = %s ;"
    event = QueryDBParameter(SQLReq, (id,))[0]
    ReadListOfDays(id)
    t = event
    temp = {}
    temp['id'] = t[0];
    temp['organization'] = t[1]
    temp['measure'] = t[2]
    temp['template'] = ReadSpecificTemplate(t[3])
    temp['measure_periode'] = t[4]
    temp['type'] = 'p'
    temp['persons'] = ReadPersonsWOG(id)
    temp['days'] = ReadListOfDays(id)
    if config.debug:
        pprint(temp)
    return temp

def ReadListOfDays(id):
    SQLReq = "select * from " + config.db_prefix + "times where event = %s ;"
    event = QueryDBParameter(SQLReq, (id,))[0]
    start = event[1]
    end = event[2]
    deltad = end - start
    result = []
    for i in range(deltad.days + 1):
        result.append((start + datetime.timedelta(days=i)).strftime("%d.%m.%Y"))
    if (config.debug):
        pprint(start.strftime("%d.%m.%Y"))
        pprint(end.strftime("%d.%m.%Y"))
        pprint(deltad.days)
        pprint(result)
    return result

def insertEvent(e):
    SQLReq = "INSERT INTO " + config.db_prefix + "events (organization, measure, template, measure_periode) VALUES ( %s , %s , %s , %s );"
    tmp = []
    tmp.append(e['organization'])
    tmp.append(e['measure'])
    tmp.append(e['template'])
    tmp.append(e['measure_periode'])
    out1 = QueryDBParameterWOO(SQLReq, tmp)
    if (config.debug):
        pprint(out1)
    SQLReq = "Select id from " + config.db_prefix + "events where organization = %s and measure = %s and template = %s and measure_periode = %s ;"
    out = QueryDBParameter(SQLReq, tmp)
    if (config.debug):
        pprint(out)
    id = out[0][0]
    if (config.debug):
        pprint(id)
    SQLReq = "INSERT INTO " + config.db_prefix + "times (event, startdate, enddate) VALUES ( %s , %s , %s );"
    tmp2 = []
    tmp2.append(id)
    tmp2.append(e['startdate'])
    tmp2.append(e['enddate'])
    out2 = QueryDBParameterWOO(SQLReq, tmp2)
    if (config.debug):
        pprint(out2)
    return id

def insertPerson(e):
    tmp = {}
    if (config.debug):
        pprint(e)
    if "gid" not in e:
        SQLReq = "INSERT INTO " + config.db_prefix + "participants ( event, `name`, university ) VALUES ( %s , %s , %s );"
        pars = []
        pars.append(e['eid'])
        pars.append(e['name'])
        pars.append(e['university'])
        out2 = QueryDBParameterWOO(SQLReq, pars)
        tmp['result'] = out2
    else:
        grps = GetGroupByEID(e['eid'])
        ugid = -1
        for t in grps:
            if t['gid'] == e['gid']:
                ugid = t['ugid']
        if (config.debug):
            pprint(ugid)
        if (ugid == -1):
            InsertGrp(e['eid'], e['gid'])
            grps = GetGroupByEID(e['eid'])
            if (config.debug):
                pprint(grps)
            for t in grps:
                if t['gid'] == e['gid']:
                    ugid = t['ugid']
            if ugid == -1:
                tmp['result'] = "You failed."
        SQLReq = "INSERT INTO " + config.db_prefix + "participants ( event, `name`, university , grp ) VALUES ( %s , %s , %s , %s );"
        pars = []
        pars.append(e['eid'])
        pars.append(e['name'])
        pars.append(e['university'])
        pars.append(ugid)
        out2 = QueryDBParameterWOO(SQLReq, pars)
        tmp['result'] = out2
    return tmp

def GetGroupByEID(eid):
    SQLReq = "select * from " + config.db_prefix + "groups where event = %s ;"
    out1 = QueryDBParameter(SQLReq, (eid,))
    grps = []
    for t in out1:
        temp1 = {}
        temp1['eid'] = t[0]
        temp1['gid'] = t[1]
        temp1['ugid'] = t[2]
        grps.append(temp1)
    if (config.debug):
        pprint(out1)
        pprint(grps)
    return grps

def InsertGrp(eid, gid):
    SQLReq = "INSERT INTO " + config.db_prefix + "groups (event, group_id) VALUES ( %s , %s );"
    pars = []
    pars.append(eid)
    pars.append(gid)
    if (config.debug):
        pprint(SQLReq)
        pprint(pars)
    out = QueryDBParameterWOO(SQLReq, pars)
    if (config.debug):
        pprint(out)
    return out

def InsertTokenToDB(token):
    SQLReq = "INSERT INTO " + config.db_prefix + "auth ( token ) VALUES ( %s );"
    pars = []
    pars.append(token)
    if (config.debug):
        pprint(SQLReq)
        pprint(pars)
    out = QueryDBParameterWOO(SQLReq, pars)
    if (config.debug):
        pprint(out)
    SQLReq = "SELECT uid from " + config.db_prefix + "auth where token = %s ;"
    out = QueryDBParameter(SQLReq, pars)
    return out

def InsertMapping(uid, eid):
    SQLReq = "INSERT INTO " + config.db_prefix + "mapping ( uid, eid ) VALUES ( %s , %s )"
    pars = []
    pars.append(uid)
    pars.append(eid)
    if (config.debug):
        pprint(SQLReq)
        pprint(pars)
    QueryDBParameterWOO(SQLReq, pars)

def checkAccess(token, eid):
    SQLReq = "SELECT uid from " + config.db_prefix + "auth where token = %s ;"
    pars = []
    pars.append(token)
    uid = QueryDBParameter(SQLReq, pars)
    if config.debug:
        pprint(uid)
    SQLReq = "SELECT uid from " + config.db_prefix + "mapping where eid = %s ;"
    pars = []
    pars.append(eid)
    if config.debug:
        pprint(pars)
    uideid = QueryDBParameter(SQLReq, pars)
    if config.debug:
        pprint(uideid)
    check = (uid == uideid)
    if config.debug:
        pprint(check)
        pprint((uid == uideid))
    return check

def checkToken(token):
    SQLReq = "SELECT uid from " + config.db_prefix + "auth where token = %s ;"
    pars = []
    pars.append(token)
    uid = QueryDBParameter(SQLReq, pars)[0]
    if config.debug:
        pprint(uid)
    if uid[0] > 0:
        return True
    else:
        return False

def getUidFromToken(token):
    SQLReq = "SELECT uid from " + config.db_prefix + "auth where token = %s ;"
    pars = []
    pars.append(token)
    uid = QueryDBParameter(SQLReq, pars)[0]
    if config.debug:
        pprint(uid)
    return uid[0]

if __name__ == "__main__":
    exit(1)