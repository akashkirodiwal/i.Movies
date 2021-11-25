from django.db import models
from django.contrib.auth.models import User
from movies.models import Screening


# Create your models here.

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    no_of_seats=models.IntegerField(default=0)
    cost=models.IntegerField(default=0)

    def __str__(self):
        return self.screening.theatre_id.name + ' - ' + self.screening.hall_name + ' - ' +str(self.screening.price) + ' - '+ str(self.no_of_seats)
