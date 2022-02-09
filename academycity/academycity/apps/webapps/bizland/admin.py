from django.contrib import admin
from .models import BizlandWeb, FAQ, Contact, ReceivedMessages, Service, Portfolio, PortfolioItem, PortfolioCategory


@admin.register(BizlandWeb)
class BizlandWebAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'email', 'phone', )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'bizland_web')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'bizland_web', 'title')


@admin.register(ReceivedMessages)
class ReceivedMessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact', 'name', 'email', 'subject')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('company', 'title', )


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('bizland_web', 'title', )


@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'name', )
    list_filter = ['portfolio', ]


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('portfolio_category', 'name', )
    list_filter = ['portfolio_category', ]

