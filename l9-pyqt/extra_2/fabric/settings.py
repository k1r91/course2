
# --------------- Пример файла настроек Django-проекта ------------------------
# Содержит настройки для боевого и тестового окружения. 
# Настройки переключаются комментированием соответствующих строк.

'''#-T - тестовый сервер'''
'''#-P - боевой сервер'''

DEBUG = False #-P
# DEBUG = True  #-T
    
TEMPLATE_DEBUG = False #-P
# TEMPLATE_DEBUG = True #-T

ALLOWED_HOSTS = ['127.0.0.1', '10.11.0.94', '10.11.1.97'] #-P
# ALLOWED_HOSTS = ['127.0.0.1', '10.11.0.94', '10.11.1.70'] #-T


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'pagination',
    'django_cleanup',
    'daterange_filter',    
#    'debug_toolbar', #-T
)
