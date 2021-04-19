from django import forms
from .models import Cost


class BS4CostForm(forms.ModelForm):
    """Bootstrapに対応するためのModelForm"""

    class Meta:
        model = Cost
        # Costで表示するフィールド、'__all__'とすると全て
        fields = ('summary', 'money', 'description')
        # widget = {‘事前に設定をしたクラスのfield’:forms.TextInput等(attrs={‘class’: ‘cssのclass名’})}
        widgets = {
            'summary': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'money': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
            }),
        }


def clean_money(self):
    money = self.cleaned_data['money']
    if 0 > money:
        raise forms.ValidationError('それやと増えとるがな')
    return money
