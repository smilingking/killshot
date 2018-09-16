__author__ = 'Nilesh'

import os
import wolframalpha
from flask import Flask, request, Response, redirect



try:
    import config
    wol_id = config.wolframalpha['app_id']
except:
    wol_id = os.environ.get('APP_ID')


if not wol_id:
    import sys
    print 'No config.py found exisiting...'
    sys.exit(0)


app = Flask(__name__)

client = wolframalpha.Client(wol_id)


@app.route('/killshot',methods=['post'])
def thel():
    '''
    :Example:
    /thel current weather in mumbai?
    '''
    text = request.values.get('text')
    try:
        res = client.query(text)
    except UnicodeEncodeError:
        return Response(('sawaal puchhne nahi aata?'
                        '%s kya matlab iska?.' % text),
                        content_type='text\plain; charset=utf-8')
    resp_qs = ['Dekh Bhai "%s"\n' % text]
    resp_qs.extend(next(res.results).text)

    return Response(''.join(resp_qs),
                    content_type='text/plain; chatset=utf-8')

@app.route('/')
def hello():
    return redirect('https://github.com/smilingking/killshot')


if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0', port=port)
