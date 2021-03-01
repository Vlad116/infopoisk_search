import requests, os

search_query = 'новости'
max_requests = 6 # 30 lines per request
output_file = open("links.txt", "a", encoding="utf-8")

for i in range(max_requests):
    request = requests.get('https://www.liveinternet.ru/rating/today.tsv?;search='+ search_query +';page=' + str(i))
    data = request.text.split("\n")
    for row in data[1:30]:
        url = row.split("\t")[1].replace("/", "")
        print(url + '\n', end='')
        output_file.write(url + "\n")

output_file.close()