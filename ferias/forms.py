from django import forms

from marketplaces.models import Marketplace
#from crowdsourcing.models import MarketplaceCrowdsourced


class MarketplaceForm(forms.ModelForm):
    class Meta:
        model = Marketplace
        # Get only the field 'fairground'
        fields = ("fairground",)

"""
class MarketplaceCrowdsourcedForm(forms.ModelForm):
    class Meta:
        model = MarketplaceCrowdsourced
        fields = '__all__'
"""