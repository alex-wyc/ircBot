import sys;
import socket;
import string;
import random;

HOST = "irc.freenode.net";
PORT = 6667;
NICK = "positron";
CHANNEL = "#stuyfyre";

outcoms = outcomes = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes", "Reply hazy try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again ", "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful", "no.", "START", "A", "B", "UP", "DOWN", "LEFT", "RIGHT", "SELECT"];

s = socket.socket();
s.connect((HOST, PORT));
s.send("NICK " + NICK + "\n");
s.send("USER " + NICK + " " + NICK + " " + NICK + " :" + NICK + "\n");

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

while not stop:
	line = s.recv(1024);

	if line.find("PRIVMSG %s" % irc['chan']) != 1:
		parse(line);

	elif line.find("PING") != -1:
		s.send("PONG :" + line.split(":")[1]);
		if not connected:
			s.send("JOIN %(chan)s\n" % irc);

			if not greet:
				greet = True;
				s.send("PRIVMSG %(chan)s :Bonjour tous les mondes!\n" % irc);

	if stop:
		break;
