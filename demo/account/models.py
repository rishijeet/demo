from __future__ import unicode_literals

from django.db import models

PORTALS = ((1, 'MORGS'), (2, 'BBG'), (3, 'MDAPI'), (4, 'MORGQ'), (5, 'CURREX'), (6, 'ALGOX'), (7, '360T'))
PLATFORM = ((1, 'JPMM'), (2, 'MorganDirect'), (3, 'Bloomberg'))
SETTLEMENT_LOCS = ((1, 'NYK'), (2, 'LDN'), (3, 'SGP'), (4, 'TYK'), (5, 'BRA'), (6, 'MUB'), (7, 'HGK'))
DISABLED_CCYS = ((1, 'USD'), (2, 'INR'), (3, 'AUD'), (4, 'GBP'), (5, 'SGD'), (6, 'HKD'), (7, 'CHN'))
CCY_PAIRS = ((1, 'USD-INR'), (2, 'INR-AUD'), (3, 'AUD-USD'), (4, 'GBP-USD'), (5, 'SGD-RUB'), (6, 'HKD-USD'), (7, 'CHN-USD'))
ORDER_TYPES = ((1, 'TRADER'), (2, 'SALES'))
AMOUNT_UNIT = ((1, 'USD'), (2, '*'))
# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=256)
    order = models.PositiveIntegerField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class AccountGroup(models.Model):
    name = models.CharField(max_length=256)
    settlement_location = models.SmallIntegerField(
        choices=SETTLEMENT_LOCS, default=1, help_text="Select Settlement Locs")
    disabled = models.BooleanField(default=False, help_text="Default Auto")
    do_not_trade = models.BooleanField(default=False, help_text="Default False")
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Customer(models.Model):
    name = models.CharField(max_length=256)
    universal_customer_number = models.CharField(max_length=12)
    special_party_number = models.CharField(max_length = 30)
    netlink_enabled = models.BooleanField(default=False, help_text="Default False")
    pb_acronym = models.CharField(max_length = 30)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Account(models.Model):
    account_group = models.ForeignKey(AccountGroup, null=False)
    externalid = models.CharField(max_length=80)
    # code = models.CharField(max_length=2,
    #                         help_text='ISO 3166-1 alpha-2 - two character country code')

    # now create portal model
    portal = models.SmallIntegerField(
        choices=PORTALS, help_text="Select Portal")

    # now create platform model
    platform = models.SmallIntegerField(
        choices=PLATFORM, help_text="Select Platform")

    settlement_location = models.SmallIntegerField(
        choices=SETTLEMENT_LOCS, default=1, help_text="Select Settlement Locs")
    profile = models.ForeignKey(Profile, null=False)
    disabled = models.BooleanField(default=False, help_text="Default Auto")
    do_not_trade = models.BooleanField(default=False, help_text="Default False")
    max_trade_size = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, help_text='Description about account')
    customer = models.ForeignKey(Customer, null=False)
    pip_slippage = models.CharField(max_length=2, default='0.0')
    worst_allowable_pnl = models.CharField(max_length=10)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.externalid

    class Meta:
        ordering = ('externalid',)
        verbose_name_plural = 'Accounts'


# Stacked inline model for Account
class AdditionalPlatform(models.Model):
    account = models.ForeignKey(Account)
    portal = models.SmallIntegerField(choices=PORTALS)
    order = models.PositiveIntegerField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.portal


class DisabledCurrencies(models.Model):
    account_group = models.ForeignKey(AccountGroup)
    ccy = models.SmallIntegerField(choices=DISABLED_CCYS)
    order = models.PositiveIntegerField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.ccy


class SalesTemplate(models.Model):
    account_group = models.ForeignKey(AccountGroup)
    name = models.CharField(max_length=256)
    order_type = models.SmallIntegerField(
        choices=ORDER_TYPES, help_text="Select Order Type")
    order = models.PositiveIntegerField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.name

class AlgoXTemplate(models.Model):
    account_group = models.ForeignKey(AccountGroup)
    name = models.CharField(max_length=256)
    markup_mode = models.SmallIntegerField(
        choices=ORDER_TYPES, help_text="Select Order Type")
    currency_pair = models.SmallIntegerField(
        choices=CCY_PAIRS, help_text="Select Currency Pair")
    amount_unit = models.SmallIntegerField(
        choices=AMOUNT_UNIT, help_text="Select Amount Unit")
    from_amount = models.TextField(max_length = 10)
    to_amount = models.TextField(max_length = 10)
    hidden_mark_up = models.TextField(max_length = 10, default = '*')
    explicit_mark_up = models.TextField(max_length = 10, default = '*')
    fixing_info = models.TextField(max_length = 10, default = '*')
    order = models.PositiveIntegerField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.name

