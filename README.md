# rss2reMarkable

rss2reMarkable is a small python script that will fetch your favorite RSS feeds to build a single PDF document that will be pushed to the reMarkable Cloud using their public API.

## Automatic installation
Run `install.sh` and follow instructions:
```
$ ./install.sh
```

## Manual installation
### Python modules
```
$ pip install pytz pypandoc feedparser
```

### Pandoc
```
$ sudo apt-get install pandoc texlive-latex-base texlive-fonts-recommended
```

### rMapi (reMarkable API Client - GO)
```
$ cd rss2reMarkable/
$ go get -u github.com/juruen/rmapi
$ go build -a github.com/juruen/rmapi
```

## Configuration
You can add your RSS feeds to `feed.txt`.

To configure your unique code so rss2reMarkable can access your tablet please execute:
```
$ ./rmapi
```

## Execute

If you used automatic installation:
```
$ ./fetch.sh
```

If you installed manually you can just:
```
$ python rssFetcher.py
```