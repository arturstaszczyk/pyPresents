from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from describe.forms import *
from django.http import HttpResponse

# Create your views here.
@login_required()
def main_page(request):

    form = PersonForm()
    return render(request, 'describe/test.html', {'form': form})