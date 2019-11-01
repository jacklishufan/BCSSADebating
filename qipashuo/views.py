from django.http import HttpResponse
from qipashuo.models import *
from django.views.generic.edit import FormView
from django import forms
from django_tables2 import tables, SingleTableView
from qipashuo.forms import *
from django.shortcuts import render
from os import environ as env
def index(request):
    return HttpResponse("Hello Word")

from .models import Speaker
from .tables import SpeakerTable,UserTable,UserTablePublic,FinalSpeakerTable

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

    this_form = forms.formset_factory(BallotForm,extra=30)
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
def grandFinal(request):
    if env['STAGE']=='FIRST_VOTE':
        return grandFinalvote(request)
    if env['STAGE']=='FIRST_VOTE_CLOSED':
        return grandFinalvote(request,'closed')
    elif env['STAGE'] == 'SECOND_VOTE':
        return grandFinalvote2(request)
    elif env['STAGE'] == 'SECOND_VOTE_CLOSED':
        return grandFinalvote2(request,'closed')
    else:
        return resultShow(request,'false')


def grandFinalvote(request,done='done'):
    gf = GrandFinal.objects.get(name='old')
    usrip = getUserIP(request)
    if FinalVoter.objects.filter(ip = usrip, type = "INIT").exists() or done =='closed':
        return render(request, 'grandfinal.html', {'nav': 'rubic',
                                               'forms': 'false',
                                               'gf': gf,
                                               'first_vote':done
                                               })
    return render(request, 'grandfinal.html', {'nav': 'rubic',
                                               'forms': 'false',
                                               'gf': gf,
                                               'first_vote':'true'
                                               })
def grandFinalvote2(request,done='done'):

    gf = GrandFinal.objects.get(name='old')
    gf2 = GrandFinal.objects.get(name='new')
    new_form = FinalBallotForm()
    usrip = getUserIP(request)
    if FinalVoter.objects.filter(ip=usrip, type="FINAL").exists() or done == 'closed':
        return render(request, 'grandfinal.html', {'nav': 'rubic',
                                                   'forms': new_form,
                                                   'gf': gf,
                                                   'gf2': gf2,
                                                   'stage2': 'true',
                                                   'first_vote': 'closed',
                                                   '2nd_vote': done
                                                   })
    return render(request,'grandfinal.html',{'nav':'rubic',
                                             'forms':new_form,
                                             'gf':gf,
                                             'gf2':gf2,
                                             'stage2':'true',
                                             'first_vote': 'closed',
                                             '2nd_vote': 'true'
                                           })
def resultShow(request,update='false'):
    sft = 'false'
    if env['UPDATE']== 'true' :
        update = 'true'
    if env['STAGE'] not in ['FIRST_VOTE','FIRST_VOTE_CLOSED'] :
        sft = 'true'
    gf = GrandFinal.objects.get(name='old')
    new_form = FinalBallotForm()
    gf2 = GrandFinal.objects.get(name='new')
    return render(request,'grandfinal.html',{'nav':'rubic',
                                             'forms':new_form,
                                             'gf':gf,
                                             'gf2':gf2,
                                             'stage2': sft,
                                             'update':update
                                           })
def getUserIP(request):
    # 获取客户端IP
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META['HTTP_X_FORWARDED_FOR']
    else:
        return request.META['REMOTE_ADDR']

def submit_ballot_GF(request):
    print("REQUESTING")
    gf = GrandFinal.objects.get(name='new')
    usrip = getUserIP(request)
    print(usrip)
    if FinalVoter.objects.filter(ip=usrip,type="FINAL").exists():
        return render(request,'redirect.html',{"msg":"User Has Submitted,Please Contact Admin",
                                               'target':'/gf'})
    print(request.POST)
    this_usr = FinalVoter()
    this_usr.ip = usrip
    this_usr.type = "FINAL"
   # this_usr.save()
    print("DEBUG CHECKPOINT A")
    rep_form = FinalBallotForm(request.POST)

    if rep_form.is_valid():
        best_speaker = rep_form.cleaned_data.get('best_speaker')
        winner = rep_form.cleaned_data.get('winner')
        print(rep_form)
        if winner == 'AFF':
            gf.gov_vote = gf.gov_vote+1
            gf.save()
        elif winner == 'NEG':
            gf.opp_vote = gf.opp_vote+1
            gf.save()
        best_speaker.votes = best_speaker.votes+1
        best_speaker.save()
        this_usr.save()
    else:
        print("FAIL",rep_form.errors)

    return render(request,'redirect.html',{'msg':"Submission Successful",
                                                  'target':'/gf'})
    # return HttpResponse("Hello Word")
    #return grandFinal(request)
def getSpeakerRankTable(request):
    sort = 'votes'
    if 'sort' in request.GET:
        sort = request.GET['sort']
        print(sort)
    table = FinalSpeakerTable(FinalSpeaker.objects.all(),order_by=(sort, ))
    return render(request, 'tabletest.html', {'table': table, 'update': 'true'})

def submit_ballot_init(request):
    choice = request.POST['vote']
    gf = GrandFinal.objects.get(name="old")
    this_usr = FinalVoter()
    this_usr.ip = getUserIP(request)
    this_usr.type = "INIT"
    this_usr.save()
    if choice == "AFF":
        gf.gov_vote = gf.gov_vote +1
    if choice == "NEG":
        gf.opp_vote = gf.opp_vote +1
    gf.save()
    print(choice)
    return render(request,'redirect.html',{'msg':"Submission Successful",
                                                  'target':'/gf'})
def clearAllUser(request):
    for i in FinalVoter.objects.all():
        i.delete()
    return render(request,'redirect.html',{'msg':"Deletion Successful",
                                                  'target':'/gf'})