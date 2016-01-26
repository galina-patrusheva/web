from django.db import models
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .exceptions import Error
import bleach
import user_agents


# Create your models here.
class Album(models.Model):
    name = models.CharField(max_length=128)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return '{} ({})'.format(self.name, self.date)


class Photo(models.Model):
    big_name = models.CharField(max_length=128)
    preview_name = models.CharField(max_length=128)
    album = models.ForeignKey(Album)

    def get_likes(self):
        return Like.objects.filter(photo=self).count()

    def liked_by_user(self, user):
        try:
            Like.objects.get(photo=self, user=user)
        except Like.DoesNotExist:
            return False
        return True

    def like(self, user):
        like = Like(photo=self, user=user)
        like.save()

    def unlike(self, user):
        like = Like.objects.get(photo=self, user=user)
        like.delete()

    def __str__(self):
        return self.big_name


class GalleryUser(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    confirmed = models.BooleanField()
    confirm_token = models.CharField(max_length=128, null=True)

    def __str__(self):
        return '{} ({} {})'.format(self.email, self.first_name, self.last_name)

    @property
    def formated_user_name(self):
        return '{first_name} {last_name}'.format(first_name=self.first_name,
                                                 last_name=self.last_name)

    @staticmethod
    def get_user_by_email(email):
        return GalleryUser.objects.get(email=email)

    @staticmethod
    def get_confirmed_user_by_id(user_id):
        return GalleryUser.objects.get(pk=user_id, confirmed=True)

    @staticmethod
    def confirm_user(token):
        user = GalleryUser.objects.get(confirm_token=token)
        user.confirmed = True
        user.confirm_token = None
        user.save()
        return True

    def is_confirmed(self):
        return self.confirmed

    def try_auth(self, password):
        if self.is_confirmed() and check_password(password, self.password):
            return True
        return False


class Comment(models.Model):
    text = models.CharField(max_length=256)
    datetime = models.DateTimeField()
    author = models.ForeignKey(GalleryUser)
    photo = models.ForeignKey(Photo)
    prev_comment = models.ForeignKey('self', null=True, blank=True)
    last_comment = models.BooleanField(default=True)

    def __str__(self):
        return '{}: {}'.format(self.author.email, self.text)

    @staticmethod
    def get_comments_by_photo_id(photo_id):
        try:
            photo = Photo.objects.get(pk=photo_id)
        except Photo.DoesNotExist:
            photo = None
        comments = Comment.objects.all() \
            .filter(photo=photo, last_comment=True).order_by('datetime')
        return comments

    @staticmethod
    def get_last_comment_by_id(comment_id):
        return Comment.objects.get(pk=comment_id, last_comment=True)

    @property
    def safe_text(self):
        return bleach.clean(
            self.text,
            ['b', 'i', 'u', 's', 'img'],  # tags
            {'img': ['src', 'alt']},  # attributes
            []  # styles
        )

    def get_history(self):
        comment_history = []
        comment = self
        while comment.prev_comment is not None:
            comment = comment.prev_comment
            comment_history.append(comment)
        return comment_history

    def change_comment(self, new_text):
        if self.text == new_text:
            return
        self.last_comment = False
        new_comment = Comment(text=new_text, datetime=self.datetime,
                              author=self.author, photo=self.photo,
                              prev_comment=self)
        self.save()
        new_comment.save()

    def delete_comments_chain(self):
        comment = self
        while comment is not None:
            prev_comment = comment.prev_comment
            comment.delete()
            comment = prev_comment

    def rollback(self, rollback_comment):
        comment = self.prev_comment
        delete_comment_list = [self]
        while comment is not None:
            if comment == rollback_comment:
                break
            delete_comment_list.append(comment)
            comment = comment.prev_comment
        if comment is None:
            raise Error('Недопустимое действие')
        comment.last_comment = True
        comment.save()
        for comment in delete_comment_list:
            comment.delete()


class Visit(models.Model):
    ip = models.CharField(max_length=64)
    user_agent = models.CharField(max_length=256, null=True)
    user_resolution = models.CharField(max_length=64, null=True)
    datetime = models.DateTimeField()

    def __str__(self):
        return '[{}] IP: {}, UA: {}, {}'.format(
            self.datetime, self.ip, self.user_agent, self.user_resolution)

    @staticmethod
    def add_visit(ip, user_agent, resolution):
        visit = Visit(ip=ip, user_agent=user_agent,
                      user_resolution=resolution, datetime=timezone.now())
        visit.save()

    @staticmethod
    def get_last_by_ip(ip):
        return Visit.objects.all().filter(ip=ip).last()

    @property
    def user_agent_parsed(self):
        return str(user_agents.parse(self.user_agent))


class Counter(models.Model):
    DELTA = timedelta(days=1)
    today_views = models.IntegerField()
    today_visits = models.IntegerField()
    total_views = models.IntegerField()
    total_visits = models.IntegerField()
    day_point = models.DateTimeField()

    @staticmethod
    def get_counter():
        try:
            counter = Counter.objects.get()
        except Counter.DoesNotExist:
            counter = Counter(today_views=0, today_visits=0,
                              total_views=0, total_visits=0,
                              day_point=timezone.now())
            counter.save()
        now = timezone.now()
        if now > counter.day_point + Counter.DELTA:
            counter.day_point = now
            counter.today_views = 0
            counter.save()
        return counter

    @staticmethod
    def inc_counter():
        counter = Counter.get_counter()
        counter.today_views += 1
        counter.total_views += 1
        counter.today_visits = Visit.objects.filter(
            datetime__gt=counter.day_point).count()
        counter.total_visits = Visit.objects.count()
        counter.save()


class History(models.Model):
    datetime = models.DateTimeField()
    ip = models.CharField(max_length=32)
    user = models.ForeignKey(GalleryUser)
    user_agent = models.CharField(max_length=256)
    query = models.CharField(max_length=256)

    @property
    def user_agent_parsed(self):
        return str(user_agents.parse(self.user_agent))

    def __str__(self):
        return '[{}] {}: {}'.format(self.datetime, self.user.email, self.query)


class Like(models.Model):
    user = models.ForeignKey(GalleryUser)
    photo = models.ForeignKey(Photo)
