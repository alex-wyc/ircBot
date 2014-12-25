import sys;
import socket;
import string;
import random;
import ssl;

HOST = "irc.freenode.net";
PORT = 6667;
NICK = "positron";
CHANNEL = "#stuyfyre";
PASSWORD = "stuycs";

outcoms = outcomes = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes", "Reply hazy try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again ", "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful", "no.", "START", "A", "B", "UP", "DOWN", "LEFT", "RIGHT", "SELECT"];

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.connect((HOST, PORT));
ircsocket = ssl.wrap_socket(s);
ircsocket.send("USER " + NICK + " " + NICK + " " + NICK + " :" + NICK + "\n");
ircsocket.send("NICK " + NICK + "\n");

joinChan(CHANNEL, PASSWORD);

connected = False;
stop = False;
greet = False;
irc = {
	"chan" : CHANNEL
}

def parse(line):

	if line.find("JOIN :#stuyfyre") != -1:
		username = line.split(":")[1].split("!")[0];
		if username.lower().find("bot") != -1:
			string = "KICK %s %s :positron is the ONLY real bot\n" %(irc['chan'], username);
			s.send(string);

def joinChan(chan, password):
	ircsocket.send("JOIN " + chan + " " + password + "\n");

while not stop:
	print connected;
	line = s.recv(1024);
	print line;

	if line.find("PRIVMSG %s" % irc['chan']) != 1:
		parse(line);

	elif line.find("PING") != -1:
		s.send("PONG :" + line.split(":")[1]);
		if not connected:
			s.send("JOIN %(chan)s stuycs\n" % irc);

			if not greet:
				greet = True;
				s.send("PRIVMSG %(chan)s :Bonjour tous les mondes!\n" % irc);

	if stop:
		break;
