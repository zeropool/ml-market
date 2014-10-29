from django import forms
from polls.models import Market, Outcome, Order, Document
from django.core import validators
from _decimal import Decimal
from django.forms import widgets
 
# 
class MarketForm(forms.Form):

    # the market this form is about
    market = None
    # all outcomes connected to that market
    outcomes = None
    # the account the user is logged in with
    account = None
    # the (single bet) claim the user has selected 
    claim = None
    # the (single bet) amount the user has selected
    amount = forms.DecimalField(
        initial=0,
        max_digits=6, 
        decimal_places=2,
        widget = widgets.NumberInput(attrs = { 'onchange': 'validate_amount(this)'}))
    
    

    template_name = 'market/detail.html'

    errors = {}

    # a hook to the context-handling data
    # maybe (!) passes the vars to the template
    #def get_context_data(self, **kwargs):
    #    context = super(MarketForm, self).get_context_data(**kwargs)

    #    # obtain the account 
    #    #try:
    #    #    acc = request.user.account_set.get(market=self.object)
    #    #except Account.DoesNotExist:
    #    #    acc = None
    #    context['accountzasd'] = self.account

    #    return context

    def validate(self):
        self.errors = {}

        # check if claim is non-null and a valid one. 
        if self.claim == None:
            self.errors['claim'] = "Please select a claim. "
        elif self.market.outcome_set.filter(id=self.claim).count() != 1:
            self.errors['claim'] = 'Please select a valid claim. '

        # check if amount is non-null, valid and not greater than current funds
        if self.amount == None:
            self.errors['amount'] = "Please select the amount to bet. "
        elif self.amount > self.account.funds:
            self.errors["amount"] = "You've bet more than you have!"
        elif self.amount < 0:
            pass    # for now

        return len(self.errors) == 0 

    

    def __init__(self, market, account, *args, **kwargs):
        self.market = market
        self.outcomes = market.outcome_set.all()
        self.account = account
        if kwargs.get('post'):
            post = kwargs['post']
            try:
                self.claim = int(post['claim'])
            except: 
                self.claim = None

            try:
                self.amount = Decimal(post['amount'])
            except: 
                self.amount = None

        super(MarketForm, self).__init__()


class UploadForm(forms.Form):
    file = forms.FileField(
        label = "Select a file",
        help_text='max. 50 megabytes')

    file_list = forms.ModelMultipleChoiceField(
        queryset=None,)

    def __init__(self, u, *args, **kwargs):
        super(UploadForm, self).__init__()
        self.fields['file_list'].queryset = Document.objects.filter(user=u)


class UserForm(forms.Form):
    user = None

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)