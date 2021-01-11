# Readme

Модуль предназначен для получения данных с API по заданным параметрам, приведения полученных данных к требуемому виду и запись в базу clickhouse. 

## Установка

```shell
$ python3.7 setup.py develop
$ export ROOT_PATH_FOR_DYNACONF=$PWD
```

Команда `export ROOT_PATH_FOR_DYNACONF=$PWD` нужна для указания пути к файлам конфигурации которые используются в программе

Так же необходимо создать в каталоге `config/` файл `.secrets.toml` в который поместить чувствительную информацию такую как имя пользователя и пароль доступа к базе и API.

```toml
[default]
# DB settings
user = 'username'
password = 'password'
# API settings
api_user = 'username'
api_password = 'password'
api_role =  ''
```

В дальнейшем могу переделать на использование Environments или volt

## Удаление

```shell
$ python3.7 setup.py develop -u
```


## Использование

```shell
$ api_parser --strt_time 2020-10-28T00:00:00+00:00 --end_time 2020-11-14T00:00:00+00:00
```

or

```shell
$ python3.7 -m api_parser --strt_time 2020-10-28T00:00:00+00:00 --end_time 2020-11-14T00:00:00+00:00
```

В модуле реализована справка

```shell
$ api_parser --help
usage: api_parser [-h] [-v] -s  -e  [-c]

Parses api for a certain range of time and writes the result in database

optional arguments:
  -h, --help           show this help message and exit
  -v, --version        show program's version number and exit
  -s , --strt_time     sampling start time in iso format
  -e , --end_time      sampling end time in iso format
  -c , --card_status   filtering by ID_CALL_RESULT_STATUS field. Choices: 0 -
                       all cards 1 - draft, 2 - filled card. Default 0.
```

## Структура пакета

```shell
├── api_parser
│   ├── common
│   │   ├── api_amr.py
│   │   ├── db_interaction.py
│   │   ├── json_parser.py
│   │   └── logger.py
│   ├── resources
│   │   ├── __init__.py
│   │   ├── call_result.json
│   │   ├── call_status.json
│   │   ├── id_attribute.json
│   │   ├── id_kind.json
│   │   └── oms_care_status.json
│   ├── __main__.py
│   └── run.py
├── config
│   ├── config.py
│   └── settings.toml
├── tests
│   ├── resources
│   │   ├── __init__.py
│   │   ├── normalize_data_for_hb_smp_table.py
│   │   ├── normalize_data_for_stl_smp_table.py
│   │   └── resp_example.json
│   ├── test_api_interconection.py
│   ├── test_argparse.py
│   ├── test_db_interconection.py
│   └── test_json_parser.py
├── Readme.md
├── requirements.txt
└── setup.py
```

**api_parser/** - основной каталог пакета и по совместительству сам пакета  
**api_parser/common** - вспомогательные модули  
**api_parser/resources** - все не python файлы. В первую очередь справочники которые используются в других модулях

**config/** - каталог содержащий конфигурационные файлы.

**tests/** - каталог с модульными тестами.

## Модули

**api_parser/run.py** - основной скрипт с логикой

**api_parser/common/api_amr.py** - реализует взаимодействие с API

**api_parser/common/json_parser.py** - реализует парсинг JSON, выборку нужных полей, приведение типов.

**api_parser/common/db_interaction.py** - реализует взаимодействие с БД. В том числе запись.

**api_parser/common/logger.py** - реализует модуль логирования.

## Справочники

**call_result.json**

**call_status.json**

**id_attribute.json**

**id_kind.json**

**oms_care_status.json**

## Настройки

Конфигурационные файлы программы находятся в каталоге `config/`:

**settings.toml** -  содержит основные настройками программы

**.secret.toml** - содержит чувствительную информацию такую как имя пользователя и пароль доступа к базе и API. Этот файл необходимо создать после клонирования репозитория.

## Логирование

Логирование происходит в текущий каталог.  
Настройки логирования задаются в конфигурационном файле.

Пример логов:

```log
15-Nov-20 18:36:56:api_parser.common.api_amr:DEBUG:Sending authentication request
15-Nov-20 18:36:57:api_parser.common.api_amr:DEBUG:Authentication has been successful
15-Nov-20 18:36:57:api_parser.common.api_amr:DEBUG:Sending data request
15-Nov-20 18:36:57:api_parser.common.api_amr:DEBUG:data has received
```
