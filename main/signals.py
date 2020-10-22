from django.db.models.signals import post_save
from django.dispatch import receiver
from comalfa.main.models import SeriesEngineGuides

@receiver(post_save, sender = SeriesEngineGuides)
def add_score(sender, **kwargs):
    print('AFTER SAVE')