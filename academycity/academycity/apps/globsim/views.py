from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language
from django.http import JsonResponse
from django.apps import apps
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, F
from django.utils.text import slugify
from .models import FinanceType, FinanceTypeAttribute, Distributor, DistributorAttribute
import random

from ..actions.utils import create_action
# --
from .models import (Segment, Game, GameType, RandD, Period, RandD_Attribute, Product,
                     ManufacturingPeriodData, HumanResourcesPeriodData,
                     ProductPeriodDataDetail)


def home(request, obj_id):
    title = _('GlobSim App')
    game = Game.objects.filter(translations__language_code=get_language()).get(id=obj_id)
    game_types = GameType.objects.filter(translations__language_code=get_language())
    # print('-'*10)
    # print(title)
    # print(game)
    # print(game_types)
    # print('-'*10)

    return render(request, 'globsim/home.html', {'title': title,
                                                 'game': game,
                                                 'game_types': game_types
                                                 })


def get_screens_randd(request, name_, game, team_, s_url):
    # print('get_screens_randd 1000')
    # print(team_)
    # print('get_screens_randd 1000')

    randds = team_.team_rds.all()
    # print(s_url)
    # print('---')
    return render(request, s_url, {'name': name_, 'game': game, 'user': request.user,
                                   'randds': randds})


def get_screens_product(request, name_, game, team_, s_url):
    try:
        # periods = Period.objects.filter(game_id=game.id).filter(period_number__lte=game.current_period_number).all()
        products = team_.team_products.all()
        # randds = team_.team_rds.filter(randd_products__isnull=True).all()
    except Exception as e:
        print("100   " +e)
    print(s_url)
    print('---')
    return render(request, s_url, {'name': name_, 'game': game, 'user': request.user, 'products': products})


def get_screens_manufacturing(request, name_, game, team_, s_url):
    team_ = game.get_current_team(request.user)
    accounts_ = {}
    for account in team_.team_manufacturing.all()[0].manufacturing_period_data_details.all():
        # n, category, account_, amount = get_account_tuple(account)
        category = account.manufacturing_type_attribute.category
        account = account.manufacturing_type_attribute.account
        try:
            x = accounts_[category]
        except Exception as e:
            accounts_[category] = {}
        accounts_[category][account] = {}
    for manufacturing_data_ in team_.team_manufacturing.all():
        sp = manufacturing_data_.period.period
        accounts = manufacturing_data_.manufacturing_period_data_details.all()
        for account1 in accounts:
            # n, category, account_, amount = get_account_tuple(account)
            category = account1.manufacturing_type_attribute.category
            account = account1.manufacturing_type_attribute.account
            accounts_[category][account][sp] = (account1.id, account1.amount,
                                                account1.manufacturing_type_attribute.min,
                                                account1.manufacturing_type_attribute.max)
    periods = range(game.start_period, game.start_period + game.current_period_number + 1)
    return render(request, s_url, {'periods': periods, 'game': game, 'accounts': accounts_, 'user': request.user})


def get_screens_humanresources(request, name_, game, team_, s_url):
    team_ = game.get_current_team(request.user)
    accounts_ = {}
    for account in team_.team_human_resources.all()[0].human_resources_period_data_details.all():
        category = account.human_resource_type_attribute.category
        account = account.human_resource_type_attribute.account
        try:
            x = accounts_[category]
        except Exception as e:
            accounts_[category] = {}
        accounts_[category][account] = {}
    for human_resources_data_ in team_.team_human_resources.all():
        sp = human_resources_data_.period.period
        accounts = human_resources_data_.human_resources_period_data_details.all()
        for account1 in accounts:
            category = account1.human_resource_type_attribute.category
            account = account1.human_resource_type_attribute.account
            accounts_[category][account][sp] = (account1.id, account1.amount,
                                                account1.human_resource_type_attribute.min,
                                                account1.human_resource_type_attribute.max)
    periods = range(game.start_period, game.start_period + game.current_period_number + 1)
    return render(request, s_url, {'periods': periods, 'game': game, 'accounts': accounts_, 'user': request.user})


def get_screens_finance(request, name_, game, team_, s_url):
    # print('---')
    # print(s_url)
    # print('---')
    return render(request, s_url, {'name': name_, 'game': game, 'user': request.user})


def get_screens_gdistributor(request, name_, game, team_, s_url):
    # print('---')
    # print(s_url)
    # print('---')
    try:
        distributors = team_.team_g_distributors.all()
    except Exception as e:
        print("100   " +e)
    return render(request, s_url, {'name': name_, 'game': game, 'user': request.user,
                                   'distributors': distributors})


def get_screens_reports(request, name_, game, team_, s_url):
    # print(s_url)
    # print('---')
    return render(request, s_url, {'name': name_, 'game': game, 'user': request.user})


def get_screens_gamesetup(request, name_, game, team_, s_url):
    # print(s_url)
    # print('---')
    return render(request, s_url, {'name': name_, 'game': game, 'user': request.user})


def get_screens_admin(request, name_, game, team_, s_url):
    # print(s_url)
    # print('---')
    return render(request, s_url, {'name': name_, 'game': game, 'user': request.user})


def get_screens(request):
    name_ = request.POST.get('name').lower()
    # print(name_)
    obj_id = request.POST.get('obj_id')  # obj_id is the game_id
    game = Game.objects.filter(translations__language_code=get_language()).get(id=obj_id)

    team_ = game.get_current_team(request.user)

    s_url = 'globsim/_' + name_ + '.html'
    sr = "get_screens_"+name_+"(request, name_, game, team_, s_url)"
    # print(sr)
    #
    #     https://python-reference.readthedocs.io/en/latest/docs/functions/eval.html
    # >>> # this example shows how providing globals argument prevents eval from accessing real globals dictionary
    # >>> eval("os.getcwd()", {})
    # NameError: name 'os' is not defined
    # >>> # that example however can be bypassed by using __import__ function inside eval
    # >>> eval('__import__("os").getcwd()', {})
    create_action(request.user, 'globsim__get_screens__' + name_, target=game)
    return eval(sr)


def get_or_create_product(request):
    product_id = request.POST.get('product_id')
    rr = {'product_id': product_id}
    try:
        app_ = request.POST.get('app').lower()
        model_name_ = request.POST.get('model_name').lower()
        obj_id = request.POST.get('obj_id')
        obj_model = apps.get_model(app_label=app_, model_name=model_name_)
        obj_randd = obj_model.objects.get(id=obj_id)
        product_ = obj_randd.get_or_create_product()
        if product_id == -1:
            create_action(request.user, 'globsim__get_or_create_product__create_product', target=product_)
        else:
            create_action(request.user, 'globsim__get_or_create_product__view_product', target=product_)
        # print('-'*50)
        # print(product_.id)
        # print('-'*20, model_name_,'-'*20, )
    except Exception as e:
        print("200 :" + e)
    rr = {'product_id': product_.id}
    return JsonResponse(rr)


def update_abandon_product(request):
    game_id = request.POST.get('game_id')
    obj_id = request.POST.get('obj_id')
    is_abandon = request.POST.get('is_abandon')
    game = Game.objects.filter(translations__language_code=get_language()).get(id=game_id)
    print(game)
    obj = Product.objects.get(id=obj_id)
    print(obj)
    print(is_abandon)
    if int(is_abandon) == 0:
        p = game.current_period_obj
        obj.set_abundant_period(p)
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'ok'})


def get_sub_screens(request):
    # print('get_sub_screens')
    name_ = request.POST.get('name').lower()
    game_id = request.POST.get('game_id')
    game = Game.objects.filter(translations__language_code=get_language()).get(id=game_id)
    app_ = request.POST.get('app').lower()
    obj_id = request.POST.get('obj_id')
    model_name_ = request.POST.get('model_name').lower()
    obj_model = apps.get_model(app_label=app_, model_name=model_name_)
    s_url = 'globsim/_' + model_name_ + '_detail.html'
    # print(s_url)

    if model_name_ == "randd":
        segments = game.game_type.segments.filter(translations__language_code=get_language()).all()
        if obj_id == "new":
            # print("new: " + model_name_)
            period_ = game.current_period_obj
            team_ = game.get_current_team(request.user)
            s0 = game.game_type.segments.all()[0]
            try:
                obj = obj_model.objects.create(name=request.POST.get('name'), period=period_, team=team_, segment=s0,
                                               scu_per_unit=1, prime_cost_per_unit=50,
                                               project_expenditure=1000000, last_entered_by=request.user
                                               )
                create_action(request.user, 'globsim__get_sub_screens__create_randd', target=obj)
            except Exception as er:
                print("view 5000: " + er)
                print(er)
            for a in s0.attributes.all():
                RandD_Attribute.objects.create(randd=obj, attribute=a, value=a.start_optimal_value - 2)
            # print("view 6000: ")
        else:
            obj = obj_model.objects.get(id=obj_id)
            create_action(request.user, 'globsim__get_sub_screens__view_randd', target=obj)

            # print("view 7000: ")
        # print(s_url)
        # print(obj)
        # print(segments)

        return render(request, s_url, {'name': model_name_, 'obj': obj, 'segments': segments})
    elif model_name_ == "product":
        obj = obj_model.objects.get(id=obj_id)
        team_ = game.get_current_team(request.user)
        randds = team_.team_rds.filter((~Q(period__period_number=F('period__game__current_period_number')) &
                                        Q(randd_products__isnull=True) | Q(id=obj.randd.id)
                                        )).all()
        # print('=========')
        # print(randds)
        try:
            obj.create_detail()
        except Exception as e:
            pass
        accounts_ = {}
        for account in obj.product_periods_data.all()[0].product_period_data_details.all():
            # n, category, account_, amount = get_account_tuple(account)

            try:
                x = accounts_[account.product_type_attribute.category]
            except Exception as e:
                accounts_[account.product_type_attribute.category] = {}
            accounts_[account.product_type_attribute.category][account.product_type_attribute.account] = {}
        first_date = 0
        for product_data_ in obj.product_periods_data.all():
            sp = product_data_.period.period
            if first_date == 0:
                first_date = int(sp)
            accounts = product_data_.product_period_data_details.all()
            for account1 in accounts:
                category = account1.product_type_attribute.category
                account = account1.product_type_attribute.account
                accounts_[category][account][sp] = (account1.id, account1.amount, account1.product_type_attribute.min,
                                                    account1.product_type_attribute.max)
                # print('accounts_[category][account][sp]')
                # print(accounts_[category][account][sp])
        # print('game.start_period + game.current_period_number + 1')
        # print(game.start_period + game.current_period_number + 1)
        periods = range(game.start_period, game.start_period + game.current_period_number + 1)
        # print(periods)
        # print(accounts_)
        # print('-------')
        # print(first_date)
        create_action(request.user, 'globsim__get_sub_screens__view_product', target=obj)
        return render(request, s_url, {'name': model_name_, 'obj': obj, 'periods': periods,
                                       'game': game, 'accounts': accounts_, 'first_date': first_date,
                                       'randds': randds})
    elif model_name_ == "gdistributor":
        obj = obj_model.objects.get(id=obj_id)
        # print('----')
        # print(obj)
        team_ = game.get_current_team(request.user)
        try:
            obj.create_detail()
        except Exception as er:
            print(er)
            # pass
        accounts_ = {}
        for g_distributor_data_ in obj.g_distributor_periods_data.all():
            sp = g_distributor_data_.period.period
            # print('----')
            # print(sp)
            accounts = g_distributor_data_.g_distributor_period_data_details.all()
            # print('----')
            # print(accounts)
            # print('----')
            for account in accounts:

                n, account_name, amount = account.id, account.distributor_attribute.name, account.amount
                # print(n, account_name, amount)
                # print('----')
                # print(account.distributor_attribute.min)
                # print(account.distributor_attribute.max)
                # print('111----1111')
                if account_name not in accounts_.keys():
                    accounts_[account_name] = {}
                accounts_[account_name][sp] = (n, amount,
                                               account.distributor_attribute.min, account.distributor_attribute.max)
                # print(accounts_[account_name][sp])
        # print(s_url)
        periods = range(game.start_period, game.start_period + game.current_period_number + 1)
        create_action(request.user, 'globsim__get_sub_screens__view_gdistributor', target=obj)
        return render(request, s_url, {'name': model_name_, 'obj': obj, 'periods': periods,
                                       'game': game, 'accounts_': accounts_})
    elif model_name_ == "finance":
        team_ = game.get_current_team(request.user)
        objs = obj_model.objects.filter(team=team_).all()
        # print('----')
        # print(objs)
        # print('----')

        try:
            for obj in objs:
                obj.create_detail()
        except Exception as er:
            print(er)
            # pass
        # print('1----')
        accounts_ = {}
        for obj in objs:
            obj_type = FinanceType.objects.filter(translations__language_code=get_language()).filter(finances__id=obj.id)[0]
            # print('1---')
            # print(obj_type.name)
            # print('1---')
            accounts_[obj_type.name] = {}
            for finance_data_ in obj.finance_periods_data.all():
                sp = finance_data_.period.period
                accounts = finance_data_.finance_period_data_details.all()
                for account in accounts:
                    obj_type_attribute = FinanceTypeAttribute.objects.filter(translations__language_code=get_language()).filter(finance_type_periods_detail=account)[0]

                    n, account_name, amount = account.id, obj_type_attribute.name, account.amount
                    if account_name not in accounts_[obj_type.name].keys():
                        accounts_[obj_type.name][account_name] = {}
                    accounts_[obj_type.name][account_name][sp] = (n, amount,
                                                                  account.finance_attribute.min,
                                                                  account.finance_attribute.max)
        #             print(obj_type.name, account_name, sp)
        #             print(accounts_[obj_type.name][account_name][sp])
        # print(s_url)
        periods = range(game.start_period, game.start_period + game.current_period_number + 1)
        create_action(request.user, 'globsim__get_sub_screens__view_finance', target=obj)
        return render(request, s_url, {'name': model_name_, 'objs': objs, 'periods': periods,
                                       'game': game, 'accounts': accounts_})


def update_attribute_value(request):
    obj_id = request.POST.get('obj_id')
    value = request.POST.get('value')
    # print(value)
    # print(obj_id)
    rr = {'status': 'ok'}
    try:
        a = RandD_Attribute.objects.get(id=int(obj_id))
        a.value = value
        a.save()
        rr["index"] = a.index
    except Exception as e:
        print("300 :" + e)
        rr = {'status': 'ko'}
    return JsonResponse(rr)


def change_segment(request):
    app_ = request.POST.get('app').lower()
    model_name_ = request.POST.get('model_name').lower()
    obj_id = request.POST.get('obj_id')
    slug = request.POST.get('slug')
    obj_model = apps.get_model(app_label=app_, model_name=model_name_)
    obj = obj_model.objects.get(id=obj_id)
    segment = get_object_or_404(Segment, translations__slug=slug)
    obj.segment = segment
    obj.save()
    as_ = obj.randd_attributes.all()
    if as_.exists():
        as_.delete()
    for s in segment.attributes.all():
        rd = RandD_Attribute.objects.create(attribute=s, randd=obj)
    s_url = 'globsim/_' + model_name_ + '_detail_attributes.html'
    return render(request, s_url, {'obj': obj})


def change_game_types(request):
    app_ = request.POST.get('app').lower()
    model_name_ = request.POST.get('model_name').lower()
    game_id = request.POST.get('game_id')
    obj_model = apps.get_model(app_label=app_, model_name=model_name_)
    game = obj_model.objects.get(id=game_id)
    slug = request.POST.get('slug')
    game_type = get_object_or_404(GameType, translations__slug=slug)
    game.game_type = game_type
    game.save()
    game.set_zero(request.user)
    rr = {'status': 'ok'}
    return JsonResponse(rr)


def change_randd(request):
    app_ = request.POST.get('app').lower()
    model_name_ = request.POST.get('model_name').lower()
    obj_id = request.POST.get('obj_id')
    randd_id = request.POST.get('randd_id')
    randd_pdd_id = request.POST.get('randd_pdd_id')

    # print(app_)
    # print(model_name_)
    # print(obj_id)
    # print(randd_id)

    obj_model = apps.get_model(app_label=app_, model_name=model_name_)
    pr_obj = obj_model.objects.get(id=obj_id)
    # print('-----')
    # print(pr_obj)
    # print('-----')

    rr = {'status': 'ok'}
    try:
        randd = get_object_or_404(RandD, id=randd_id)
        # print(randd)
        pr_obj.randd = randd
        pr_obj.save()

        randd_pdd_obj = get_object_or_404(ProductPeriodDataDetail, id=randd_pdd_id)
        # print(randd_pdd_obj)
        # print(randd_pdd_obj.id)
        randd_pdd_obj.amount = randd.id
        randd_pdd_obj.save()
    except Exception as e:
        print("400 :" + e)
        rr = {'status': 'ko'}
    # print(rr)
    return JsonResponse(rr)


# called after establishing a new game
def configure_globsim_game(request, game):
    print(1000)
    print(game.name)
    game_type = GameType.objects.all()[0]
    game.game_type = game_type
    game.save()
    # create new period
    period = Period.objects.create(game=game, period_number=0)
    # create new randd project

    print('done configure_globsim_game')


def management(request):
    slug = request.POST.get('slug')
    fun = request.POST.get('fun')
    game = get_object_or_404(Game, translations__slug=slug)
    s_fun = "game."+fun+"(request.user)"
    eval(s_fun)
    rr = {'status': 'ok'}
    return JsonResponse(rr)


def link_management_data(request):
    slug = request.POST.get('slug')
    fun = request.POST.get('fun')
    game = get_object_or_404(Game, translations__slug=slug)
    arg = {'game': game}
    if fun == "schedule_period_dates":
        arg['course_schedule'] = game.course_schedule
        arg['schedule_period_dates'] = game.get_schedule_period_dates
    elif fun == "edit_game_info":
        game.get_edit_game_info
    elif fun == "new_distributor_account":
        obj_slug = request.POST.get('obj_slug')
        distributors = Distributor.objects.filter(translations__language_code=get_language())
        distributor = distributors.filter(translations__slug=obj_slug)[0]
        r1 = random.randint(0, 10000000)
        s_slug = slugify(str(r1) + '-new distributor-' + get_language())
        da = DistributorAttribute.objects.create(distributor=distributor, slug=s_slug)
        da.name = "new"
        da.save()
        da.slug = slugify(str(da.pk) + '-distributor-account-' + get_language())
        da.save()
        fun = "edit_game_distributors"
    elif fun == "delete_distributor_account":
        obj_id = int(request.POST.get('obj_id'))
        DistributorAttribute.objects.get(pk=obj_id).delete()
        fun = "edit_game_distributors"
    elif fun == "delete_distributor":
        obj_id = int(request.POST.get('obj_id'))
        Distributor.objects.get(pk=obj_id).delete()
        fun = "edit_game_distributors"
    elif fun == "new_distributor":
        s_slug = slugify('0-new distributor-' + get_language())
        d = Distributor.objects.create(slug=s_slug, game_type=game.game_type)
        d.name = "new"
        d.save()
        d.slug = slugify(str(d.pk) + '-distributor-' + get_language())
        d.save()
        fun = "edit_game_distributors"

    elif fun == "new_finance_instrument":
        obj_slug = request.POST.get('obj_slug')
        finance_types = FinanceType.objects.filter(translations__language_code=get_language())
        finance_type = finance_types.filter(translations__slug=obj_slug)[0]
        r1 = random.randint(0, 10000000)
        s_slug = slugify(str(r1) + '-new finance-' + get_language())
        fa = FinanceTypeAttribute.objects.create(finance_type=finance_type, slug=s_slug)
        fa.name = "new"
        fa.save()
        fa.slug = slugify(str(fa.pk) + '-finance_instrument-' + get_language())
        fa.save()
        fun = "edit_game_finances"
    elif fun == "delete_finance_instrument":
        obj_id = int(request.POST.get('obj_id'))
        FinanceTypeAttribute.objects.get(pk=obj_id).delete()
        fun = "edit_game_finances"
    elif fun == "delete_finance_type":
        obj_id = int(request.POST.get('obj_id'))
        FinanceType.objects.get(pk=obj_id).delete()
        fun = "edit_game_finances"
    elif fun == "new_finance":
        s_slug = slugify('0-new finance-' + get_language())
        f = FinanceType.objects.create(slug=s_slug, game_type=game.game_type)
        f.name = "new"
        f.save()
        f.slug = slugify(str(f.pk) + '-finance-' + get_language())
        f.save()
        fun = "edit_game_finances"

    if fun == "edit_game_distributors":
        distributors = Distributor.objects.filter(translations__language_code=get_language())
        arg['distributors'] = distributors
    if fun == "edit_game_finances":
        finance_types = FinanceType.objects.filter(translations__language_code=get_language())
        arg['finance_types'] = finance_types

    s_html = "globsim/_" + fun + ".html"
    # print('1-----')
    # print(s_html)
    # print('1-----')
    return render(request, s_html, arg)


def team(request):
    title = _('Team')
    return render(request, 'globsim/team.html', {'title': title})

