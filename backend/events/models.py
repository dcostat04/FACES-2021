from django.db import models
# from django_markdown.models import MarkdownField
from martor.models import MartorField
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4

class Event(models.Model):

  DAYS = (
    (1, "One"),
    (2, "Two"),
    (3, "Three")
  )
  CATEGORIES = (
    ("C","Cultural"),
    ("S", "Sports"),
  )

  event_code = models.CharField(_("Event Code"),max_length=36,default=uuid4, unique=True, primary_key=True)
  day = models.SmallIntegerField(_("Day"), choices=DAYS, blank=False)
  start = models.TimeField(_("Start Time"), max_length=5, blank=False)
  end = models.TimeField(_("End Time"), max_length=5, blank=False)
  title = models.CharField(_("Event Title"), max_length=256,blank=False)
  description = MartorField(_("Event Description"), blank=False)
  # description = models.TextField(_("Event Description"), blank=False)
  image = models.ImageField(_("Event Banner"), upload_to="uploads/")
  seats = models.IntegerField(_("Event Seats"),blank=False,default=0)
  max_seats = models.IntegerField(_("Maximum Event Seats"),blank=False,default=0)
  category = models.CharField(_("Category"), choices=CATEGORIES, max_length=1, blank=False)
  is_seminar = models.BooleanField(_("Is Event a Seminar"), default=False, blank=False)
  team_size = models.IntegerField(_("Team Size"), default=1)
  is_team_size_strict = models.BooleanField(_("Is Team Size Strict"), blank=False)
  entry_fee = models.IntegerField(_("Entry Fee"), blank=False)
  prize_money = models.TextField(_("Prize Money JSON"))
  

  def __str__(self) -> str:
    return f"{self.title}#{self.event_code}"

