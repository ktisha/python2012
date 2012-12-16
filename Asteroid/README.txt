Проект "Астероид"
Авторы: Сергей Карашевич, Кирилл Кононов (отсортировано по фамилии, а не по конрибуции ;) )
karashevich@gmail.com, kirill.a.kononov@gmail.com

Для работы с проектом необходимо поставить предварительно СУБД PostgreSQL (рекомендуется 9.2) и 
настроить ее в соответствии python2012\Asteroid\Django\asteroid\settings.py. Также настройки надо задать
в Parser.py  Для корректной работы с базой данных неоюходимо поставить адаптер psycopg2, его можно скачать:
www.stickpeople.com/projects/python/win-psycopg/psycopg2-2.4.5.win-amd64-py2.7-pg9.1.3-release.exe

Проект состоит 3х частей:
	- Parser.py - скрипт, который находит *.proclog файлы в текущей директории и во всех внутренних, 
		и кладет всю информацию в базу данных "asteroidb", которая управляется POstgreSQL.
	- БД "asterodb" в ней хранится вся распаршенная информация.
		"Image name" 		- имя файла изображения
		"Exposure"		- время экспозиции
		"CCD temperature		- температура ПЗС-матрицы
		"Filter"			- используемый фильтр
		"Mid-exposure time"	- время середины экспозиции
		"Latitude"		- широта обсерватории
		"Longitude"		- долгота обсерватории
		"Altitude"		- высота обсерватории
		"Astrometric catalog"	- астрометрический каталог для обработки
		"Image center RA"		- положение по alpha центра кадра
		"Image center DEC"	- положение по delta центра кадра
	- Django сайт, выводящий список всех асетроидов в базе данных и информацию по каждому из астреоидов.
#########
Для работы следует:
1) произвести начальную настройку и убедиться, что в python2012\Asteroid\Django\asteroid\settings.py 
и в python2012\Asteroid\Parser.py верно указаны настройки для "asteroidb".
2) Запустить скрипт python2012\Asteroid\Parser.py - он добавит в базу объекты из python2012\Asteroid\test\
3) Запустить сайт выполнить  python2012\Asteroid\Django\manage.py runserver
4) зайти в браузере на сайт localhost:8000
#########
Для более наглядного понимания процесса лучше ознакомиться с нашей презентацией.
	