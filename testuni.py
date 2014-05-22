#!/usr/bin/python
# -*- coding: utf-8 -*-
def myfunction(text):
    try:
	#text2=text.decode('utf-8')
        text = unicode(text, 'utf-8')
    except TypeError:
	print 'error'
    return text

print(myfunction(u'cer\xF3n'))
