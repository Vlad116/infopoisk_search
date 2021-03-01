# How to start the crawler?

1. Download and install Python. Select the option to add to system variables
2. Download this repository and go to the _task1_pages_crawler_ folder
3. Run on the command line
``,
pip install requests
pip install bs4
``,
4. Delete the old index.txt (and links.txt if change _search_query_) file
5. (Optional) You can modify the query for a set of sites by changing the _search_query_ parameter in create_links_list.py
6. Execute in the command line
``,
    python create_links_list.py
    python main.py
``,

# Как запустить crawler?

1. Загрузить и установить Python. Выбрать опцию по добавлению в системные переменные
2. Скачать этот репозиторий и перейти в папку _task1_pages_crawler_
3. Выполнить в командной строке 
```
pip install requests
pip install bs4
```
4. Удалить старый файл index.txt
5. (Опционально) Можно изменить запрос по набору сайтов, изменив параметр search_query в create_links_list.py
6. Выполнить в коммандной строке 
```
    python create_links_list.py
    python main.py
```