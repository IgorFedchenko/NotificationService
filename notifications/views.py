from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def main(request):
    pass

def registration(request):
    pass

@login_required()
def account(request):
    pass

@login_required()
def create_app(request):
    pass

@login_required()
def create_app_key(request):
    pass

@login_required()
def create_theme(request):
    pass

@login_required()
def app_details(request, pk):
    pass

@login_required()
def theme_details(request, pk):
    pass

@login_required()
def message_details(request, pk):
    pass

