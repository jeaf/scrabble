#!/usr/bin/python

import cgi
import cgitb

import scrabble

cgitb.enable()

form = cgi.FieldStorage()

print "Content-Type: text/html"
print
print '<html><head></head><body>'
for w in scrabble.lookup(form.getfirst('q', '')):
    print w + '<br/>'
print '</body></html>'

