# rss2reMarkable

rss2reMarkable is a small python script that will fetch your favorite RSS feeds to build a single PDF document that will be pushed to the reMarkable Cloud using their public API.

## Instalation (requirements)
### Python modules

$ pip install pytz pypandoc feedparser

### Pandoc
$ sudo apt-get install pandoc texlive-latex-base texlive-fonts-recommended

### rMapi (reMarkable API Client - GO)
$ cd rss2reMarkable/

$ go get -u github.com/juruen/rmapi

$ go build -a github.com/juruen/rmapi

## Configuration
Add the RSS feed URLs in the feeds.txt file, and then run rmapi to add your unique code:

$ ./rmapi

## Execute

$ python rssFetcher.py
