import requests
import time
import sendMail
import urllib

# set URL
url1 = "insert_url_1"
url2 = "insert_url_2"
url = [url1, url2]

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

while True:
    count = 0
    goodurl = []
    passing = False
    for x in url:
        req = urllib.request.Request(x, headers=headers)
        resp = urllib.request.urlopen(x)
        redirected = resp.geturl() != x  # redirected will be a boolean
        a = resp.geturl()
        if a == 'redirected_website_for_url1' or a == 'redirected_website_for_url2': # checks if there was a redirect in given URL
            print('no change in ' + url[count])
            print(a)
            goodurl.append(None)
        else:
            print('page no longer redirects at ' + x)
            goodurl.append(url[count])
            passing = True

        count += 1
    if passing:
        print(goodurl)
        sendMail.sendEmail(goodurl)
    # check again in 30 min
    print('will check again in 30 min')
    time.sleep(1800)
    # continue loop
    continue