import httplib
from datetime import datetime

import schedule
import time

config = {
    'serviceHost': '127.0.0.1:5002',
    'uri': '/initiate_feeding',
    'feedingTime': [
        '21:33',
        '06:00',
        '18:00',
    ]
}


def job():
    print 'Opening connection with ' + config['serviceHost']

    connection = httplib.HTTPConnection(config['serviceHost'])

    print 'Request to ' + config['uri'] + '...'

    connection.request('POST', config['uri'], '{}', {'Content-Type': 'application/json'})
    response = connection.getresponse()

    print 'Remote service responded with code ' + str(response.status)

    if (response.status == 200):
        print 'Feeding process initiated at ' + datetime.now().strftime('%m.%d.%Y %H:%M')

    print '*********************************'


job()

print 'Configuring....'

for timeString in config['feedingTime']:
    schedule.every().day.at(timeString).do(job)
    print 'Job successfully registered to run at ' + timeString

print 'Starting scheduler'
print ''

while True:
    schedule.run_pending()
    time.sleep(1)
