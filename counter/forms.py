from django.forms import *
from counter.models import *

class IncludeExcludeForm(Form):
	CHOICES=[('include','With ALL of the following'),
			 ('exclude','With NONE of the following')]
	CHOICES_MAP=[('include',"Only these maps"),
			 ('exclude',"Every map except")]
	player_select = ChoiceField(choices=CHOICES, widget=RadioSelect())
	player_choices = ModelMultipleChoiceField(widget=SelectMultiple(attrs={'class':'form-control'}),queryset=Player.objects.all(), required=False)
	map_select = ChoiceField(choices=CHOICES_MAP, widget=RadioSelect())
	map_choices = ModelMultipleChoiceField(widget=SelectMultiple(attrs={'class':'form-control','size':'17;'}),queryset=Map.objects.all(), required=False)

class AddForm(ModelForm):
	class Meta:
		model=Result
		exclude=[]


class AddPlayerForm(ModelForm):
	class Meta:
		model=Player
		exclude=[]