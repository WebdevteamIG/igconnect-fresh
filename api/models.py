from datetime import timedelta
from re import T
from time import time
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete

from datetime import datetime, timedelta
from django.utils import timezone 

class Event(models.Model):
    event = models.CharField(max_length=200)
    description = models.TextField()
    formLink = models.TextField(blank=True, null=True)
    contactNumber = models.CharField(max_length=13) # +91XXXXXXXXXX 
    contactEmail = models.EmailField(blank=True, null=True)
    eligiblity = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    incentives = models.TextField(blank=True, null=True)

    @staticmethod
    def getAccToDate(date):
        filterDic = {}
        if date == "eq":
            filterVar = "fromtimestamp__contains"
            filterDic[filterVar] = timezone.now().date()
        else:
            filterVar = "fromtimestamp__" + date
            time = timezone.now().time()
            filterDic[filterVar] = timezone.now() - timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)

        events = Event.objects.all()
        _events = []
        for event in events:
            timelines = event.timeline.filter(**filterDic)
            if(len(timelines) > 0):
                _events.append(event)

        # for event in events:
        #     timelines = event.timeline.objects.filter(**filterDic)
        return _events

    def __str__(self):
        return self.event

    class Meta:
        db_table = 'event'
        managed = True
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

def uploadEventMedia(instance, filename):
    ext = filename.split(".")[1]
    filename = instance.type +"."+ext
    # file will be uploaded to MEDIA_ROOT/<int:event_id>/answers/<str:filename>
    return 'event_{0}/media/{1}'.format(instance.event.id, filename)



class EventMedia(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="mediafiles")
    type = models.CharField(max_length=20)
    file = models.FileField(upload_to=uploadEventMedia)
    desc = models.TextField()

    def __str__(self) -> str:
        return "event" + self.event.id + "_" + self.type

    class Meta:
        db_table = 'eventmedia'
        managed = True
        verbose_name = 'EventMedium'
        verbose_name_plural = 'EventMedia'


class Team(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='teams')
    teamname = models.CharField(max_length=200)
    leader = models.CharField(max_length=10)

    def __str__(self):
        return self.teamname
    
    class Meta:
        db_table = 'team'
        managed = True
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'


def uploadTimelineImg(instance, filename):
    ext = filename.split(".")[-1]
    filename = instance.tag +"."+ext
    # file will be uploaded to MEDIA_ROOT/<int:event_id>/answers/<str:filename>
    return 'event_{0}/timeline/{1}'.format(instance.event.id, filename)


class Timeline(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="timeline")
    tag = models.CharField(max_length=200)
    fromtimestamp = models.DateTimeField()
    totimestamp = models.DateTimeField()
    desc = models.TextField()
    image = models.FileField(upload_to=uploadTimelineImg, blank=True, null=True)
    topics = models.TextField(blank=True, null=True)
    allowSubmission = models.BooleanField(default=False)

    def __str__(self):
        return self.tag

    class Meta:
        db_table = 'timeline'
        managed = True
        verbose_name = 'Timeline'
        verbose_name_plural = 'Timelines'
    

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="allRegistrations")
    userName = models.CharField(max_length=200)
    userNumber = models.CharField(max_length=10)
    userEmail = models.EmailField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team", blank=True, null=True)

    def __str__(self):
        return self.userName

    def save(self, *args, **kwargs):
        self.userNumber = self.userNumber[-10:]
        super(Registration, self).save(*args, **kwargs)

    class Meta:
        db_table = 'registration'
        managed = True
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'


class TimelineRegistration(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name="timelineregistration")
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE, related_name='registrations')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}_{}".format(self.registration.userName, self.timeline.tag)

    class Meta:
        db_table = 'timelinereg'
        managed = True
        verbose_name = 'TimelineRegistration'
        verbose_name_plural = 'TimelineRegistrations'
    


class Submission(models.Model):
    event = models.ForeignKey(Timeline, on_delete=models.CASCADE, related_name="allSubmissions")
    user = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='submissions')
    type = models.CharField(max_length=20, null=True, blank=True)
    desc = models.TextField()

    def __str__(self):
        return "{}_submission".format(self.type)

    class Meta:
        db_table = 'submission'
        managed = True
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'



def uploadPrizeImg(instance, filename):
    ext = filename.split(".")[-1]
    filename = "prize" + instance.rankRange + "." + ext
    # file will be uploaded to MEDIA_ROOT/<int:event_id>/prize/<str:filename>
    return 'event_{0}/prize/{1}'.format(instance.event.id, filename)

class Prize(models.Model):
    event = models.ForeignKey(Timeline, on_delete=models.CASCADE, related_name="prizes")
    rank = models.IntegerField(default=-1)
    rankRange = models.CharField(max_length=8)
    desc = models.TextField()
    image = models.FileField(upload_to=uploadPrizeImg, null=True, blank=True)

    def __str__(self):
        return "prize"

    class Meta:
        db_table = 'prize'
        managed = True
        verbose_name = 'Prize'
        verbose_name_plural = 'Prizes'


# Post delete hooks
@receiver(post_delete, sender=Timeline)
def postDeleteTimeline(sender, instance, **kwargs):
    instance.image.delete(False)

@receiver(post_delete, sender=Prize)
def postDeletePrize(sender, instance, **kwargs):
    instance.image.delete(False)

@receiver(post_delete, sender=EventMedia)
def postDeletePrize(sender, instance, **kwargs):
    instance.file.delete(False)