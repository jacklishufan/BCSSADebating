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
        return sum([i.score for i in score_list])/len(score_list)

class Round(models.Model):
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




