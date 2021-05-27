from django.contrib import admin
from .models import Profile, Roommate_Request, Match, Post
# Register your models here.
admin.site.register(Profile)
admin.site.register(Roommate_Request)
admin.site.register(Match)
admin.site.register(Post)
