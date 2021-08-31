from bot import chat_bot
import requests
import json
from gtts import gTTS

update_id = None

weather_api_key = "efafc7058eb2e839c7145092ddbc28fd"

bot = chat_bot("config.cfg")


def get_name(last_entry):
  name = last_entry["message"]["from"]["first_name"]
  if "last_name" in last_entry["message"]["from"]:
    name = name + last_entry["message"]["from"]["last_name"]
  return name

# def gather_data(update):
#   update = update["result"]
  
#   if update:
#     last_entry = update[len(update) - 1]
#     update_id = last_entry["update_id"]
#     recipient_id = last_entry["message"]["from"]["id"]
#     recipient_name = get_name(last_entry)
    
    
#     if "username" in last_entry["message"]["from"]:
#       recipient_uname = last_entry["message"]["from"]["username"]


while True:
  update = bot.get_updates(offset=update_id)
  update = update["result"]
  
  if update:
    last_entry = update[len(update) - 1]
    update_id = last_entry["update_id"]
    recipient_id = last_entry["message"]["from"]["id"]
    # recipient_name = get_name(last_entry)
    
    
    # if "username" in last_entry["message"]["from"]:
    #   recipient_uname = last_entry["message"]["from"]["username"]
    
    
    #message slicing    
    if "text" in last_entry["message"] and last_entry["message"]["text"]=="/repeat":
      while True:
        old_update_id = update_id
        update = bot.get_updates(offset=update_id)
        update = update["result"]
    
        if update:
          last_entry = update[len(update) - 1]
          update_id = last_entry["update_id"]
          recipient_id = last_entry["message"]["from"]["id"]
          recipient_name = get_name(last_entry)
          
          
          if "username" in last_entry["message"]["from"]:
            recipient_uname = last_entry["message"]["from"]["username"]
        
        if "text" in last_entry["message"] and last_entry["message"]["text"]=="/norepeat":
          break
        
        if "text" in last_entry["message"]:
          msg_type = "text"
          message = last_entry["message"]["text"]
        if "sticker" in last_entry["message"]:
          msg_type = "sticker"
          message = last_entry["message"]["sticker"]["file_id"]
        if "photo" in last_entry["message"]:
          msg_type = "photo"
          message = last_entry["message"]["photo"][0]["file_id"]
        if "voice" in last_entry["message"]:
          msg_type = "voice"
          message = last_entry["message"]["voice"]["file_id"]
        if "audio" in last_entry["message"]:
          msg_type = "audio"
          message = last_entry["message"]["audio"]["file_id"]
        if "document" in last_entry["message"]:
          msg_type = "document"
          message = last_entry["message"]["document"]["file_id"]
        if "video" in last_entry["message"]:
          msg_type = "video"
          message = last_entry["message"]["video"]["file_id"]
        if "location" in last_entry["message"]:
          msg_type = "location"
          message = last_entry["message"]["location"]
          
        if old_update_id != update_id:
          bot.send_message(message, msg_type, recipient_id)
    
    
    if "text" in last_entry["message"] and "/weather" in last_entry["message"]["text"]:
      city = last_entry["message"]["text"].split(" ")
      city.pop(0)
      # print(city)
      if city == []:
        bot.send_message("Proper usage is : /weather <city_name>", "text", recipient_id)
        
      if len(city) >= 1:
        if len(city) > 1:
          city = " ".join(city)
        if len(city) == 1:
          city = city[0]
        
        # print(city)
        
        weatherurl = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city, weather_api_key)
        
        weatherjson = json.loads(requests.get(weatherurl).content)
        
        if "message" in weatherjson:
          bot.send_message("city not found","text", recipient_id)
        else:
          
          city_name = weatherjson["name"]
          weather = weatherjson["weather"][0]["main"]
          longitude = weatherjson["coord"]["lon"]
          latitude = weatherjson["coord"]["lat"]
          temperature = weatherjson["main"]["temp"]
          feels_like = weatherjson["main"]["feels_like"]
          max_temp = weatherjson["main"]["temp_max"]
          min_temp = weatherjson["main"]["temp_min"]
          pressure = weatherjson["main"]["pressure"]
          humidity = weatherjson["main"]["humidity"]
          wind_speed = weatherjson["wind"]["speed"]
          country = weatherjson["sys"]["country"]
          
          
          weather_msg = """
          City name:  {}
Weather:  {}
Coordinates:
    Longitude:  {}
    Latitude:  {}
Temperature:  {}
Feels Like:  {}
Max-Temperature:  {}
Min-Temperature:  {}
Pressure:  {}
Humidity:  {}
Wind speed:  {}
Country:  s{}
          """.format(city_name, weather, longitude, latitude, temperature, feels_like, max_temp, min_temp, pressure, humidity, wind_speed, country)
          
          bot.send_message(weather_msg, "text", recipient_id)
          
          
          
    if "text" in last_entry["message"] and "/ipscan" in last_entry["message"]["text"]:
      ip = last_entry["message"]["text"].split(" ")
      ip.pop(0)
      
      if ip == []:
        bot.send_message("Proper usage is : /ipscan <ip_address>", "text", recipient_id)
      else:
        ip = ip[0]
        
        ipurl = "http://ip-api.com/json/" + str(ip) + "?fields=39579647"
        
        ipdata = json.loads(requests.get(ipurl).text) 
        
        ip_msg = "IP DETAILS : \n\n"
           
        for item in ipdata:
          ip_msg = ip_msg + str(item) + "   ->   " + str(ipdata[item]) + "\n"
      
          
        bot.send_message(ip_msg, "text", recipient_id)

    if "text" in last_entry["message"] and "/txttospeech" in last_entry["message"]["text"]:
      typedText = last_entry["message"]["text"].split(" ")
      typedText.pop(0)      
      
      if typedText == []:
        bot.send_message("Proper usage is : /txttospeech <your_text>", "text", recipient_id)
      else:
        typedText = " ".join(typedText)
        language = "en"
        output = gTTS(text=typedText, lang=language, slow=False)  
        output.save("audio.mp3")
        afile = {"audio": open("audio.mp3", 'rb')}
        bot.send_message(afile, "txttospeech", recipient_id)