from django.urls import path
from .views import (home, candle,
                    home_chat_working,
                    # get_companies_valuation_actual,
                    wacc_ebit_roic, team, update_data, update_data_year,
                    update_account, get_industry_detail,
                    # get_company_detail,
                    get_interest_coverage_ratio,
                    get_screens, update_todo, delete_todo,
                    get_accounts, get_data_ticker,
                    admin_setup, admin_setup_attribute, tdameritrade_setup_w_attribute, analysis_setup_attribute,
                    activate_obj_function,
                    stream, sse,
                    # streama,
                    sec, get_r, get_sec, onchange_account, get_matching_accounts,
                    save_industry_default,
                    create_company_by_ticker,
                    get_risk_premium,
                    update_country_risk,
                    app, ac_home)

# create_company_by_ticker,

app_name = "corporatevaluation"

urlpatterns = [
    path('', ac_home, name='ac_home'),
    path('app/<str:app_name>/', app, name='app'),
    path('activate_obj_function/', activate_obj_function, name='activate_obj_function'),
    path('candle/', candle, name='candle'),
    path('home/<int:obj_id>/', home, name='home'),
    path('home_chat_working/<int:obj_id>/', home_chat_working, name='home_chat_working'),

    path('wacc_ebit_roic/', wacc_ebit_roic, name='wacc_ebit_roic'),
    path('team/', team, name='team'),
    path('update_data/', update_data, name='update_data'),
    path('update_account/', update_account, name='update_account'),
    path('update_data_year/', update_data_year, name='update_data_year'),
    path('get_industry_detail/', get_industry_detail, name='get_industry_detail'),
    # path('get_companies_valuation_actual/', get_companies_valuation_actual, name='get_companies_valuation_actual'),
    # path('get_company_detail/', get_company_detail, name='get_company_detail'),
    path('get_interest_coverage_ratio/', get_interest_coverage_ratio, name='get_interest_coverage_ratio'),

    path('update_country_risk/', update_country_risk, name='update_country_risk'),

    path('get_screens/', get_screens, name='get_screens'),
    path('update_todo/', update_todo, name='update_todo'),
    path('delete_todo/', delete_todo, name='delete_todo'),

    path('get_accounts/', get_accounts, name='get_accounts'),
    path('get_data_ticker/', get_data_ticker, name='get_data_ticker'),
    path('admin_setup/', admin_setup, name='admin_setup'),
    path('admin_setup_attribute/', admin_setup_attribute, name='admin_setup_attribute'),
    path('tdameritrade_setup_w_attribute/', tdameritrade_setup_w_attribute, name='tdameritrade_setup_w_attribute'),
    path('analysis_setup_attribute/', analysis_setup_attribute, name='analysis_setup_attribute'),

    path('sec/', sec, name='sec'),
    path('get_r/', get_r, name='get_r'),
    path('get_sec/', get_sec, name='get_sec'),
    path(r'stream/', stream, name='stream'),
    path(r'sse/', sse, name='sse'),
    # path(r'streama/', streama, name='streama'),

    # Data_Processing
    path('get_matching_accounts/', get_matching_accounts, name='get_matching_accounts'),
    path('onchange_account/', onchange_account, name='onchange_account'),
    path('save_industry_default/', save_industry_default, name='save_industry_default'),
    # path('clean_data_for_all_companies/', clean_data_for_all_companies, name='clean_data_for_all_companies'),
    path('create_company_by_ticker/', create_company_by_ticker, name='create_company_by_ticker'),
    # Valuation
    path('get_risk_premium/', get_risk_premium, name='get_risk_premium'),
]
