import urllib2;
import sys;
#notes:
#	> Find <div id="mw-content-text" blah blah blah
#	> split html there, take later portion
#	> in the 2nd part, find first <p> and </p>
#	> Nuke everythin in square brackets
#	> Return the result

wikipeaURL = "http://en.wikipedia.org/wiki/"; # Add the actual site name later

def destroyAllBrackets(html):
	while "<" in html and ">" in html:
		html = html[:html.find("<")] + html[html.find(">") + 1:];
	return html;

def getFirstP(keyword):
	keyword = keyword.replace(" ", "_");
	realURL = wikipeaURL + keyword;

	try:
		page = urllib2.urlopen(realURL);
	except:
		return "Wikipedia article not found!";

	html = page.read().split('<div id="mw-content-text"')[1]
	html = html.split('div id="toc" class="toc"')[0];
	html = html.split("<p>")[1];
	html = destroyAllBrackets(html);
	return html;

print getFirstP(sys.argv[1]);
