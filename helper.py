import os
import config
from pprint import pprint
import _mysql

def sha256name(filename):
    name = os.popen("sha256sum " + filename).read()
    name = name[0:name.index(' ')]
    name = name + ".pdf"
    return name

def renameFile(old):
    new = sha256name(old)
    os.system("mv " + old + " " + new)
    return new

def assimilatePersons(personList):
    result = []
    if (config.debug):
        pprint(personList)
    for x in personList:
        tmp = {}
        tmp['id'] = x['id']
        tmp['Name'] = x['name']
        tmp['Hochschule'] = x['university']
        result.append(tmp)
    return result

def MySQLEscape(input):
    output = _mysql.escape_string(str(input))
    return output

def GarbageCollect(files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)
        if (config.debug):
            pprint("File " + str(file) + " deleted.")
    return

def RenumberPersons(event):
    id = 1
    if (config.debug):
        pprint("renumerbering in Progress")
        pprint(event)
        pprint(event.keys())
        pprint("type: " + str(event['type']))
    if event['type'] == 'p' :
        temp = []
        for t in event['persons']:
            tmp = {}
            tmp['id'] = id
            tmp['name'] = t['name']
            tmp['university'] = t['university']
            if (config.debug):
                pprint("old:" + str(t[0]) + ", new: " + str(id))
            temp.append(tmp)
            id = id + 1
        event['persons'] = temp
    elif event['type'] == 'g' :
        grps = {}
        for x in event['groups'].keys():
            temp = []
            for t in event['groups'][x]:
                tmp = {}
                tmp['id'] = id
                tmp['name'] = t['name']
                tmp['university'] = t['university']
                temp.append(tmp)
                if (config.debug):
                    pprint("old:" + str(t['id']) + ", new: " + str(id))
                id = id + 1
            grps[x] = temp
        event['groups'] = grps
    return event

if __name__ == "__main__":
    exit(1)