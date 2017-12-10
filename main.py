# -*- coding: utf-8 -*- 
import sys
import StringIO
import json
import logging
import random
import urllib
import urllib2
import pickle
import datetime
#from pytz.gae import pytz

# for sending images
from PIL import Image
import multipart

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

LUNCH = u'Обед'
BREAKFAST = u'Завтрак'
MEAL_DB = 'meal.db'

reload(sys)
sys.setdefaultencoding('utf8')

TOKEN_FILE = 'secret.token'
with open(TOKEN_FILE, 'r') as myfile:
    TOKEN=myfile.read().strip()
assert len(TOKEN) == 45

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False


class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))

class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))

def reply_order(person, wday, hday):
    meal = ""
    msg = u''
    # if hday < 12:
    #     msg = BREAKFAST
    #     meal = BREAKFAST
    # else:
    msg = LUNCH
    meal = LUNCH
    with open(MEAL_DB, 'rb') as f:
        meal_db = pickle.load(f)
        if wday not in meal_db[meal]:
            msg = u"No work - no food. That's the law."
        elif person not in meal_db[meal][wday]:
            msg = u"You did not order."
        else:
            msg += "\n" + u"\n".join(meal_db[meal][wday][person])
    f.close()
    return msg


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        update_id = body['update_id']
        message = body['message']
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        chat = message['chat']
        chat_id = chat['id']

        if not text:
            logging.info('no text')
            return

        def reply(msg=None, img=None):
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg.encode('utf-8'),
                    'disable_web_page_preview': 'true',
                    'reply_to_message_id': str(message_id),
                })).read()
            elif img:
                resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [
                    ('chat_id', str(chat_id)),
                    ('reply_to_message_id', str(message_id)),
                ], [
                    ('photo', 'image.jpg', img),
                ])
            else:
                logging.error('no msg or img specified')
                resp = None

            logging.info('send response:')
            logging.info(resp)

        if text.startswith('/'):
            if text == '/start':
                reply('Bot enabled')
                setEnabled(chat_id, True)
            elif text == '/stop':
                reply('Bot disabled')
                setEnabled(chat_id, False)
            elif text == '/image':
                img = Image.new('RGB', (512, 512))
                base = random.randint(0, 16777216)
                pixels = [base+i*j for i in range(512) for j in range(512)]  # generate sample image
                img.putdata(pixels)
                output = StringIO.StringIO()
                img.save(output, 'JPEG')
                reply(img=output.getvalue())
            elif text.startswith('/test'):
                params = text.split(" ")
                msg = reply_order(params[1], int(params[2]), int(params[3]))
                reply(msg)
            else:
                reply('What command?')

        # CUSTOMIZE FROM HERE

        elif 'who are you' in text:
            reply('I am you waiter. Ready to serve.')
        elif 'what time' in text:
            reply('Look at the top of your screen.')
        elif 'wtf' in text.lower():
            reply("Be patient - or go fasten")
        else:
            if getEnabled(chat_id):
                person = text.lower()
                now = datetime.datetime.utcnow()
                #now = datetime.datetime.now(pytz.timezone('Europe/Moscow')) #import pytz breaks the app not work
                wday = int(now.strftime("%w"))
                hday = (int(now.strftime("%H")) + 3) #% 24 #TODO

                msg = reply_order(person, wday, hday)
                reply(msg)
            else:
                reply("Bot is resting. Use old-fashioned papersheet please.")
            return

app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
