import sys, base64, json, requests, re

# Preparatioin of parms
DOMAIN = sys.argv[1]
AUTH = sys.argv[2]
RAWDATA = sys.argv[3]
URL_ZABBIX = sys.argv[4]
KEY_ZABBIX = sys.argv[5]

# Variables generates in code
TOKEN = ""
URL = ""
TICKETID = ""

def encodeAuth(auth):
    global TOKEN

    authString = auth
    authStringBytes = authString.encode("ascii")

    base64Bytes = base64.b64encode(authStringBytes)
    base64String = base64Bytes.decode("ascii")

    TOKEN = base64String

def setUrlZendesk(domain):
    global URL

    if domain == domain+"/":
        URL = domain+"api/v2/tickets.json"
    else:
        URL = domain+"/api/v2/tickets.json"

def makePayload():
    eventName = re.search("\"EVENT_NAME\": (.*?),", RAWDATA)
    server = re.search("\"HOST_NAME\": (.*?),", RAWDATA)
    opData = re.search("\"OP_DATA\": (.*?),", RAWDATA)
    eventId = re.search("\"EVENT_ID\": (.*?),", RAWDATA)

    message = "Problema: "+str(eventName[1])+"""
    Servidor: """+str(server[1])+"""
    Dados adicionais: """+str(opData[1])

    data = {
        'ticket': {
            'type': 'Incident',
            'status': 'new',
            'subject': 'Zabbix problem #'+str(eventId[1])+" - "+str(eventName[1]),
            'comment': {
                'body': message
            },
            'tags': 'Zabbix'
        }
    }

    return json.dumps(data)

def makeRequisition(url, token):
    global TICKETID

    payload = makePayload()
    headers = {'Content-Type': 'application/json', 'Authorization': 'Basic '+token}

    r = requests.post(url, data=payload, headers=headers)

    response = json.loads(r.text)

    ticket = response['ticket']
    TICKETID = ticket['id']

def updateAlarmZabbix():
    global URL_ZABBIX
    global KEY_ZABBIX
    
    eventId = re.search("\"EVENT_ID\": (.*?),", RAWDATA)
    

    payload = {
        'jsonrpc': '2.0',
        'method': 'event.acknowledge',
        'params': {
            'eventids': int(eventId[1]),
            'action': 4,
            'message': 'Aberto chamado Zendesk #'+str(TICKETID)
        },
        'auth': KEY_ZABBIX,
        'id': 1
    }
    headers = {'Content-Type': 'application/json-rpc'} 

    r = requests.post(URL_ZABBIX, data=json.dumps(payload), headers=headers)

def mainCode():
    encodeAuth(AUTH)
    setUrlZendesk(DOMAIN)
    makeRequisition(URL, TOKEN)
    updateAlarmZabbix()


if __name__ == "__main__":
    mainCode()
    sys.exit()
