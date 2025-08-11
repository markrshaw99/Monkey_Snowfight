from django.urls import path
from .views import *

urlpatterns = [
    path('', chat_view, name="home"),
    path('<username>', get_or_create_chatroom, name="start-chat"),
    path('room/<chatroom_name>', chat_view, name="chatroom"),
    path('new_groupchat/', create_groupchat, name="new-groupchat"),
    path('edit/<chatroom_name>', chatroom_edit_view, name="edit_chatroom"),
    path('delete/<chatroom_name>', chatroom_delete_view, name="chatroom-delete"),
    path('leave/<chatroom_name>', chatroom_leave_view, name="chatroom-leave"),
    path('file-upload/<chatroom_name>', chat_file_upload, name="chat-file-upload"),
    path('older/<chatroom_name>', load_older_messages, name="load-older-messages"),
]