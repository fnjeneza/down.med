#!/usr/bin/env python3
#*-*Coding: UTF-8 *-*
__author__ = "fnjeneza"

from urllib.request import urlopen, Request
from urllib.parse import urlencode, urlparse
import re
import subprocess
import getopt, sys

def uptobox(url):
    header = {"User-Agent":''}
    req = Request(url, headers = header)

    page = urlopen(req)
    html = page.read().decode()
    
    # check if there is a waiting time
    wait_regex = re.compile(r'wait\s(?P<wait_t>\d+)\s(minutes|seconds)')
    has_to_wait = wait_regex.search(html)
    # if has_to_wait is not None
    if has_to_wait:
        # time to wait
        wait_time = has_to_wait.group(0)
        raise Exception(wait_time)

    #input's attribut: name and value
    attr_regex = re.compile(r'<input.*name="(?P<name>.*)"\svalue="(?P<value>.*)">')
    attr_list = attr_regex.findall(html)

    #data to send
    _data = {}
    # name of the file
    fname=''
    # parameter/data to send in POST
    for attr in attr_list:
        name = attr[0]
        value = attr[1]
        _data[name]=value
        if(name=="fname"):
            fname = value

    _data = urlencode(_data)
    _data = _data.encode()
    header['Content-type']="application/x-www-form-urlencoded"
    # set up the request
    req = Request(url,data = _data, headers=header)
    # send the request POST
    page = urlopen(req)
    # process the returned text/html
    html = page.read().decode()

    # regex to get link
    link_regex = re.compile(r'<a href="(?P<link>http://w+\d*.*'+fname+')">')
    # down link
    down_link = link_regex.search(html)
    down_link = down_link.group('link')

    cmd = "wget -c --show-progress --no-verbose "+down_link
    exitcode = subprocess.call(cmd.split())
    return exitcode

def unfichier(url):
    page = urlopen(url)
    html = page.read().decode()

    #check if there is a waiting time
    wait_regex = re.compile('\d+\sminutes')
    has_to_wait = wait_regex.search(html)
    if has_to_wait:
        #time to wait
        raise Exception('wait '+has_to_wait.group(0))

    # text in <td> balise
    td_regex = re.compile(r'<td.*>(?P<valeur>.*)</td>')
    # all text in td balise
    values = td_regex.findall(html)
    index = 0
    title_index = None
    for value in values:
        if value.find('Nom du fichier')>=0:
            next_is_title = True
            title_index = index+1
            break
        index+=1

    title = "from unfichier"
    if title_index:
        title = values[title_index]
    
    u = urlparse(url)
    query = u.query
    
    #parameters for POST
    param = urlencode({query:''})
    param = param.encode()
    req = Request(url,data=param)

    page = urlopen(req)
    html = page.read().decode()
    
    #retrieve the download link
    pattern = re.compile(r'<a.*href="(?P<link>.*?)".*>Cliquer.*</a>')
    link = pattern.search(html).group("link")

    #download the file
    cmd = ("wget -c -O "+title+" --show-progress --no-verbose "+link)
    exitcode=subprocess.call(cmd.split())
    return exitcode

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:],'d:',['--dir='])
    try:
        url = args[0]
        u = urlparse(url)
        host = u.hostname
        if host=="1fichier.com":
            code = unfichier(url)
        elif host == 'uptobox.com':
            code = uptobox(url)
        else:
            raise Exception('Unhandled host : '+host)

    except IndexError:
        print("Missing URL")
        exit(1)
    except Exception as e:
        print(e)
        exit(1)
