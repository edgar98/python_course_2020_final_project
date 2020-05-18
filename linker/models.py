import random
import string

from django.db import models


# Create your models here.
from django.urls import reverse


# Create model Link
class Link(models.Model):
    full_link = models.TextField()  # Field containing full link entered by user
    shortened_link = models.TextField(null=True, blank=True)  # Shortened link
    redirects = models.IntegerField()  # Number of redirects on this link

    def generate_shortened_link(self):
        """
            This method generates short link for full link saved in model
            :return: Link(Model)
        """
        self.check_full_link()  # Normalize full link
        link = self.hash_generator()  # Call method to generate short link
        link = reverse('linker:redirect_view', kwargs={'short_link': link})  # Get short link absolute path
        self.shortened_link = link  # Write short link to model
        self.save(force_update=True)  # Save changes
        return self

    def get_absolute_url(self):
        """Returns model absolute URL

        Default method, returns absolute URL for model given
        :returns: Absolute URL for model
        :rtype: str
        """
        return reverse('linker:result', kwargs={'link_id': self.id})

    def check_full_link(self):
        """Adds 'http://' to full link

            Due to django's redirect mechanism, it can redirect to absolute
            path only if path starts with 'http://...'. This method adds such
            if there not

            :returns: Model itself for one-line style coding
        """
        if self.full_link.startswith('http'):  # Check link already have protocol
            return self
        else:  # If not
            self.full_link = 'http://' + self.full_link  # Add protocol string to full link
            self.save(force_update=True)  # Then save changes
            return self

    @staticmethod
    def hash_generator(size=8, chars=string.digits + string.ascii_letters):
        """Generates hash link

            This method is utility. It generates hash string for short link

            :parameter size: Length of output string
            :parameter chars: Chars used for generation

            :todo: Make it more complicated than random
        """
        return ''.join(random.choice(chars) for _ in range(size))  # Get random chars from set

    def increment_redirects(self):
        self.redirects += 1
        self.save(force_update=True)
