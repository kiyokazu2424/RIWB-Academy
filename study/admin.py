from django.contrib import admin
from . models import Genre,Text,Comment,Thread,Reply

admin.site.register(Genre)
admin.site.register(Text)
admin.site.register(Comment)
admin.site.register(Thread)
admin.site.register(Reply)