from django.http import HttpResponse
from qipashuo.models import *
from django.views.generic.edit import FormView
from django import forms
from django_tables2 import tables, SingleTableView
from qipashuo.forms import *
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello Word")

from .models import Speaker
from .tables import SpeakerTable,UserTable,UserTablePublic

def people(request):
    table = UserTable(User.objects.all())
    return render(request, 'tabletest.html', {'table': table})

def peoplePublic(request):
    table = UserTablePublic(User.objects.all())
    return render(request, 'tabletest.html', {'table': table})

class PersonListView(SingleTableView):
    model = Speaker
    table_class = SpeakerTable
    template_name = 'tabletest.html'

def getPersonTable(request):
    for s in Speaker.objects.all():
        s.avg = s.get_avg
        s.save()
    return PersonListView.as_view()(request)


class UserView(SingleTableView):
    model = User
    table_class = UserTable
    template_name = 'tabletest.html'

class UserViewPublic(SingleTableView):
    model = User
    table_class = UserTablePublic
    template_name = 'tabletest.html'
# class PersonListView(tables.Table):
#     name = tables.Column()

# def get_speaker_table(request):

# class BallotView(FormView):
#     form_class = forms.formset_factory(BallotForm,extra=10)
#     template_name = 'formbasic.html'
#     success_url = ''

def BallotView(request):
    form = forms.formset_factory(BallotForm,extra=10)
    form = form()
    print("REQUESTING")
   # print(request.POST)
    return render(request,'formbasic.html',{'formset': form})

def user_exist(thisname):
    if User.objects.filter(name=thisname).exists():
        return True
    return False
def submit_ballot(request):
    print("REQUESTING")
    print(request.POST['name'])
    usr_name = request.POST['name']
    if user_exist(usr_name):
        return render(request,'redirect.html',{"msg":"User Has Submitted,Please Contact Admin"})
    print(request.POST)
    this_usr = User()
    this_usr.name = usr_name
    this_usr.save()
    form_set = forms.formset_factory(BallotForm)
    form_set = form_set(request.POST)
    new_ballot = Ballot()
    new_ballot.voter = this_usr
    new_ballot.save()
    if form_set.is_valid():
        for form in form_set:
            speaker = form.cleaned_data.get('speaker_name')
            score = form.cleaned_data.get('speaker_score')

            if speaker and score:
                print(speaker,score)
                new_scoring = Scoring()
                new_scoring.scored_speaker = speaker
                new_scoring.score = score
                new_scoring.save()
                new_ballot.scorings.add(new_scoring)
                #new_ballot.save()
    new_ballot.save()
    #new_ballot.save()


    return render(request,'redirect.html',{})
    return HttpResponse("Hello Word")

def del_user(request,userid):

    this_user = User.objects.filter(id=userid)
    if not this_user.exists():
        return HttpResponse("ERROR")
    this_user=this_user[0]
    this_user.clear_vote()
    this_user.delete()
    return render(request,'redirect.html',{})