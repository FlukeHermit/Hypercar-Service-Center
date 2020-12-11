from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView

operations = {
                 'change_oil': {
                     'name': 'Change oil',
                     'minutes_for_operation': 2,
                 },
                 'inflate_tires': {
                     'name': 'Inflate tires',
                     'minutes_for_operation': 5,
                 },
                 'diagnostic': {
                     'name': 'Get diagnostic test',
                     'minutes_for_operation': 30,
                 }
             }

class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html',
                      context={'operations': operations})


class OperationView(TemplateView):
    template_name = 'tickets/operation.html'

    queue = {}

    def get_ticket_number(self):
        count_of_elements = 0

        for x in self.queue.values():
            count_of_elements += x

        return count_of_elements + 1

    def get_time_to_wait(self, operation):
        times = {'change_oil': 0,
                 'inflate_tires': 0,
                 'diagnostic': 0}

        for x in times.keys():
            times[x] = self.queue.get(x, 0) * operations[x]['minutes_for_operation']

        times['inflate_tires'] += times['change_oil']
        times['diagnostic'] += times['inflate_tires']

        return times[operation]

    def get_context_data(self, **kwargs):
        operation = kwargs['operation']

        if operation not in operations:
            pass
        context = super().get_context_data(**kwargs)
        context['operation'] = operation
        context['title'] = operations[operation]['name']
        context['ticket_number'] = self.get_ticket_number()
        context['minutes_to_wait'] = self.get_time_to_wait(operation)

        self.queue[operation] = self.queue.get(operation, 0) + 1
        
        return context
