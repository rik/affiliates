from datetime import datetime

from django.db import models

from celery.decorators import task

from banners.models import BannerInstance

@task
def add_click(banner_instance_id):
    """Increment the click count for a banner instance."""
    now = datetime.now()
    try:
        instance = BannerInstance.objects.get(pk=banner_instance_id)
    except BannerInstance.DoesNotExist:
        return

    stats, created = instance.clickstats_set.get_or_create(
        month=now.month, year=now.year)
    stats.clicks = models.F('clicks') + 1
    stats.save()

    instance.clicks = models.F('clicks') + 1
    instance.save()


@task
def old_add_click(user_id, banner_id, banner_img_id):
    """Increment the click counter for an existing banner instance."""
    now = datetime.now()

    try:
        instance = BannerInstance.objects.get(user_id=user_id,
                                              badge_id=banner_id,
                                              image_id=banner_img_id)
    except BannerInstance.DoesNotExist:
        # Because this type of link is depreciated, we do not create new
        # banner instances with it.
        return

    stats, created = instance.clickstats_set.get_or_create(month=now.month,
                                                           year=now.year)
    stats.clicks = models.F('clicks') + 1
    stats.save()

    instance.clicks = models.F('clicks') + 1
    instance.save()
