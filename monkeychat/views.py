from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse
from django.contrib import messages
from django.http import Http404
from .models import *
from .forms import *



@login_required
def chat_view(request, chatroom_name='public-chat'):
    chat_group = get_object_or_404(ChatRoom, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]  # Get the last 30 messages
    form = ChatMessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404("You are not a member of this private chat group.")
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break

    if chat_group.groupchat_name:
        if request.user not in chat_group.members.all():
            if request.user.emailaddress_set.filter(verified=True).exists():
                chat_group.members.add(request.user)
            else:
                messages.warning(request, "You must verify your email to join this group chat.")
                return redirect('profile-settings')
            
    if request.htmx:
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message': message,
                'user': request.user,
            }
            return render(request, 'monkeychat/partials/chat_message_p.html', context)
        
    context = {
        'chat_messages': chat_messages,
        'form': form,
        'other_user': other_user,
        'chatroom_name': chatroom_name,
        'chat_group': chat_group,
    }
    return render(request, 'monkeychat/chat.html', context)

@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')
    
    other_user = User.objects.get(username=username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    chatroom = None
    if my_chatrooms.exists():
        for room in my_chatrooms:
            if other_user in room.members.all():
                chatroom = room
                break
    if not chatroom:
        chatroom = ChatRoom.objects.create(is_private=True)
        chatroom.members.add(other_user, request.user)

    return redirect('chatroom', chatroom_name=chatroom.group_name)

@login_required
def create_groupchat(request):
    form = NewGroupForm()

    if request.method == 'POST':
        form = NewGroupForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            return redirect('chatroom', new_groupchat.group_name)

    context = {
        'form': form,
    }
    return render(request, 'monkeychat/create_groupchat.html', context)

@login_required
def chatroom_edit_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatRoom, group_name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404("You do not have permission to edit this chat room.")
    
    form = ChatRoomEditForm(instance=chat_group)

    if request.method == 'POST':
        form = ChatRoomEditForm(request.POST, instance=chat_group)
        if form.is_valid():
            form.save()

            remove_members = request.POST.getlist('remove_members')
            for member_id in remove_members:
                member = User.objects.get(id=member_id)
                chat_group.members.remove(member)

            return redirect('chatroom', chatroom_name)

    context = {
        'form': form,
        'chat_group': chat_group,
    }

    return render(request, 'monkeychat/chatroom_edit.html', context)

@login_required
def chatroom_delete_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatRoom, group_name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404("You do not have permission to delete this chat room.")
    
    if request.method == 'POST':
        chat_group.delete()
        messages.success(request, "Chat room deleted successfully.")
        return redirect('home')
    
    return render(request, 'monkeychat/chatroom_delete.html', {'chat_group': chat_group})

@login_required
def chatroom_leave_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatRoom, group_name=chatroom_name)
    if request.user not in chat_group.members.all():
        raise Http404("You are not a member of this chat room.")
    
    if request.method == 'POST':
        chat_group.members.remove(request.user)
        messages.success(request, "You have left the chat room.")
        return redirect('home')


@login_required
def load_older_messages(request, chatroom_name):
    chat_group = get_object_or_404(ChatRoom, group_name=chatroom_name)
    offset = int(request.GET.get('offset', 0))
    older_messages = chat_group.chat_messages.all()[offset:offset+20]
    
    context = {
        'chat_messages': older_messages,
        'user': request.user
    }
    return render(request, 'monkeychat/partials/older_messages.html', context)

def chat_file_upload(request, chatroom_name):
    chat_group = get_object_or_404(ChatRoom, group_name=chatroom_name)
    
    if request.htmx and request.FILES:
        file = request.FILES['file']
        message = ChatMessage.objects.create(
            file=file,
            author=request.user,
            group=chat_group,
            original_filename=file.name
        )
        channel_layer = get_channel_layer()
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        async_to_sync(channel_layer.group_send)(
            chatroom_name, event
        )
        return HttpResponse()