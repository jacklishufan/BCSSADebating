from django.db import models

class User(models.Model):
    ip = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now=True)
    @property
    def has_voted(self):
        ballots = [i for i in self.ballot_set.all()]
        return bool(ballots)
    def clear_vote(self):
        ballots = [i for i in self.ballot_set.all()]
        for ballot in ballots:
            for score in ballot.scorings.all():
                score.delete()
            ballot.delete()


class Speaker(models.Model):
    name = models.CharField(max_length=200)
    avg = models.FloatField(default=0)
    def __str__(self):
        return self.name

    @property
    def get_avg(self):
        score_list = [i for i in self.scoring_set.all()]
        if len(score_list) ==0:
            return 0
        return sum([i.score for i in score_list])/len(score_list)

class Round(models.Model):
    round_id = models.IntegerField(default=0)
    name = models.CharField(max_length=200,default="")
    speakers = models.ManyToManyField(Speaker)

class Scoring(models.Model):
    scored_speaker = models.ForeignKey(Speaker,on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    def __str__(self):
        return str(self.scored_speaker)+":"+str(self.score)

class Ballot(models.Model):
    voter = models.ForeignKey(User,on_delete=models.CASCADE)
    scorings = models.ManyToManyField(Scoring)
    def __str__(self):
        return str([str(i) for i in self.scorings.all()])

class FinalSpeaker(models.Model):
    name = models.CharField(max_length=20)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class FinalVoter(models.Model):
    ip = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now=True)
    voted_team = models.CharField(max_length=20)
    best_speaker = models.ForeignKey(FinalSpeaker, on_delete=models.CASCADE)


class GrandFinal(models.Model):
    gov_vote = models.IntegerField(default=0)
    opp_vote = models.IntegerField(default=1)

    @property
    def global_sum(self):
        return self.gov_vote+self.opp_vote
    @property
    def gov_percentage(self):
        sum = self.gov_vote+self.opp_vote
        if not sum:
            return "50%"
        return str(round(self.gov_vote/sum*100))+"%"

    @property
    def opp_percentage(self):
        sum = self.gov_vote + self.opp_vote
        if not sum:
            return "50%"
        return str(round(self.opp_vote / sum * 100)) + "%"


