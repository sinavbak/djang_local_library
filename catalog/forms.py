import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text = "Yeni tarihi girin 3 hafta")
    
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        if data < datetime.date.today():
            raise ValidationError(_('Geçmiş tarih girilemez'))
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('İleri tarig girilemez'))
        
        return data