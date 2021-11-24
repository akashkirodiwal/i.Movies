from django.db import models
from django.contrib.auth.models import User
from movies.models import Screening


# Create your models here.

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)

    def __str__(self):
        return self.screening.theatre_id.name + ' - ' + self.screening.hall_name
