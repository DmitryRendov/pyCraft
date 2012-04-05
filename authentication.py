import urllib
import urllib2
import getpass
import socket
import sys
import PacketManager
import time
import threading
import wx
import wxPython

sessionid = ""
username = ""

#Eclipse pyDev error fix
wx = wx

class Window(wx.Frame):
    
    def __init__(self, parent, title):
        self.username = ""
        self.sessionID = ""
        self.LoggedIn = False
            
        super(Window, self).__init__(parent, title=title, 
            size=(400, 100))
        
        self.InitializeServerBrowser()
        self.Show()

    def initialize(self):
        
        self.sizer = wx.GridBagSizer()
        
        self.label = wx.StaticText(self, -1, label=u'Username')
        self.sizer.Add( self.label, (0,0),(1,1), wx.EXPAND )
        
        self.entry = wx.TextCtrl(self,-1)
        self.sizer.Add(self.entry,(0,1),(1, 2),wx.EXPAND | wx.ALIGN_LEFT)
        self.Bind(wx.EVT_TEXT_ENTER, self.onPressEnterOnFields, self.entry)
        
        self.label2 = wx.StaticText(self, -1, label=u'Password')
        self.sizer.Add( self.label2, (2,0),(1,2), wx.EXPAND)
        
        self.entry2 = wx.TextCtrl(self, -1, style = wx.TE_PASSWORD)
        self.sizer.Add(self.entry2,(2,2),(2,2), wx.EXPAND | wx.ALIGN_LEFT)
        self.Bind(wx.EVT_TEXT_ENTER, self.onPressEnterOnFields, self.entry2)
        
        button = wx.Button(self,-1,label="Login")
        self.sizer.Add(button, (5,0))
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, button)
        
        self.status = wx.StaticText(self, -1,)
        self.sizer.Add(self.status,(5,1),(5,2), wx.EXPAND)
        
        self.sizer.AddGrowableCol(0)
        self.SetSizerAndFit(self.sizer) 
        
    def InitializeServerBrowser(self):
        
        self.sizer = wx.GridBagSizer()
        
        #Top label
        self.topLabel = wx.StaticText(self, -1, label=u'Logged in as ' + self.username + '! (Session id: ' + self.sessionID + ')')
        self.sizer.Add(self.topLabel, (0,0),(1,1), wx.EXPAND)
        #Top label
        
        #Address label
        self.addressLabel = wx.StaticText(self, -1, label=u'Server address')
        self.sizer.Add(self.addressLabel, (2,0), (1,2), wx.EXPAND)
        #Address lable
        
        #Address entry box
        self.AddressEntry = wx.TextCtrl(self, -1)
        self.sizer.Add(self.AddressEntry,(2,2),(2,2), wx.EXPAND)
        #Address entry box
        
        self.connectbutton = wx.Button(self, -1, label="Connect")
        self.sizer.Add(self.connectbutton,(4,0))
        
        self.sizer.AddGrowableCol(0)
        self.SetSizerAndFit(self.sizer) 
        
    def OnButtonClick(self, event):
        if(self.entry.GetValue() == ""):
            self.status.set("Enter a username sherlock")
            return
        if(self.entry2.GetValue() == ""):
            self.status.set("Enter a password you derp")
            return
        password = self.entry2.GetValue()
        username = self.entry.GetValue()
        self.status.SetForegroundColour(wx.BLUE)
        self.status.SetLabel("Logging in...")
        thread = MinecraftLoginThread(self, username, password)
        thread.start()
        while(thread.is_alive() == True):
            pass
        self.sizer.DeleteWindows()
        self.InitializeServerBrowser()
    
    def onPressEnterOnFields(self, event):
        if(self.entry.GetValue() == ""):
            self.status.set("Enter a username sherlock")
            return
        if(self.entry2.GetValue() == ""):
            self.status.set("Enter a password you derp")
            return
        password = self.entry2.GetValue()
        username = self.entry.GetValue()
        self.status.SetForegroundColour(wx.BLUE)
        self.status.SetLabel("Logging in...")
        thread = MinecraftLoginThread(self, username, password)
        thread.start()
        while(thread.is_alive() == True):
            pass
        self.sizer.DeleteWindows()
        self.InitializeServerBrowser()
        
class MinecraftLoginThread(threading.Thread):
    
    def __init__(self, window, username, password):
        threading.Thread.__init__(self)
        self.window = window
        self.username = username
        self.password = password
               
    def run(self):
        url = 'https://login.minecraft.net'
        header = {'Content-Type' : 'application/x-www-form-urlencoded'}
        data = {'user' : self.username, 
                'password' : self.password,
                'version' : '13'}
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data, header)
        opener = urllib2.build_opener()
        response = opener.open(req)
        response = response.read()
        if(response == "Bad login"):
            self.window.status.SetForegroundColour(wx.RED)
            self.window.status.SetLabel("Incorrect username or password!")
            return
        response = response.split(":")
        self.window.username = response[2]
        self.window.sessionID = response[3]
        self.window.LoggedIn = True
        KeepConnectionAlive(self.username, self.password).start()
        
class KeepConnectionAlive(threading.Thread):
    
    def __init__(self, username, password):
        threading.Thread.__init__(self)
        self.username = username
        self.password = password
     
    def run(self):
        while True:   
            url = 'https://login.minecraft.net'
            header = {'Content-Type' : 'application/x-www-form-urlencoded'}
            data = {'user' : self.username,
                    'password' : self.password,
                    'version' : '13'}
            data = urllib.urlencode(data)
            req = urllib2.Request(url, data, header)
            opener = urllib2.build_opener()
            opener.open(req)
            time.sleep(300)
        
if __name__ == "__main__":
    app = wx.App()
    Window(None, title='pyCraft')
    app.MainLoop()

"""
url = 'https://login.minecraft.net'
header = {'Content-Type' : 'application/x-www-form-urlencoded'}
username = raw_input("Enter your username: ")
password = getpass.getpass("Enter your password: ")
data = {'user' : username, 
        'password' : password,
        'version' : '13'}
data = urllib.urlencode(data)
req = urllib2.Request(url, data, header)
opener = urllib2.build_opener()
response = opener.open(req)
response = response.read()
response = response.split(":")
sessionid = response[3]
print "Your session id is: " + sessionid
mySocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
host = raw_input("Please enter host: ");
port = raw_input("Please enter port (return for 25565): ");
if(port == ""):
    port = 25565
else:
    port = int(port)
mySocket.connect ( ( host, port ) )
PacketManager.sendString("\x02", username + host + ":" + str(port), mySocket)
response = PacketManager.readStringFromSocket(mySocket)
print "Server id is: " + response['string']
serverid = response['string']
url = "http://session.minecraft.net/game/joinserver.jsp?user=" + username + "&sessionId=" + sessionid + "&serverId=" + serverid
response = urllib2.urlopen(url).read()
print "Response: " + response
if(response != "OK"):
    print "OH GOD RESPONSE IS NOT OK. QUITING NOW."
    sys.exit()
PacketManager.sendLoginRequest(mySocket, username)
while True:
    PacketManager.handleIncomingPacket(mySocket)
"""


