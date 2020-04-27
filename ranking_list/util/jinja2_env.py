from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment



def jinja2_env(**args):
    en=Environment(**args)
    en.globals.update({
        'url':reverse,
        'static':staticfiles_storage.url,

    })

    return en


