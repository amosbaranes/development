from django.urls import path
from .views import (home, get_companies_valuation_actual, wacc_ebit_roic, team, update_data, update_data_year,
                    update_account, get_industry_detail, get_company_detail, get_interest_coverage_ratio,
                    get_screens)

app_name = "corporatevaluation"

urlpatterns = [
    path('home/<int:obj_id>/', home, name='home'),
    path('wacc_ebit_roic/', wacc_ebit_roic, name='wacc_ebit_roic'),
    path('team/', team, name='team'),
    path('update_data/', update_data, name='update_data'),
    path('update_account/', update_account, name='update_account'),
    path('update_data_year/', update_data_year, name='update_data_year'),
    path('get_industry_detail/', get_industry_detail, name='get_industry_detail'),
    path('get_companies_valuation_actual/', get_companies_valuation_actual, name='get_companies_valuation_actual'),
    path('get_company_detail/', get_company_detail, name='get_company_detail'),
    path('get_interest_coverage_ratio/', get_interest_coverage_ratio, name='get_interest_coverage_ratio'),

    path('get_screens/', get_screens, name='get_screens'),
]
