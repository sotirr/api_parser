# Импорт недавно установленного пакета setuptools.
import setuptools


# Зависимости проекта.
with open('requirements.txt') as fp:
    requirements = fp.read()

# Функция, которая принимает несколько аргументов. Она присваивает эти значения пакету.
setuptools.setup(
    # Имя дистрибутива пакета. Оно должно быть уникальным.
    name="api_parser",
    # Номер версии вашего пакета. Обычно используется семантическое управление версиями.
    version="0.8",
    # Имя автора.
    author="Anton Borisov",
    # Его почта.
    author_email="a.borisov@hostco.ru",
    # URL-адрес, представляющий домашнюю страницу проекта.
    url="https://github.com/sotirr/api_parser.git",
    # Находит все пакеты внутри проекта и объединяет их в дистрибутив.
    packages=setuptools.find_packages(),
    # requirements или dependencies, которые будут установлены вместе с пакетом.
    install_requires=requirements,
    # Требуемая версия Python.
    python_requires='>=3.7',
    # точка входа для запуска через консоль
    entry_points={
        'console_scripts': [
            'api_parser = api_parser.run:main',
        ],
    },
)
