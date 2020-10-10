import sys
import irc.bot
import requests

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print 'Connecting to ' + server + ' on port ' + str(port) + '...'
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)
        

    def on_welcome(self, c, e):
        print 'Joining ' + self.channel

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        # If a chat message starts with an exclamation point, try to run it as a command
        if e.arguments[0].startswith('!'):
            args = e.arguments[0].split(' ')
            cmd = args[0][len('!'):]
            print('Received command: ' + e.arguments[0])
            self.do_command(e, cmd, args)

    def do_command(self, e, cmd, args):
        c = self.connection

        if cmd == "scrollspeed" or cmd == "ss":
            if len(args) < 2:
                c.privmsg(self.channel, "You must specify an argument!")
            else:
                try:
                    val = int(args[1])
                    f = open("twitch.txt","w+")
                    f.write("activate=ss" + args[1])
                    f.close() 
                    c.privmsg(self.channel, "Scrollspeed has been set to " + args[1])
                except ValueError:
                    c.privmsg(self.channel, "Argument is not a number!")

        elif cmd == "nv" or cmd == "nightvision":
            if len(args) < 2:
                c.privmsg(self.channel, "You must specify an argument!")
            elif args[1] == "on":
                message = "Activated Night Vision."
                f = open("twitch.txt","w+")
                f.write("activate=nv_on")
                f.close() 
                c.privmsg(self.channel, message)
            elif args[1] == "off":
                message = "Deactivated Night Vision."
                f = open("twitch.txt","w+")
                f.write("activate=nv_off")
                f.close() 
                c.privmsg(self.channel, message)
            else:
                c.privmsg(self.channel, "Unknown argument " + args[1] + ". Type !help for a list of commands")      
                
        elif cmd == "sb" or cmd == "spacebar":
            if len(args) < 2:
                c.privmsg(self.channel, "You must specify an argument!")
            elif args[1] == "enable":
                message = "Enabled Space Bar."
                f = open("twitch.txt","w+")
                f.write("activate=sb_enable")
                f.close() 
                c.privmsg(self.channel, message)
            elif args[1] == "disable":
                message = "Disabled Space Bar."
                f = open("twitch.txt","w+")
                f.write("activate=sb_disable")
                f.close() 
                c.privmsg(self.channel, message)
            else:
                c.privmsg(self.channel, "Unknown argument " + args[1] + ". Type !help for a list of commands")        
                
        elif cmd == "invert" or cmd == "inv":
            if len(args) < 2:
                c.privmsg(self.channel, "You must specify an argument!")
            elif args[1] == "enable":
                message = "Inverted Scroll Arrows."
                f = open("twitch.txt","w+")
                f.write("activate=inv_enable")
                f.close() 
                c.privmsg(self.channel, message)
            elif args[1] == "disable":
                message = "Uninverted Scroll Arrows."
                f = open("twitch.txt","w+")
                f.write("activate=inv_disable")
                f.close() 
                c.privmsg(self.channel, message)
            else:
                c.privmsg(self.channel, "Unknown argument " + args[1] + ". Type !help for a list of commands")        
        
        elif cmd == "room" or cmd == "r" or cmd == "rm":
            if len(args) < 2:
                c.privmsg(self.channel, "You must specify an argument!")
            elif args[1] == "random":
                message = "Warped to a Random Room."
                f = open("twitch.txt","w+")
                f.write("activate=rm_random")
                f.close() 
                c.privmsg(self.channel, message)
            else:
                c.privmsg(self.channel, "Warped to " + args[1])
                f = open("twitch.txt","w+")
                f.write("activate=rm" + args[1])
                f.close() 
                c.privmsg(self.channel, message)
                
                

        # The command was not recognized
        #else:
        #    c.privmsg(self.channel, "Unknown command: " + cmd + ". Type !help for a list of commands.")

def main():
    if len(sys.argv) != 5:
        print("Usage: twitchbot <username> <client id> <token> <channel>")
        sys.exit(1)

    username  = sys.argv[1]
    client_id = sys.argv[2]
    token     = sys.argv[3]
    channel   = sys.argv[4]

    bot = TwitchBot(username, client_id, token, channel)
    bot.start()

if __name__ == "__main__":
    main()
