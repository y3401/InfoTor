# InfoTor
Local DB InfoTor + http-server (Локальная поисковая система InfoTor)

Запуск через start.py

Дамп очередного бэкапа БД RuTracker.org берется с http://rutracker.org/forum/viewtopic.php?t=5290461  

Файл распаковать и поместить backup.\*.xml в каталог /UPDATE.

Если есть новый справочник форумов forums.csv, то его поместить в каталог /DB.

Время полной загрузки и обработки 12Гб порядка 2,5 часов. Если загружать только часть категорий - то меньше.

Вместо встроенного http сервера можно настроить стандартный http сервис в OS, например как настроить IIS в Windows в прилагаемом документе https://github.com/y3401/InfoTor/blob/master/IIS_Win10.docx
