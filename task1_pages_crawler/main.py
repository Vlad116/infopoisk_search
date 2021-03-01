import os
import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

folder_name = 'files'
os.mkdir(folder_name)

input_file = 'links.txt'
urls = [line.rstrip('\n') for line in open(input_file)]
urls_set = set(urls)
uniq_urls = list(urls_set)

index_file = open("index.txt", "a", encoding="utf-8")
iterator = 0

for url in uniq_urls:
    try:
        req_url = "http://" + url
        req = Request(
            req_url,
            headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        soup = BeautifulSoup(html, features="html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text_from_link = '\n'.join(chunk for chunk in chunks if chunk)
        print(text_from_link)

    except urllib.request.HTTPError as error:
        output = format(error)
        print(output)
        print(url + " HTTP Error")
    else:
        iterator += 1
        print(str(iterator) + '. ' + url + " ... ", end='')

        filename = folder_name + '/' + 'выкачка_' + url + '_' + str(iterator) + ".txt"
        page = open(filename, "a", encoding="utf-8")
        page.write(text_from_link)
        page.close()

        index_file.write(str(iterator) + ' ' + url + "\n")

index_file.close()