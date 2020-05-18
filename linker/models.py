import random
import string

from django.db import models


# Create your models here.
from django.urls import reverse
import uuid


class Link(models.Model):
    full_link = models.TextField()
    shortened_link = models.TextField(null=True, blank=True)
    redirects = models.IntegerField()

    def generate_shortened_link(self):
        self.__check_full_link()
        link = self.id_generator()
        link = reverse('linker:redirect_view', kwargs={'short_link': link})
        self.shortened_link = link
        self.save(force_update=True)
        return self

    def get_absolute_url(self):
        return reverse('linker:result', kwargs={'link_id': self.id})

    def __check_full_link(self):
        if self.full_link.startswith('http'):
            return self
        else:
            self.full_link = 'http://' + self.full_link
            self.save(force_update=True)
            return self

    @staticmethod
    def id_generator(size=8, chars=string.digits + string.ascii_letters):
        return ''.join(random.choice(chars) for _ in range(size))
