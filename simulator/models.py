import time
from django.db import models
from jsonfield import JSONField


class Project(models.Model):
    title = models.CharField("Название проекта", max_length=255, blank=True, null=True)

    host = models.CharField("Хост тестируемого приложения", max_length=255, blank=True, null=True)
    prefix = models.CharField("Префикс пути", max_length=255, blank=True, null=True)
    base_headers = JSONField("Тестер. Базовые заголовки", blank=True, null=True)
    variables = JSONField("Переменные", blank=True, null=True)

    out_request_modifiers = JSONField("Тестер. Модификаторы запроса ", blank=True, null=True)
    out_response_modifiers = JSONField("Тестер. Модификаторы ответа ", blank=True, null=True)
    in_request_modifiers = JSONField("Заглушка. Модификаторы запроса ", blank=True, null=True)
    in_response_modifiers = JSONField("Заглушка. Модификаторы ответа ", blank=True, null=True)

    def location(self):
        return f"{self.host}{self.prefix}"

    def get_headers(self):
        headers = self.base_headers.copy()
        all_variables = self.variables.copy()
        for key in headers.keys():
            headers[key] = headers[key] % all_variables
        return headers

    def get_variables(self):
        variables = {"current_time": str(int(time.time()))}
        if self.variables:
            variables.update(self.variables)
        return variables

    def __str__(self):
        return f'{self.id}: {self.title} ({self.host})'


class Case(models.Model):
    title = models.CharField("Название теста", max_length=255, blank=True, null=True)
    active = models.BooleanField("Тест активен", default=True, blank=True)

    out_url_path = models.CharField("Тестер. Метод АПИ", max_length=255, blank=True, null=True)
    out_request_method = models.CharField("Тестер. Метод", max_length=10, blank=True, null=True)
    out_request_body = JSONField("Тестер. Тело запроса", blank=True, null=True)
    out_response_code = models.IntegerField("Тестер. Ожидаемый код ответа", blank=True, null=True)
    out_response_body = JSONField("Тестер. Тело ответа", blank=True, null=True)

    in_url_path = models.CharField("Заглушка. Метод АПИ", max_length=255, blank=True, null=True)
    in_request_method = models.CharField("Заглушка. Метод", max_length=10, blank=True, null=True)
    in_request_body = JSONField("Заглушка. Тело запроса", blank=True, null=True)
    in_response_code = models.IntegerField("Заглушка. Код ответа", blank=True, null=True)
    in_response_body = JSONField("Заглушка. Тело ответа", blank=True, null=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f'{self.id}: {self.title} ({self.out_url_path})'


class State(models.Model):
    current_case = models.ForeignKey(Case, on_delete=models.CASCADE, blank=False, null=False)

    @classmethod
    def get_case(cls):
        states = cls.objects.all()
        return states[0].current_case if states else None

    @classmethod
    def set_case(cls, case):
        cls.objects.all().delete()
        cls.objects.create(current_case=case)
        return case
