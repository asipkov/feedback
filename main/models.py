from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='media/user', verbose_name='avatar', blank=True)
    phone_number = models.CharField(max_length=15, default=" ", verbose_name='Номер телефона')
    ratings = GenericRelation(Rating, related_query_name='User')

    def __unicode__(self):
        return self.user, self.ratings

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def get_absolute_url(self):
        return reverse('profile',
                       args=[self.id])


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    name = models.TextField(verbose_name='comment from')
    name = models.CharField(max_length=20, default=" ", verbose_name='comment from')
    body = models.TextField(verbose_name='Отзыв')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.user)
