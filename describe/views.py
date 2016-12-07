import random
from django.shortcuts import render, redirect

from describe.controllers.display_controller import DisplayController
from describe.models import RandomizationModel
from describe.persons_controller import PersonsController
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from describe.forms import *
from describe.exceptions import CannotFindReceiver


@login_required()
def user_page(request):
    ui_message = ""
    persons = PersonsController()

    person = persons.get_person(request.user)
    form = PersonForm(request.POST or None, instance=person)
    if _save_person_form_changes(request, form):
        ui_message = "Zamówienie przyjęte. Prezent w trakcie pakowania..."

    display_controller = DisplayController()
    giving_user_data = _get_receiver_data(request.user)
    template_data = {'form': form,
                     'user_name': person.get_user_name(),
                     'user_pk': person.user_id.pk,
                     'ui_message': ui_message,
                     'is_authorized': request.user.is_authenticated(),
                     'display_edit_field': display_controller.can_user_describe_present()}
    template_data = dict(list(template_data.items()) + list(giving_user_data.items()))

    return render(request, 'describe/main_page.html', template_data)


def _save_person_form_changes(request, form):
    saved = False

    present = form.instance.present_description
    if form.is_valid() or (present != None and len(present) > 0):
        saved = True
        if form.is_valid() and request.method == "POST":
            person_instance = form.save(commit=False)
            person_instance.user_id = request.user
            person_instance.save()


    return saved

def _get_receiver_data(user):
    receiver_name = ""
    receiver_wanted_present = ""
    try:
        receiver_pk = RandomizationModel.objects.get(user_id=user.pk).giving_id
        receiver = PersonModel.objects.get(user_id=receiver_pk)

        receiver_name = receiver.get_user_name()
        receiver_wanted_present = receiver.present_desc
    except:
        try:
            receiver_pk = RandomizationModel.objects.get(user_id=user.pk).giving_id
            receiver = User.objects.get(pk=receiver_pk)

            receiver_name = PersonModel.get_user_name_static(receiver)
        except:
            pass

    return {'receiver_name': receiver_name,
            'receiver_wanted_present': receiver_wanted_present}

@login_required()
def randomize(request, user_pk):

    random.seed()

    persons = PersonsController()

    try:
        persons.draw(User.objects.get(pk=user_pk))
    except CannotFindReceiver:
        pass

    return redirect('user-page')

#*---------------------------------------------------------------*#
def logout_user(request):
    logout(request)
    return redirect('user-page')