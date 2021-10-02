# praktikum_new_diplom

![](https://github.com/StromeXb/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

###Описание:
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка».

###Порядок установки локально:
1. Создайте файл .env с переменными окружения в папке infra для работы с базой данных со следующим содержанием:
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

2. Создайте папку nginx и поместите в неё конфиг default.conf

3. Запустите в командной строке файл настройки следующей командой и следуйте инструкциям по настройке суперпользователя:
bash installer.sh

###Quickstart:
1. Ссылка на кабинет администратора: http://127.0.0.1/admin/
2. Ссылка на документацию по работе с API: http://127.0.0.1/redoc/

###Рабочая версия проекта доступна по ссылкам:
1. Ссылка на кабинет администратора: http://130.193.41.199/admin/
2. Ссылка на документацию по работе с API: http://130.193.41.199/redoc/

####Автор:
Брагин Юрий (stromex@yandex.ru)
