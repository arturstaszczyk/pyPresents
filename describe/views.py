from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import random
from describe.models import RandomizationModel
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from describe.forms import *
from django.core.exceptions import ObjectDoesNotExist

#*---------------------------------------------------------------*#
def _save_person_form_changes(request, form):
    saved = False
    if request.method == "POST" and form.is_valid():
        person_instance = form.save(commit=False)
        person_instance.user_id = request.user
        person_instance.save()
        saved = True

    return saved

#*---------------------------------------------------------------*#
def _get_person_model(request):
    try:
        person = PersonModel.objects.get(user_id=request.user.pk)
    except ObjectDoesNotExist:
        person = PersonModel()
        person.user_id = request.user
        person.save()

    return person

#*---------------------------------------------------------------*#
def _get_giving_data(user_pk):
    giving_user_name = ""
    giving_user_present = ""
    try:
        giving_user_pk = RandomizationModel.objects.get(user_id=user_pk).giving
        giving_person = PersonModel.objects.get(user_id=giving_user_pk)
        giving_user_name = giving_person.get_user_name()
        giving_user_present = giving_person.present_desc
    except:
        try:
            giving_user_pk = RandomizationModel.objects.get(user_id=user_pk).giving
            giving_user = User.objects.get(pk=giving_user_pk)
            giving_user_name = PersonModel.get_user_name_static(giving_user)
        except:
            pass

    return {'giving_user_name': giving_user_name,
            'giving_user_present': giving_user_present}

#*---------------------------------------------------------------*#
@login_required()
def user_page(request):
    ui_message = ""

    person = _get_person_model(request)
    form = PersonForm(request.POST or None, instance=person)
    if _save_person_form_changes(request, form):
        ui_message = "Aniołek przyjął zamówienie. Prezent w trakcie pakowania..."

    giving_user_data = _get_giving_data(request.user.pk)
    template_data = {'form': form,
                     'user_name': person.get_user_name(),
                     'user_pk': person.user_id.pk,
                     'ui_message': ui_message,
                     'is_authorized': request.user.is_authenticated() }
    template_data = dict(list(template_data.items()) + list(giving_user_data.items()))

    return render(request, 'describe/main_page.html', template_data)

#*---------------------------------------------------------------*#
def _get_random_user_not_me(user_pk):
    all_users = list(User.objects.all())
    all_users_count = len(all_users)
    rand = random.randint(1, all_users_count * 10000) % all_users_count
    rand_user_pk = all_users[rand].pk

    if user_pk != str(rand_user_pk):
        return rand_user_pk

    return None

#*---------------------------------------------------------------*#
def _save_randomization_between(user_pk, giving_pk):
    randModel = RandomizationModel()
    randModel.user_id = user_pk
    randModel.giving_id = giving_pk
    randModel.save()

#*---------------------------------------------------------------*#
@login_required()
def randomize(request, user_pk):

    random.seed()
    counter = 0
    can_give = False

    choosen_person = None
    while counter < 500 and choosen_person == None:
        counter += 1
        giving_pk = _get_random_user_not_me(user_pk)
        if giving_pk == None:
            continue

        giving_person = User.objects.get(pk=giving_pk)
        user = User.objects.get(pk=user_pk)
        user_groups = user.groups.values_list('name', flat=True)
        giving_group = giving_person.groups.values_list('name', flat=True)

        if giving_group[0] == user_groups[0]:
            continue

        already_taken = False
        for model in RandomizationModel.objects.all():
            if(model.giving == giving_pk):
                already_taken = True
                break

        if already_taken:
            continue

        choosen_person = User.objects.get(pk=giving_pk)

    if choosen_person:
        _save_randomization_between(user_pk, choosen_person.pk)

    return redirect('user-page')

#*---------------------------------------------------------------*#
def logout_user(request):
    logout(request)
    return redirect('user-page')