import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
import re
from .models import Action, ActionCategory, ActionSubCategory
from ..courses.models import SubSection


def create_action(user, verb, target=None):
    # check for any similar action made in the last minute
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id, verb= verb, created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(content_type=target_ct, object_id=target.id)
    if not similar_actions:
        # no existing actions found
        category = 'general'
        sub_category = 'general'
        objsc = None
        # print(verb)
        if '__' in verb:
            ll = verb.split("__")
            category = ll[0]
            sub_category = ll[1]
            verb = ll[2]
            # print(category, sub_category, verb)
            objc, created = ActionCategory.objects.get_or_create(name=category)
            objsc, created = ActionSubCategory.objects.get_or_create(name=sub_category, category=objc)
        action = Action(user=user, verb=verb, target=target, sub_category=objsc)
        action.save()
        return True
    return False


def get_data():
    # Action.objects.get(
    #     Q(question__startswith='Who'),
    #     Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)).distinct().values('first_name', 'last_name')
    # )
    return Action.objects.all().values('verb').distinct()

