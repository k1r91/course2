
# Fabric - это Python-библиотека и консольная утилита
# для автоматизации действий по SSH.

# Официальный сайт проекта: http://www.fabfile.org/
# Для Python3 существует fork проекта под именем fabric3. 
# Все API-функции те же, что и в основной библиотеке
# Установка стандартна:  pip install fabric3

# Дополнительные материалы:
# http://adw0rd.com/2012/8/14/python-fabric/
# https://habrahabr.ru/post/141271/

# Ключом к работе утилиты fab будет файл fabfile.py. 
# Утилита fab будет запускать python-функции, описанные в этом файле.
# Вот как могут выглядеть команды для автоматизации через Fabric:

# > fab local_test  - debug-настройки в локальных файлах
# > fab local_product  - боевые настройки в локальных файлах
# > fab deploy_testbian - заливка боевого сайта на testbian

# При этом должен быть файл fabfile.py, в котором должны быть описаны 
# функции local_test, local_product, deploy_testbian

import os
from fabric.api import run, env, cd, roles
from fabric.operations import sudo, local
from fabric.contrib.files import comment, uncomment

# Списком можно перечислить несколько серверов, которые будут использоваться.
# Подключение к ним будет происходить вызовом функции roles().
env.roledefs['production'] = ['superman@10.11.1.97']
env.roledefs['testbian'] = ['tester@10.11.1.70']


def production_env():
    """ Окружение для "боевого" сервера
    """
    # Путь на локальной машине до файла с SSH-ключами
    env.key_filename = [os.path.join('docs','keys','product')]  

    # На сервере будем работать из под пользователя "web-admin"
    env.user = 'web-admin'               
    passwd = open('web-admin.pwd').read()
    env.password = passwd

    # Путь до каталога проекта (на сервере)
    env.project_root = '/srv/megasite'  

    
def test_env():
    """ Окружение для тестового сервера
    """
    # Локальный путь до файла с SSH-ключами
    env.key_filename = [os.path.join('docs','keys','testbian')]  
    # На сервере будем работать из под пользователя "tester"
    env.user = 'tester'  
    env.password = 'Mamb@T8'
    # Путь до каталога проекта (на сервере)
    env.project_root = '/home/tester/megasite'  

    
@roles('production')
def deploy_production():
    # Инициализация окружения
    production_env()  

    # Заходим в директорию с проектом на сервере
    with cd(env.project_root):  
        # Пуляемся из репозитория
        run('git pull origin master')  
        # Что-нибудь делаем. Например, собираем статику для Django-проекта
        run('python manage.py collectstatic --noinput')  
        # Перезапускаем apache2, чтобы показать, что мы это можем
        sudo('service apache2 restart')     
        
        
@roles('testbian')
def deploy_testbian():
    # Инициализация окружения
    test_env()      

    # Заходим в директорию с проектом на сервере
    with cd(env.project_root):  
        # Пуляемся из репозитория
        run('git pull origin master')  
        # Собираем статику для Django-проекта
        run('python manage.py collectstatic --noinput')  
        
        # Комментим продакшен
        # Для комментирования/раскомментирования также можно использовать функции
        # comment, uncomment из fabric.contrib.files
        # Пример файла с комментариями см. в файле settings.py
        run("sed -i.bak -r -e 's/^([a-zA-Z[:space:]=_]*)([^# ].+#-P.*)$/# \\1\\2/g' ./megasite/settings.py")
        
        # Раскомментим тест
        run("sed -i.bak -r -e 's/^# ?(.+#-T.*)$/\\1/g' ./megasite/settings.py")
        
        # Перезапускаем apache2, чтобы все файлы обработались
        sudo('service apache2 restart')     


# Локальная установка тестового окружения
def local_test():
    # Комментим продакшен
    local('"c:\\Program Files\\Git\\usr\\bin\\sed.exe" -i.bak -r -e '+
        "'s/^([a-zA-Z[:space:]=_]*)([^# ].+#-P.*)$/# \\1\\2/g' .\\megasite\\settings.py")
    
    # Раскомментим тест
    local('"c:\\Program Files\\Git\\usr\\bin\\sed.exe" -i.bak -r -e '+
           "'s/^# ?(.+#-T.*)$/\\1/g' .\\megasite\\settings.py)")
    
    
# Локальная установка продакшена
def local_product():
    # Комментим тест
    local('"c:\\Program Files\\Git\\usr\\bin\\sed.exe" -i.bak -r -e '+"'s/^([a-zA-Z[:space:]=_]*)([^# ].+#-T.*)$/# \\1\\2/g'"+' .\\chkptsite\\settings.py')
    
    # Раскомментим продакшен
    local('"c:\\Program Files\\Git\\usr\\bin\\sed.exe" -i.bak -r -e '+"'s/^# ?(.+#-P.*)$/\\1/g'"+' .\\chkptsite\\settings.py')
                       