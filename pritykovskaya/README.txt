
Проект состоит из следующих модулей:

0) config.py - пользовательская конфигурации взаимодействия с SQL базой
и redis'ом
1) mysql_utils.py - подключение к sql базе и получение данных
2) redises.py - взаимодействие с redis key-value таблицами
3) common.py - список стоп слов, должен быть доступен в модулях
normalized.py, indexer.py, search_runner.py

4) normalizer.py - модуль, отвечающий за нормализацию всего и вся, путем взаимодействия с perl скриптом, на который перекладываются все содержательные действия
5) indexer.py - модуль, строящий все необходимые redis key-value таблицы, например "обратный индекс" или id_товара - название

6) search_runner.py - модуль, соспастовляющий тегу все возможные варианты товаров 

7) utils.py - все возможные утилиты

8) test.py - тест


Для того, чтобы начать работу с проектом нужно:

1) установить mysql
2) создать базу данных с помощью скрипта create_table.sql
3) наполнить ее при помощи скрипта insert_script.sql и команды
mysql -u root -p goods_db < /home/pritykovskaya/Desktop/python_project/insert_script.sql

4) установить redis (http://redis.io/) 
5) установить байдинги для redis'a под python (https://github.com/andymccurdy/redis-py)
 
6) установить perl библиотеки с помощью команды cpan LWP

7) запустить функцию setup из модуля test.py
