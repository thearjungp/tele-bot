import requests
import json
import configparser as cfg

class chat_bot():
  def __init__(self, config):
    parser = cfg.ConfigParser()
    r = parser.read(config)
    t = parser.get("creds","token")
    self.token = t
    self.base = "https://api.telegram.org/bot{}/".format(self.token)
    # print(self.base)
  
  def get_updates(self, offset=None):
    geturl = self.base + "getUpdates?timeout=100"
    if offset:
      geturl = geturl + "&offset={}".format(offset + 1)
       
    print("\n" + geturl + "\n")
    
    a = requests.get(geturl)
    return json.loads(a.content)
    
  
  def send_message(self, msg, msg_type, chat_id):
    
    if msg_type == "text":
      sendurl = self.base + "sendMessage?text={}&chat_id={}".format(msg, chat_id)
    if msg_type == "sticker":
      sendurl = self.base + "sendSticker?sticker={}&chat_id={}".format(msg, chat_id)
    if msg_type == "photo":
      sendurl = self.base + "sendPhoto?photo={}&chat_id={}".format(msg, chat_id)  
    if msg_type == "voice":
      sendurl = self.base + "sendVoice?voice={}&chat_id={}".format(msg, chat_id)  
    if msg_type == "audio":
      sendurl = self.base + "sendAudio?audio={}&chat_id={}".format(msg, chat_id) 
    if msg_type == "txttospeech":
      sendurl = self.base + "sendAudio?chat_id={}".format(chat_id)
    if msg_type == "document":
      sendurl = self.base + "sendDocument?document={}&chat_id={}".format(msg, chat_id) 
    if msg_type == "location":
      sendurl = self.base + "sendLocation?latitude={}&longitude={}&chat_id={}".format(msg["latitude"], msg["longitude"], chat_id)
      
      
    if type(msg) != str:
      requests.post(sendurl, files =msg)
    else:
      requests.post(sendurl)
    
    
# bot = chat_bot("config.cfg")
# # bot.get_updates()
# bot.send_message("thalaiva",944092784)