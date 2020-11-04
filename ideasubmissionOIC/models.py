from django.db import models

class OICSubmissions(models.Model):
    teamName = models.CharField(max_length=100)
    leaderName = models.CharField(max_length=100)
    user = models.EmailField(unique=True)
    desc = models.TextField()

    def __str__(self):
        return "{}_submission".format(self.teamName)

    class Meta:
        db_table = 'oicsubmission'
        managed = True
        verbose_name = 'OICSubmission'
        verbose_name_plural = 'OICSubmissions'

