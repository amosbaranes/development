from __future__ import unicode_literals
from .models import (FabHoseAfricaWeb, Home, Catalog, CatalogSection, CatalogSectionCategory,
                     CatalogSectionCategoryStyle, CatalogSectionImageStyleImage,
                     Contact, ReceivedMessages, ContactInformation, Gallery, GalleryItems, About)
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


@admin.register(FabHoseAfricaWeb)
class FabHoseAfricaWebAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name')
    # list_filter = ('status', 'created', 'publish', 'author')
    # search_fields = ('title', 'body')
    # prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('author',)
    # date_hierarchy = 'publish'
    # ordering = ('status', 'publish')


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'fab_hose_africa_web',)


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'fab_hose_africa_web', )


@admin.register(CatalogSection)
class CatalogSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'section_title', )


@admin.register(CatalogSectionCategory)
class CatalogSectionCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'section', 'category_title', )
    list_filter = ('section', )


@admin.register(CatalogSectionCategoryStyle)
class CatalogSectionCategoryStyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'style_title', )
    list_filter = ('category', )


@admin.register(CatalogSectionImageStyleImage)
class CatalogSectionImageStyleImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'style', 'image_title', )
    list_filter = ('style', )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'fab_hose_africa_web')


@admin.register(ReceivedMessages)
class ReceivedMessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact', 'name', 'email', 'subject')


@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact', 'title')


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'section_title', 'fab_hose_africa_web')


@admin.register(GalleryItems)
class GalleryItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'gallery', 'image_title')


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('id', 'fab_hose_africa_web', 'about_us_title')

