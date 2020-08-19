from django import forms
from apps.app_base.utils import decrypt


class PersonalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.obj = kwargs.pop('obj', None)
        super(PersonalForm, self).__init__(*args, **kwargs)

        if self.obj:
            self.initial['full_name'] = decrypt(self.obj.full_name) if self.obj.full_name else None
