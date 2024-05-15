from django.shortcuts import render
from app.models import Message, Account
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from  django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from app.views import MessageForm
# Create your views here.

@login_required
def messenger(request):
    user = request.user
    my_users = Message.get_thread_users(user)
    thread_user = my_users.first()
    return HttpResponseRedirect(reverse('messenger:thread', args = [thread_user.id]))
    

@login_required
def thread(request, user_id):
    user = request.user #ja
    thread_user = get_object_or_404(User, pk=user_id)# user s kojim zelimo vijet razgvor
    thread = Message.get_thread(user, thread_user) #sve poruke izmedu nas i usera s kojim smo vodili razgov
    sidebar_threads = Message.get_threads_for(user) # svi ostali useri koji trebaju biti u lijevom side baru
             
    form = MessageForm()

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = Message(
                text = form.cleaned_data['text'],
                sender = request.user,
                receiver = thread_user,
            )
            message.save()
            return HttpResponseRedirect(reverse('messenger:thread', args=[thread_user.id]))
        
   
    context={
        'sidebar_threads':sidebar_threads,
        'thread_user':thread_user,
        'thread':thread,
        'form': form,
        
    }
    return render(request, 'messenger/messenger.html', context)