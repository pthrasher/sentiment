#!/usr/bin/env python
# encoding: utf-8
"""
goodorbad.py

Created by Philip Thrasher on 2011-02-28.
Copyright (c) 2011 pthrash entuhpryzizz. All rights reserved.
"""

import sys, urllib, sentiment, json
import optparse


help_message = '''
The help message goes here.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def build_parser():
    """docstring for build_parser"""
    parser = optparse.OptionParser()
    parser.add_option('-q', action="store", default="apple", dest='query', help="what you want to search twitter for")
    parser.add_option('-p', action="store", default=10, dest='max_pages', type='int', help="the maximum number of twitter search result pages to fetch.")
    return parser

def get_tweets(query, max_pages=10):
    """docstring for get_tweets"""
    page = 0
    next_page = ""
    tweets = []
    baseurl = "http://search.twitter.com/search.json"
    print "Fetching pages:"
    while next_page != "done" and page < max_pages:
        page += 1
        print "%d" % page
        qs = next_page
        if next_page == "":
            qs = "?q=%s" % query
        content = json.loads(urllib.urlopen("%s%s" % (baseurl, qs,)).read())
        tweets += [result['text'] for result in content['results']]
        if content.get('next_page', None):
            if content['next_page'] != next_page:
                next_page = content['next_page']
            else:
                next_page = "done"
        else:
            next_page = "done"
    return tweets

def main(args):
    parser = build_parser()
    options, values = parser.parse_args(args)
    try:
        print "Searching for: %s." % options.query
        tweets = get_tweets(options.query, max_pages=options.max_pages)

        c = sentiment.Classifier()
        results = c.classify(tweets)
        positive = [result for result in results if result['classification'] == 'pos']
        negative = [result for result in results if result['classification'] == 'neg']
        print ""
        for result in results:
            if result['classification'] == 'pos':
                print "Good: %s\n" % result['content']
            else:
                print "Bad: %s\n" % result['content']
        unknown = len(tweets) - len(results)
        
        out = "Tweets analyzed: %d | Positive: %d | Negative: %d | Unknown: %s" % (len(tweets), len(positive), len(negative), unknown)
        metrics = "Percentiles - Positive: %d%%, Negative: %d%%" % (float(len(positive))/float(len(results))*100, float(len(negative))/float(len(results))*100)

        print "="*84
        print "= %s =" % out.center(80)
        print "= %s =" % metrics.center(80)
        print "="*84
            
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv))
