from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth.models import User


class Event(models.Model):
    date = models.DateField('date')
    title = models.CharField(max_length=50)
    description = models.TextField('description')
    color = models.TextField('color')
    start_time = models.TimeField('start_time')
    end_time = models.TimeField('end_time')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Scheduling"
        verbose_name_plural = "Scheduling"
        

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end):    #overlaps partially or inside of it
            overlap = True
        elif new_start <= fixed_end and new_end >= fixed_end:
            overlap = True

        return overlap

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError('<div class="info">종료시간은 시작시간보다 나중이어야 합니다.</div>')

        events = Event.objects.filter(date=self.date)
        if events.exists():
            for event in events:
                if self.check_overlap(event.start_time, event.end_time, self.start_time, self.end_time):
                    raise ValidationError(
                        '<div class="info">다른 이벤트와 시간대가 겹칩니다 : <br><strong>' + str(event.title) + "</strong><br>" + str(event.date) + ', ' + str(event.start_time) + '-' + str(event.end_time) + "</div>")
