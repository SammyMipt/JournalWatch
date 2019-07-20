from django import forms
from .models import Article


class AddingForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('DOI', 'theme',)

    def clean(self):
        if 'DOI' in self.cleaned_data and 'article_file' in self.cleaned_data:
            if not self.cleaned_data['DOI'] and not self.cleaned_data['article_file']:
                raise forms.ValidationError("You should enter DOI or give me the article itself, please.")
        return self.cleaned_data


class GettingForm(forms.Form):
    created_at_start = forms.DateTimeField(widget=forms.widgets.SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
    ), label='Start date',
        required=True)
    created_at_end = forms.DateTimeField(widget=forms.widgets.SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
    ), label='End date',
        required=True)
