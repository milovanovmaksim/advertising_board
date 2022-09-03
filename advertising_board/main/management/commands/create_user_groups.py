import json

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создание Group из json файла.'

    def add_arguments(self, parser):
        parser.add_argument('--json', type=str)

    def handle(self, *args, **options):
        json_data = self.get_json_data(**options)
        self.create_groups(json_data)

    def get_json_data(self, **options):
        path_json_file = options['json']
        try:
            with open(path_json_file) as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            CommandError(f'Файл {path_json_file} не неайден')
        return data

    def create_groups(self, json_data):
        for group in json_data:
            permissions = self.get_permissions(group)
            group, created = Group.objects.get_or_create(name=group['name_group'])
            group.permissions.add(*permissions)
            info = f"Создана группа <<{group}>>."
            self.stdout.write(self.style.SUCCESS(info))

    def get_permissions(self, group):
        code_name_permissons = group["code_name_permissions"]
        permissions = []
        for code_name_permission in code_name_permissons:
            permission, created = Permission.objects.get_or_create(codename=code_name_permission)
            permissions.append(permission)
        return permissions
