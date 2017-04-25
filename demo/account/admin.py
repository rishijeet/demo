from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.forms import ModelForm, Select, TextInput, NumberInput
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import redirect
from django_select2.forms import ModelSelect2Widget
from suit import apps

from suit.admin import RelatedFieldAdmin, get_related_field
from suit.admin_filters import IsNullFieldListFilter
from suit.sortables import SortableTabularInline, SortableModelAdmin, SortableStackedInline
from suit.widgets import AutosizedTextarea, EnclosedInput
from .widgets import Bootstrap4Select
from .models import *
from .views import *

# Register your models here.


class AdditionalPlatformForm(ModelForm):
    class Meta:
        widgets = {
            # 'portal': EnclosedInput,
        }


class AdditionalPlatformInline(admin.TabularInline):
    form = AdditionalPlatformForm
    model = AdditionalPlatform
    list_display = ('name',)
    min_num = 0
    extra = 0
    verbose_name_plural = 'Additional Platforms'
    suit_classes = 'suit-tab suit-tab-portal'
    suit_form_inlines_hide_original = True



class SalesPricingForm(ModelForm):
    class Meta:
        widgets = {
            'portal': EnclosedInput,
        }


class SalesPricingInline(admin.TabularInline):
    form = SalesPricingForm
    model = SalesTemplate
    min_num = 0
    extra = 0
    verbose_name_plural = 'Sales Template'
    suit_classes = 'suit-tab suit-tab-sales'
    suit_form_inlines_hide_original = True


class AlgoXPricingForm(ModelForm):
    class Meta:
        widgets = {
            'fixing_info': EnclosedInput,
            'from_amount': EnclosedInput,
            'to_amount': EnclosedInput,
            'hidden_mark_up': EnclosedInput,
            'explicit_mark_up': EnclosedInput,
        }


class AlgoXPricingInLine(admin.TabularInline):
    form = AlgoXPricingForm
    model = AlgoXTemplate
    min_num = 0
    extra = 0
    verbose_name_plural = 'AlgoX Template'
    suit_classes = 'suit-tab suit-tab-algox'
    suit_form_inlines_hide_original = True

class AccountForm(ModelForm):
    class Meta:
        widgets = {
            # 'code': TextInput(attrs={'class': 'input-mini'}),
            #'independence_day': SuitDateWidget,
            'description': AutosizedTextarea,
        }

@admin.register(Account)
class AccountAdmin(RelatedFieldAdmin):
    form = AccountForm
    search_fields = ('externalid', 'profile')
    list_display = ('portal', 'externalid', 'settlement_location', 'link_to_account_group', 'link_to_customer', 'disabled', 'do_not_trade', 'updated')
    list_filter = ('portal', 'externalid', 'customer',)
    #suit_list_filter_horizontal = ('code', 'population')
    list_select_related = True
    inlines = (AdditionalPlatformInline, )
    # date_hierarchy = 'independence_day'

    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ['externalid', 'portal', 'account_group', 'platform', 'settlement_location']
        }),
        ('Account Details', {
            'classes': ('suit-tab suit-tab-general',),
            'description': 'EnclosedInput widget examples',
            'fields': ['profile', 'do_not_trade', 'customer']}),
        ('Account Description', {
            'classes': ('suit-tab suit-tab-general',),
            'description': 'AutosizedTextarea widget example - adapts height '
                           'based on user input',
            'fields': ['description']}),
        ('Trade Info', {
            'classes': ('suit-tab suit-tab-general',),
            'description': 'Tabs can contain any fieldsets and inlines',
            'fields': ['pip_slippage', 'worst_allowable_pnl']}),
    ]

    suit_form_size = {
        'fields': {
            'portal': apps.SUIT_FORM_SIZE_INLINE,
            'externalid': apps.SUIT_FORM_SIZE_SMALL,
            'account_group': apps.SUIT_FORM_SIZE_INLINE,
        },
        'widgets': {
            'AutosizedTextarea': apps.SUIT_FORM_SIZE_XXX_LARGE,
        },
    }

    suit_form_tabs = (
        ('general', 'General'),
        ('portal', 'Portals'),
        ('sales', 'Sales Pricing'),
        ('charts', 'Trader Pricing'),
        ('algox', 'AlgoX Tab'),
        ('misc', 'Miscellaneous'),
        ('ncmr',  'NCMR')
    )

    suit_form_includes = (
        ('admin/demo/country/tab_docs.html', '', 'ncmr'),
    )


class AccountInlineForm(ModelForm):
    class Meta:
        widgets = {
            # 'code': TextInput(attrs={'class': 'input-mini'}),
            # 'population': TextInput(attrs={'class': 'input-medium'}),
            # 'independence_day': SuitDateWidget,
        }


class AccountInline(admin.TabularInline):
    form = AccountInlineForm
    model = Account
    fields = ('portal', 'externalid', 'settlement_location', 'customer', )
    extra = 1
    suit_classes = 'suit-tab suit-tab-general'
    suit_form_inlines_hide_original = True
    verbose_name_plural = 'Accounts'


class AccountGroupForm(ModelForm):
    class Meta:
        widgets = {
            # 'code': TextInput(attrs={'class': 'input-mini'}),
            #'independence_day': SuitDateWidget,
            'name': AutosizedTextarea,
        }

@admin.register(AccountGroup)
class AccountGroupAdmin(RelatedFieldAdmin):
    form = AccountGroupForm
    search_fields = ('name',)
    list_display = ('name', 'accounts', 'updated',)
    list_filter = ('settlement_location', )
    inlines = (AccountInline, SalesPricingInline, AlgoXPricingInLine, )

    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ['name', 'settlement_location']
        }),
        ('Group Details', {
            'classes': ('suit-tab suit-tab-general',),
            'description': 'EnclosedInput widget examples',
            'fields': ['do_not_trade', 'disabled']}),
    ]

    suit_form_size = {
        'fields': {
            'name': apps.SUIT_FORM_SIZE_INLINE,
        },
        'widgets': {
            'AutosizedTextarea': apps.SUIT_FORM_SIZE_XXX_LARGE,
        },
    }

    suit_form_tabs = (
        ('general', 'General'),
        ('sales', 'Sales'),
        ('charts', 'Trader'),
        ('algox', 'AlgoX'),
    )

    suit_form_includes = (
        ('admin/demo/country/tab_docs.html', 'bottom', 'algox'),
    )

    def accounts(self, obj):
        return len(obj.account_set.all())


class CustomerForm(ModelForm):
    class Meta:
        widgets = {
            'universal_customer_number': EnclosedInput,
        }


@admin.register(Customer)
class CustomerFormAdmin(RelatedFieldAdmin):
    form = CustomerForm
    min_num = 1
    extra = 0
    verbose_name_plural = 'Primary Customers'
    search_fields = ('name',)
    list_display = ('name', 'accounts', )
    inlines = (AccountInline, )

    def accounts(self, obj):
        return len(obj.account_set.all())



class ProfileForm(ModelForm):
    class Meta:
        widgets = {
            'name': EnclosedInput,
        }


@admin.register(Profile)
class ProfileFormAdmin(SortableModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'accounts')
    sortable = 'order'
    inlines = (AccountInline, )
    verbose_name_plural = 'Profile'

    def suit_row_attributes(self, obj, request):
        class_map = {
            'citi': 'table-success',
            'america': 'table-warning',
            'india': 'table-success',
            'barclay': 'table-danger',
            'test': 'table-info',
        }
        css_class = ''
        for key in class_map:
            if key in obj.name.lower():
                css_class = class_map.get(key)
        if css_class:
            return {'class': css_class}

    def suit_column_attributes(self, column):
        if column == 'accounts':
            return {'class': 'text-xs-center'}

    def suit_cell_attributes(self, obj, column):
        if column == 'accounts':
            cls = 'text-xs-center'
            if 'test' in obj.name.lower():
                cls += ' table-danger'
            return {'class': cls}

    def accounts(self, obj):
        return len(obj.account_set.all())
