from bottle import route, run, template
import json, string
import config
from store import retreive


@route('/')
def index():
    return ('<b>Monitoring RD trace route</b>!')


@route('/get/all/seqnumber=<seqnumber:int>')
def getallinfo(seqnumber=0):

    json_value = {}

    json_value = json.dumps(retreive.get_all_info_since(seqnumber), sort_keys=True, indent=4, separators=(',', ': '))


    if json_value:
        return json_value

def main(host='147.83.35.241', port=8080):
    run(host=host,port=port)

if __name__ == '__main__':
    main()
