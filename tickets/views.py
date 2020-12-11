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
    length = {'change_oil': 0,
              'inflate_tires': 0,
              'diagnostic': 0}

    def get_ticket_number(self, operation):
        count_of_elements = 0

        for x in self.queue.values():
            count_of_elements += x

        self.length[operation] += 1
        return count_of_elements + 1

    def get_time_to_wait(self, operation):
        times = {'change_oil': 0,
                 'inflate_tires': 0,
                 'diagnostic': 0}

        for x in times.keys():
            times[x] = self.queue.get(
                x, 0) * operations[x]['minutes_for_operation']

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
        context['ticket_number'] = self.get_ticket_number(operation)
        context['minutes_to_wait'] = self.get_time_to_wait(operation)

        self.queue[operation] = self.queue.get(operation, 0) + 1

        return context


class ProcessingView(TemplateView):

    template_name = "tickets/processing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['lines'] = {'Change oil': OperationView.length['change_oil'],
                            'Inflate tires': OperationView.length['inflate_tires'],
                            'Get diagnostic': OperationView.length['diagnostic']}
        return context
