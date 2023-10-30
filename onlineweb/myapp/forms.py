from django import forms  
from myapp.models import register,donorregister

class Updatepro(forms.ModelForm):  
    class Meta:  
        model=donorregister  
        fields="__all__"  