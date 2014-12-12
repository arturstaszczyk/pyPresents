from django.shortcuts import render, redirect, get_object_or_404
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

    return render(request, 'describe/main_page.html', {'form': form,
                                                       'user': getUserName(request.user),
                                                       'message': msg })

def logout_user(request):
    logout(request)
    return redirect('/');