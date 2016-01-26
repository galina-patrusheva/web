from django.contrib import admin
from .models import Photo, Album, GalleryUser, Comment, Visit, History,\
    Like


# Register your models here.
class PhotoAdmin(admin.ModelAdmin):
    pass


class AlbumAdmin(admin.ModelAdmin):
    pass


class GalleryUserAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass


class VisitAdmin(admin.ModelAdmin):
    pass


class HistoryAdmin(admin.ModelAdmin):
    pass


class LikeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(GalleryUser, GalleryUserAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Visit, VisitAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Like, LikeAdmin)
