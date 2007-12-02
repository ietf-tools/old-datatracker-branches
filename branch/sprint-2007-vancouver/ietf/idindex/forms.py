# Copyright The IETF Trust 2007, All Rights Reserved

from django import newforms as forms
from ietf.idtracker.models import IDState, IDStatus, IETFWG
from ietf.idindex.models import orgs

class IDIndexSearchForm(forms.Form):
    within_choices= [
	  ('','All/Any'),
	  ('7','+/- 1 week'),
	  ('31','+/- 1 month'),
	  ('90', '+/- 3 months'),
    ]
    filename = forms.CharField(max_length=100, label='Filename (Full or Partial):', widget=forms.TextInput(attrs={'size': 30}))
    id_tracker_state_id = forms.ChoiceField(label='I-D Tracker State:')
    wg_id = forms.ChoiceField(label='Working Group:')
    other_group = forms.ChoiceField(choices=[('', 'All/Any')] + [(org['key'], org['name']) for org in orgs], label='Other Group:')
    status_id = forms.ChoiceField(label='I-D Status:')
    sub_after_date  = forms.DateField(label='Submitted After')
    exp_after_date  = forms.DateField(label='Expires After')
    sub_before_date = forms.DateField(label='Submitted Before')
    exp_before_date = forms.DateField(label='Expires Before')
    sub_within_date = forms.ChoiceField(choices=within_choices, label='Submitted Within')
    exp_within_date = forms.ChoiceField(choices=within_choices, label='Expires Within')
    last_name = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    def __init__(self, *args, **kwargs):
	super(IDIndexSearchForm, self).__init__(*args, **kwargs)
	self.fields['id_tracker_state_id'].choices = [('', 'All/Any')] + IDState.choices()
	self.fields['wg_id'].choices = [('', 'All/Any')] + IETFWG.choices()
	self.fields['status_id'].choices = [('', 'All/Any')] + [(status.status_id, status.status) for status in IDStatus.objects.all()]
