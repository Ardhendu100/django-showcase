from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q
import datetime
from django.utils import timezone


@login_required
def chat_room(request, room_name=None):
    # If no room_name is provided, redirect to the user's own room
    if room_name is None:
        room_name = request.user.username + '(You)'  # Default to the user's username as room_name
    
    search_query = request.GET.get('search', '') 
    users = User.objects.exclude(id=request.user.id)
    
    # Fetch chats for the specific room_name
    chats = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver__username=room_name)) |
        (Q(receiver=request.user) & Q(sender__username=room_name))
    )

    if search_query:
        chats = chats.filter(Q(content__icontains=search_query))  

    chats = chats.order_by('timestamp') 
    user_last_messages = []

    for user in users:
        last_message = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) |
            (Q(receiver=request.user) & Q(sender=user))
        ).order_by('-timestamp').first()

        user_last_messages.append({
            'user': user,
            'last_message': last_message
        })

    min_time = timezone.make_aware(datetime.datetime.min)

    user_last_messages.sort(
        key=lambda x: x['last_message'].timestamp if x['last_message'] else min_time,
        reverse=True
    )

    return render(request, 'chat/chat.html', {
        'room_name': room_name,
        'chats': chats,
        'users': users,
        'user_last_messages': user_last_messages,
        'search_query': search_query 
    })
