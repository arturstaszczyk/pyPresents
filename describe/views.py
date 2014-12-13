from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import random
from describe.models import RandomizationModel
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from describe.forms import *
from django.core.exceptions import ObjectDoesNotExist

def getUserName(user):
    return user.first_name + " " + user.last_name

@login_required()
def user_page(request):

    try:
        person = PersonModel.objects.get(user_id=request.user.pk)
    except ObjectDoesNotExist:
        person = None

    msg = ""
    form = PersonForm(request.POST or None, instance=person)
    if request.method == "POST" and form.is_valid():
        person = form.save(commit=False)
        person.user_id = request.user
        person.save()
        msg = "Zapisano twój wymarzony prezent."

    giving_user_name = ""
    giving_user_present = ""
    try:
        giving_user_pk = RandomizationModel.objects.get(user_id=request.user.pk).giving
        giving_user = User.objects.get(pk=giving_user_pk)
        giving_user_name = getUserName(giving_user)
        #giving_person = PersonModel.objects.get(user_id=giving_user_pk)
        #giving_user_present = giving_person.present_description
    except:
        pass


    return render(request, 'describe/main_page.html', {'form': form,
                                                       'user': getUserName(request.user),
                                                       'user_pk': request.user.pk,
                                                       'message': msg,
                                                       'is_authorized': request.user.is_authenticated(),
                                                       'giving_user': giving_user_name,
                                                       'giving_user_present': giving_user_present})

def getRandomUserNot(user_pk):
    all_users = list(User.objects.all())
    all_users_count = len(all_users)
    rand = random.randint(0, all_users_count - 1)
    rand_user_pk = all_users[rand].pk

    if user_pk != rand_user_pk:
        return rand_user_pk

    return None

def randomize(request, user_pk):

    random.seed()
    counter = 0
    choosen_person = None
    while counter < 100 and choosen_person == None:
        counter += 1
        giving_pk = getRandomUserNot(user_pk)

        can_give = True
        for model in RandomizationModel.objects.all():
            if(model.giving == giving_pk):
                can_give = False

        if can_give:
            choosen_person = User.objects.get(pk=giving_pk)

    if choosen_person:
        randModel = RandomizationModel()
        randModel.user_id = user_pk
        randModel.giving = choosen_person.pk
        randModel.save()

    return redirect('describe.views.user_page')

def logout_user(request):
    logout(request)
    return redirect('/');