from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView

menu = {'change_oil': 'Change oil',
        'inflate_tires': 'Inflate tires',
        'diagnostic': 'Get diagnostic test'}

class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html',
                      context={'operations': menu})


class OperationView(TemplateView):
    template_name = 'tickets/operation.html'

    def get_context_data(self, **kwargs):
        operation = kwargs['operation']

        if operation not in menu:
            pass

        context = super().get_context_data(**kwargs)
        context['operation'] = operation
        context['title'] = menu[operation]
        return context