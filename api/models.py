from django.db import models

class Event(models.Model):
    event = models.CharField(max_length=200)
    description = models.TextField() # soon rtf field
    formLink = models.TextField(blank=True, null=True)
    contactNumber = models.CharField(max_length=13) # +91XXXXXXXXXX 
    contactEmail = models.EmailField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event

    class Meta:
        db_table = 'event'
        managed = True
        verbose_name = 'Event'
        verbose_name_plural = 'Events'


class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="allRegistrations")
    userName = models.CharField(max_length=200)
    userNumber = models.CharField(max_length=13)
    userEmail = models.EmailField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.userName

    class Meta:
        db_table = 'registration'
        managed = True
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'


def uploadTimelineImg(instance, filename):
    ext = filename.split(".")[1]
    filename = instance.tag +"."+ext
    # file will be uploaded to MEDIA_ROOT/<int:event_id>/answers/<str:filename>
    return '{0}/answers/{1}'.format(instance.event.id, filename)


class Timeline(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="timeline")
    tag = models.CharField(max_length=200)
    fromtimestamp = models.DateTimeField()
    totimestamp = models.DateTimeField()
    desc = models.TextField()
    image = models.FileField(upload_to=uploadTimelineImg, blank=True, null=True)

    def __str__(self):
        return self.tag

    class Meta:
        db_table = 'timeline'
        managed = True
        verbose_name = 'Timeline'
        verbose_name_plural = 'Timelines'
    
def uploadPrizeImg(instance, filename):
    ext = filename.split(".")[1]
    filename = "prize" + instance.rankRange + "." + ext
    # file will be uploaded to MEDIA_ROOT/<int:event_id>/prize/<str:filename>
    return '{0}/prize/{1}'.format(instance.event.id, filename)

class Prize(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="prizes")
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


