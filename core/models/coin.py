from django.db import models
from django.utils.functional import cached_property


class Coin(models.Model):
    name = models.CharField(max_length=255)
    ticker = models.CharField(max_length=10)
    color = models.IntegerField(default=0x696969)
    scan = models.BooleanField(default=False)

    @cached_property
    def img_url(self):
        return f'https://cryptologos.cc/logos/{self.name.lower()}-{self.ticker.lower()}-logo.png'

    def __str__(self):
        return f'{self.name} {self.ticker}'
