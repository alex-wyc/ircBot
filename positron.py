import sys;
import socket;
import string;
import random;
import hashlib;
import urllib2;

HOST = "irc.freenode.net";
PORT = 6667;
NICK = "positronBot";
INDENT = "positronbot";
CHANNEL = "#stuyfyre";
PASSWORD = "stuycs";
TOPIC = "We hold these shells to be self evident, that not all C derivatives are created equal, and that they are endowed by their compilers with certain inalienable instructions.";

outcomes = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes", "Reply hazy try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again ", "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful", "no.", "START", "A", "B", "UP", "DOWN", "LEFT", "RIGHT", "SELECT"];

banlist = ["charlesma", "bot"];

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.connect((HOST, PORT));
#ircsocket = ssl.wrap_socket(s);
s.send("NICK %s\r\n" % NICK);
s.send("USER %s %s %s :Positron Bot\r\n" % (INDENT, HOST, NICK))

def joinChan(chan, pwd):
	s.send("JOIN " + chan + " " + pwd + "\r\n");

joinChan(CHANNEL, PASSWORD);

s.send("MODE %s +k %s\r\n" % (CHANNEL, PASSWORD));
s.send("TOPIC %s :%s\r\n" % (CHANNEL, TOPIC));
s.send("MODE %s +t\r\n" % (CHANNEL));

slots = 6;

def parse(line):

	if line.find("JOIN") != -1:

		username = line.split(":")[1].split("!")[0];

		if username != NICK:
			for banel in banlist:
				if username.lower().replace(" ", "").find(banel) != -1:
					string = "KICK %s %s :The BAN HAMMER has struck\r\n" % (CHANNEL, username);
					s.send(string);
					break;

		if username == "hiWorld" or username == "photoXin":
			string = " MODE %s +o %s\r\n" % (CHANNEL, username);
			s.send(string);

	if line.find("NICK") != -1:

		newUsername = line.split(":")[-1];

		for banel in banlist:
			if newUsername.lower().replace(" ", "").find(banel) != -1:
				string = "KICK %s %s :The BAN HAMMER has struck\r\n" % (CHANNEL, newUsername);
				s.send(string);
				break;

	if len(line.split(":")) == 3:

		username = line.split(":")[1].split("!")[0];
		message = line.split(":")[2];

		if message.split(" ")[0].strip().strip(",").strip(":").lower() in ["hi", "hello", "hei"]: # Greeting Function

			s.send("PRIVMSG %s :Hello, %s\r\n" % (CHANNEL, username));

		if message.find("`") == 0:

			actual = message[1:].split(" ");
			command = actual[0];

			if command.find("roulette") != -1:

				global slots
				rang = random.random();

				if rang < (1.0 / slots):
					slots = 6;
					s.send("KICK %s %s :You died! D:\r\n" % (CHANNEL, username));
					s.send("PRIVMSG %s :*reloads chambers*, there are %d slots left\r\n" % (CHANNEL, slots));

				else:
					slots = slots - 1;
					s.send("PRIVMSG %s :*click*, there are %d slots left\r\n" % (CHANNEL, slots));

			if command.find("md5") != -1:
				try:
					stuff = message[5:].replace("\r\n", "");
					result = hashlib.md5();
					result.update(stuff);

					if len(stuff) < 1:
						raise Exception();

					s.send("PRIVMSG %s :md5 of \"%s\" is %s\r\n" % (CHANNEL, stuff, result.hexdigest()));

				except Exception:
					s.send("PRIVMSG %s :Usage: `md5 [stuff]\r\n" % CHANNEL);

			if command.find("hf") != -1:
				s.send("PRIVMSG %s :%s, %s\r\n" % (CHANNEL, username, random.choice(outcomes)));

			if command.find("roll") != -1:
				try:
					top = int(message[6:].replace("\r\n", ""));
					result = random.randrange(0,top);
					s.send("PRIVMSG %s :%s, you rolled %d\r\n" % (CHANNEL, username, result));

				except Exception:
					s.send("PRIVMSG %s :F**k you %s, I hope you die a gruesome death\r\n" % (CHANNEL, username));

			if command.find("wiki") != -1:
				url = "http://en.wikipedia.org/wiki/" + message[6:].replace(" ", "_");

				#try:

while True:
	#print connected;
	line = s.recv(1024);
	print line;

	if line.find("PRIVMSG %s" % CHANNEL) != 1:
		parse(line);

	if line.find("PING :") != -1:

		s.send("PONG :Pong\r\n");
