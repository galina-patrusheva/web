from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.utils import IntegrityError
from django.db.models.base import ValidationError
from .models import Album, GalleryUser, Photo, \
    Comment, Counter, Visit, History, Like
from .utils import make_graphic_counter, handle_views
from .exceptions import AccessDenied, Error
import os
import binascii
import datetime
import xml.etree.ElementTree as ET


# Create your views here.
languages = [
    'C++',
    'Java',
    'Python',
    'JavaScript',
    'Prolog',
    'Haskell',
    'HTML5/CSS3'
]


def render_error(request, message):
    return render(request, 'message.html', {
            'error_message': message
        })


def render_success(request, message):
    return render(request, 'message.html', {
            'success_message': message
        })


def index(request):
    return render(request, 'index.html', {'active': 'HOME',
                                          'languages': languages})


def contacts(request):
    return render(request, 'contacts.html', {'active': 'CONTACTS'})


def gallery(request):
    albums = Album.objects.all().order_by('-date')
    albums_info = []
    try:
        user = GalleryUser.get_confirmed_user_by_id(
            request.session.get('auth_user_id'))
    except GalleryUser.DoesNotExist:
        user = None
    for album in albums:
        albums_info.append({
            'id': album.pk,
            'name': album.name,
            'date': album.date,
            'description': album.description,
            'photos': Photo.objects.filter(album=album)
        })
    response = render(request, 'gallery.html', {'active': 'GALLERY',
                                                'albums_info': albums_info,
                                                'user': user})
    response['Access-Control-Allow-Headers'] = 'Cookies'
    return response


# Comments views
def signin(request):
    try:
        user = GalleryUser.get_user_by_email(email=request.POST.get('email'))
        if user.try_auth(request.POST.get('password')):
            request.session['auth_user_id'] = user.pk
            return redirect('/gallery/')
        else:
            raise AccessDenied('not authorized')
    except (GalleryUser.DoesNotExist, AccessDenied):
        return render_error(request, 'Неверное имя пользователя или пароль.')


def signup(request):
    try:
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')
        if not all([first_name, last_name, password, email]):
            raise AccessDenied('Не все поля заполнены.')
        new_user = GalleryUser(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            password=make_password(request.POST['password']),
            email=request.POST['email'],
            confirmed=False,
            confirm_token=binascii.hexlify(os.urandom(40)).decode('utf-8')
        )
        new_user.save()
        GalleryUser.confirm_user(new_user.confirm_token)
        return render_success(
            request,
            'Учетная запись создана успешно.')
    except AccessDenied as ex:
        return render_error(request, ex.message)
    except IntegrityError:
        return render_error(request,
                            'Пользователь с указанным E-mail уже существует.')


def signout(request):
    if 'auth_user_id' in request.session:
        del request.session['auth_user_id']
    return redirect('/gallery/')


def confirm(request):
    token = request.GET.get('confirm_token')
    try:
        GalleryUser.confirm_user(token)
        return render_success(request, 'Подтверждение прошло успешно.')
    except GalleryUser.DoesNotExist:
        return render_error(
            request,
            'Возникли ошибки при подтверждении учетной записи. '
            'Проверьте корректность токена.')


def add_comment(request):
    try:
        user = GalleryUser.get_confirmed_user_by_id(
            request.session.get('auth_user_id'))
        photo = Photo.objects.get(pk=request.POST['photoId'])
        comment = Comment(text=request.POST['text'],
                          datetime=datetime.datetime.now(),
                          author=user,
                          photo=photo)
        comment.full_clean()
        comment.save()
        return HttpResponse('success')
    except GalleryUser.DoesNotExist:
        return HttpResponse('Вы не авторизованы.')
    except Photo.DoesNotExist:
        return HttpResponse('Фото не существует.')
    except (KeyError, ValidationError):
        return HttpResponse('Ошибка. Проверьте правильность заполнения формы.')


def list_comment(request, photo_id):
    try:
        user = GalleryUser.get_confirmed_user_by_id(
            request.session.get('auth_user_id'))
    except GalleryUser.DoesNotExist:
        user = None
    comments = Comment.get_comments_by_photo_id(photo_id)
    return render(request, 'comments.html', {
        'comments': comments,
        'user': user
    })


def edit_comment(request, comment_id, action):
    try:
        user = GalleryUser.get_confirmed_user_by_id(
            request.session.get('auth_user_id'))
        last_comment = Comment.get_last_comment_by_id(comment_id)
        if user != last_comment.author:
            raise AccessDenied('Вы не можете редактировать чужие комментарии.')
        if action == 'edit':
            comment_history = last_comment.get_history()
            return render(request, 'edit_comment.html', {
                'history': comment_history,
                'last_comment': last_comment
            })
        elif action == 'delete':
            last_comment.delete_comments_chain()
            return HttpResponse('success')
        elif action == 'save':
            last_comment.change_comment(request.POST.get('text'))
            return redirect('/gallery/')
        elif action == 'rollback':
            rollback_comment = Comment.objects.get(
                pk=request.POST.get('rollback_comment_id'))
            last_comment.rollback(rollback_comment)
            return redirect('/gallery/')
    except GalleryUser.DoesNotExist:
        return render_error(request, 'Вы не авторизованы.')
    except Comment.DoesNotExist:
        return render_error(request, 'Комментария не существует.')
    except (AccessDenied, Error) as ex:
        return render_error(request, ex.message)


def like(request, photo_id):
    if request.method == 'GET':
        try:
            photo = Photo.objects.get(pk=photo_id)
        except Photo.DoesNotExist:
            return HttpResponse('error')
        try:
            user = GalleryUser.get_confirmed_user_by_id(
                request.session.get('auth_user_id'))
        except GalleryUser.DoesNotExist:
            user = None
        likes = photo.get_likes()
        liked = photo.liked_by_user(user)
        return HttpResponse(str(likes) + ';' + str(liked))
    else:
        try:
            photo = Photo.objects.get(pk=photo_id)
        except Photo.DoesNotExist:
            return HttpResponse('Фото не существует.')
        try:
            user = GalleryUser.get_confirmed_user_by_id(
                request.session.get('auth_user_id'))
        except GalleryUser.DoesNotExist:
            return HttpResponse('Вы не авторизованы.')
        if photo.liked_by_user(user):
            photo.unlike(user)
        else:
            photo.like(user)
        return HttpResponse('success')


@never_cache
def counter_views(request):
    if request.method == 'POST':
        handle_views(request)
        return HttpResponse()
    else:
        counter = Counter.get_counter()
        return HttpResponse(
            make_graphic_counter(counter),
            content_type="image/png"
        )


@login_required
def visits_view(request):
    visits = Visit.objects.all().order_by('-datetime')
    users = GalleryUser.objects.filter(confirmed=True)
    return render(request, 'visits.html', {'visits': visits, 'users': users})


@login_required
def history_view(request, user_id):
    try:
        user = GalleryUser.get_confirmed_user_by_id(user_id)
        history = History.objects.filter(user=user).order_by('-datetime')
        return render(request, 'history.html', {'history': history,
                                                'user': user})
    except GalleryUser.DoesNotExist:
        return render_error(request, 'Пользователя не существует')


def statistic(request):
    xml_header = b'<?xml version="1.0" encoding="UTF-8"?>\n'
    photos = Photo.objects.all()
    ET.dump(ET.Comment('lol'))
    root = ET.Element('Gallery')
    for photo in photos:
        photo_node = ET.SubElement(root, 'Photo')
        ET.SubElement(photo_node, 'PreviewName').text = \
            '/static/Portfolio/photos/' + photo.preview_name
        ET.SubElement(photo_node, 'Name').text = \
            '/static/Portfolio/photos/' + photo.big_name
        ET.SubElement(photo_node, 'Likes').text = str(photo.get_likes())
        comments_amount = Comment.objects\
                                 .filter(photo=photo, last_comment=True)\
                                 .count()
        ET.SubElement(photo_node, 'Comments').text = str(comments_amount)
    return HttpResponse(
        xml_header + ET.tostring(root),
        content_type='text/xml'
    )
