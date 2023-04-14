from django.contrib import admin
from .models import Room, Message, Topic
# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'created', 'updated']

@admin.register(Message)
class Messagedmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'room', 'body','created', 'updated']

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']