#sys libs
import os, sys
import hashlib
from datetime import date
from datetime import datetime
import fnmatch

import urllib.request
from urllib.error import HTTPError

#class for supportive functions for repetitive tasks
class Helpers:
    def __init__(self):
        self.data = []

#compute an unique hash for urls
    def computeMD5hash(string):
        m = hashlib.md5()
        m.update(string.encode('utf-8'))
        return m.hexdigest()

#change coding for html source codes
    def changeCoding(source):
        if type(source) == str:
            source = source.encode('utf-8')
        else:
            source = source.decode('utf-8')

        return str(source, 'utf-8', 'ignore')

#function to create log files for scraping tasks
    def saveLog(file_name, content, show):
        log_now = datetime.now()
        log_now = log_now.strftime('%Y-%m-%d_%H%M%S')
        log_path = os.getcwd() + "//" + file_name
        with open(log_path,'a+') as f:
            log_now = log_now+'\n'
            f.write(log_now)
            if(show == 1):
                print(log_now)
                c = content+'\n'
                f.write(c)
                if(show == 1):
                    print(c)
        f.close()

#replace html symbols to prepare the source code to write it into the database
    def html_escape(text):
        html_escape_table = {
            "&": "&amp;",
            '"': "&quot;",
            "'": "&apos;",
            ">": "&gt;",
            "<": "&lt;",
            "#": "&hash;"
        }
        """Produce entities within text."""
        return "".join(html_escape_table.get(c,c) for c in text)

#conver html symbols back
    def html_unescape(text):
        text = text.replace("&lt;", "<")
        text = text.replace("&gt;", ">")
        text = text.replace("&quot;", '"')
        text = text.replace("&apos;", "'")
        text = text.replace("&hash;", "#")
        text = text.replace("&amp;", "&")
        return text

#text matching function to check for plugins and tools in source code
    def matchText(text, pattern):
        text = text.lower()
        pattern= pattern.lower()
        check = fnmatch.fnmatch(text, pattern)
        return check

#helper to remove duplicates in lists
    def remove_duplicates_from_list(a_list):
        b_set = set(tuple(x) for x in a_list)
        b = [ list(x) for x in b_set ]
        b.sort(key = lambda x: a_list.index(x) )
        return b

#helper to validate urls
    def get_netloc(url):
        parsed = urlparse(url)
        return parsed.netloc

    def validate_url(url):
        try:
            urllib.request.urlretrieve(url)
        except:
            return False
        else:
            return True
