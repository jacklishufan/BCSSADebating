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
    return render(request, 'tabletest.html', {'table': table,'nav':'ballot'})

def peoplePublic(request):
    if 'sort' in request.GET:
        sort = request.GET['sort']
        table = UserTablePublic(User.objects.all(),order_by=(sort, ))
    else:
        table = UserTablePublic(User.objects.all())
    return render(request, 'tabletest.html', {'table': table, 'nav': 'ballot'})

def root_main(request):
    return render(request, 'main.html', {'motionlist':Round.objects.all()})

class PersonListView(SingleTableView):
    model = Speaker
    table_class = SpeakerTable
    template_name = 'tabletest.html'

def getPersonTable(request):
    sort = 'name'
    if 'sort' in request.GET:
        sort = request.GET['sort']
        print(sort)
    for s in Speaker.objects.all():
        s.avg = s.get_avg
        s.save()
    table = SpeakerTable(Speaker.objects.all(),order_by=(sort, ))
    return render(request, 'tabletest.html', {'table': table, 'nav': 'speakers'})


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

def BallotView(request,round_num = 1):
    try:
        this_round = Round.objects.get(round_id = round_num)
        obj_set = this_round.speakers
    except:
        obj_set = Speaker.objects
        this_round = Round()

    this_form = forms.formset_factory(BallotForm,extra=10)
    this_form = this_form()
    round_total = range(1,1+len(Round.objects.all()))
    for form in this_form:
        form.set_entries(obj_set)
    print("REQUESTING")
   # print(request.POST)
    return render(request,'formbasic.html',{'formset': this_form,
                                            'nav':'home',
                                            'round_id':round_num,
                                            'round_name':this_round.name,
                                            'round_total':round_total})

def user_exist(thisname):
    if User.objects.filter(name=thisname).exists():
        return True
    return False
def submit_ballot(request):
    print("REQUESTING")
    print(request.POST['name'])

    try:
        round_num = request.POST['round_id']
    except:
        round_num = "default"

    usr_name = request.POST['name']+'_round{}'.format(round_num)

    if user_exist(usr_name) or not request.POST['name']:
        return render(request,'redirect.html',{"msg":"User Has Submitted,Please Contact Admin",
                                               'target':'/poll'})
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


    return render(request,'redirect.html',{'msg':"Submission Successful",
                                                 'target':'/poll'})
    return HttpResponse("Hello Word")

def del_user(request,userid):

    this_user = User.objects.filter(id=userid)
    if not this_user.exists():
        return HttpResponse("ERROR")
    this_user=this_user[0]
    this_user.clear_vote()
    this_user.delete()
    return render(request,'redirect.html',{'target':'/users'})

def getRuby(request):

    return render(request,'ruby.html',{'nav':'rubic',
                                           })