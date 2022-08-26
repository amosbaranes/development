from django.shortcuts import get_object_or_404
from ..courses.models import GeneralLedger, ChartOfAccounts
from .utils import get_number, add_years_months_days
from .sql import SQL


class AccountingObj(object):
    def __init__(self):
        pass

    def update_trial_balance(self):
        pass

