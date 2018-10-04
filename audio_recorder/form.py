from django import forms


class NameRegisterForm(forms.Form):
    name = forms.CharField(max_length=100)

    def clean_name(self):
        if self.cleaned_data['name'] is None:
            return None
        return self.cleaned_data['name']
