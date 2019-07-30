#!/usr/bin/env python
# encoding: utf-8

import feedparser as fp
import time
from datetime import datetime, timedelta
import pytz
import os
import codecs
import pypandoc
import re
from unidecode import unidecode

PANDOC = "/usr/bin/pandoc"
RMAPI = "./rmapi"
FEED_FILE = "feeds.txt"
feed_file = os.path.expanduser(FEED_FILE)
utc = pytz.utc
homeTZ = pytz.timezone('US/Central')

html_head=u"""<html>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width" />
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <meta name="apple-mobile-web-app-capable" content="yes" />
<style>
</style>
<title>THE DAILY NEWS</title>
</head>
<body>

"""

html_tail=u"""
</body>
</html>
"""

html_perpost=u"""
    <article>
        <h1><a href="{3}">{2}</a></h1>
        <p><small>By <i>{1}</i>, on {0}.</small></p>
         {4}
    </article>
"""

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
  cleantext = re.sub(cleanr, '', raw_html)
  #return re.sub(r'([^\s\w]|_)+', '', cleantext)
  return remove_non_ascii(cleantext)

def load_feeds():
    with open(feed_file, 'r') as f:
        return list(f)
        
def get_start_time():
    dt = datetime.now(homeTZ)
    if dt.hour < 2:
        dt = dt - timedelta(hours=24)
    start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    start = start.astimezone(utc)
    return start
    
def get_posts():
    print "Checking feeds"
    posts = []
    for s in load_feeds():
        f = fp.parse(s)
        try:
            blog = cleanhtml(f['feed']['title'])
            print 'Source:'+str(blog)
        except KeyError:
            continue
        print "Downloading entries"
        for e in f['entries']:
            try:
                when = e['updated_parsed']
            except KeyError:
                when = e['published_parsed']
            when =  utc.localize(datetime.fromtimestamp(time.mktime(when)))
            if when > get_start_time():
                title = cleanhtml(e['title'])
                try:
                    body = cleanhtml(e['content'][0]['value'])
                except KeyError:
                    body = cleanhtml(e['summary'])
                link = cleanhtml(e['link'])
                posts.append((when, blog, title, link, body))
    posts.sort()
    posts.reverse()
    if posts:
        litems = []
        print "Formating posts"
        for post in posts:
            q = [ x.encode('utf8') for x in post[1:] ]
            timestamp = post[0].astimezone(homeTZ)
            q.insert(0, timestamp.strftime('%b %d, %Y %I:%M %p'))
            litems.append(html_perpost.format(*q))
            
        print "Compiling newspaper"
        result = html_head + u"\n".join(litems) + html_tail
        with codecs.open('dailynews.html', 'w', 'utf-8') as f:
            f.write(result)
            
        if os.path.exists('dailynews.pdf'):
            print "Pushing updated file"
            cmd = RMAPI+" rm "+'dailynews'
            print cmd
            os.system(cmd)
            cmd = RMAPI+" put "+'dailynews.pdf'
            print cmd
            os.system(cmd)
            os.remove('dailynews.pdf')
        else:
            print("Can not delete the file as it doesn't exists")
        os.environ['PYPANDOC_PANDOC'] = PANDOC
        pypandoc.convert('dailynews.html', 'pdf', outputfile='dailynews.pdf', extra_args=['-V geometry:margin=1.5cm', '--standalone', '--table-of-contents'])
            
    return result
    
    
if __name__ == '__main__':
    get_posts()
