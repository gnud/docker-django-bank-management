#!/usr/bin/python
"""
Replaces the 'bank' project with your 'project name'. It will replace the necessary settings in a
few files.
"""
import os


def replace(file, old, new):
    with open(file) as f:
        new_text = f.read().replace(old, new)

    with open(file, "w") as f:
        f.write(new_text)


def handle(project_name):
    replace("docker-compose.yml",
            "POSTGRES_DB_NAME=bank",
            "POSTGRES_DB_NAME={0}".format(project_name))

    replace("bank/manage.py",
            'os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bank.settings")',
            'os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{0}.settings")'.format(project_name))

    replace("bank/bank/settings.py",
            "ROOT_URLCONF = 'bank.urls'",
            "ROOT_URLCONF = '{0}.urls'".format(project_name))

    replace("bank/bank/settings.py",
            "WSGI_APPLICATION = 'bank.wsgi.application'",
            "WSGI_APPLICATION = '{0}.wsgi.application'".format(project_name))

    replace("bank/bank/wsgi.py",
            'os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bank.settings")',
            'os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{0}.settings")'.format(project_name))

    # Rename the 'bank' dir to 'your_project'
    os.rename("bank/bank", "bank/{0}".format(project_name))


if __name__ == "__main__":
    name = input("Project name: ")
    handle(name)
