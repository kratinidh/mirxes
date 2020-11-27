from .models import Ticket, Ticket_Comments
from .decorators import allowed_users, redirect_users
from Profile.models import Profile

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User, Group
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

@login_required(login_url='login')
@redirect_users
@allowed_users(allowed_roles=['Employee', 'Manager'])
def User_Ticketing(request):
    user_profile = Profile.objects.get(user = request.user)
    Ticket_database = Ticket.objects.filter(created_by = user_profile)

    context={
        'ticketing_list' : Ticket_database
    }

    return render(request, 'Ticketing/HuNetM_ViewTicketing.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['HR', 'HR manager'])
def HR_Ticketing(request):
    Ticket_database = Ticket.objects.all()

    context={
        'ticketing_list' : Ticket_database
    }

    return render(request, 'Ticketing/HuNetHR_ViewTicketing.html', context)

class Create_Ticketing(CreateView):
    model = Ticket
    fields = ['category', 'title', 'description', 'status']
    template_name = 'Ticketing/HuNet_CreateTicketing.html'
    success_url = reverse_lazy('Ticketing:User_Ticket')

    def form_valid(self, form):
        form.instance.created_by = self.request.user.profile
        print(form.cleaned_data)
        return super(Create_Ticketing, self).form_valid(form)

class Create_Comments(CreateView):
    model = Ticket_Comments
    fields = ['ticket', 'comment']  
    template_name = 'Ticketing/HuNet_CreateComments.html'
    success_url = reverse_lazy('Ticketing:User_Ticket')

    def form_valid(self, form):
        form.instance.user = self.request.user.profile
        print(form.cleaned_data)
        return super(Create_Comments, self).form_valid(form)

class Update_Ticketing(UpdateView):
    model = Ticket
    fields=['category', 'title', 'description', 'attachments', 'status']
    template_name = 'Ticketing/HuNet_CreateTicketing.html'
    success_url = reverse_lazy('Ticketing:User_Ticket')
    
    def form_valid(self, form):
        print(form.cleaned_data)
        return super(Update_Ticketing, self).form_valid(form)

class Update_Comments(UpdateView):
    model = Ticket_Comments
    fields = ['ticket', 'comment']
    template_name = 'Ticketing/HuNet_CreateComments.html'
    success_url = reverse_lazy('Ticketing:User_Ticket')

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(Update_Comments, self).form_valid(form)

class Detail_Ticket(DetailView):
    template_name = 'Ticketing/HuNet_DetailTicket.html'
    queryset = Ticket.objects.all()

    def get_object(self):
        if self.request.user.is_authenticated:
            id = self.kwargs.get("pk")
            return Ticket.objects.get(id=id)
        
        else:
            return Ticket.objects.none()

class Delete_Comments(DeleteView):
    template_name='Ticketing/HuNet_DeleteComments.html'
    success_url = reverse_lazy('Ticketing:User_Ticket')

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Ticket_Comments, id=id)
    
class Delete_Ticket(DeleteView):
    template_name='Ticketing/HuNet_DeleteTicket.html'
    success_url = reverse_lazy('Ticketing:User_Ticket')

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Ticket, id=id)
