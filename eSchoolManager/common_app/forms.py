from django import forms


class SearchForm(forms.Form):
    search_query = forms.CharField(
        error_messages='',
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search',
                'class': 'input-search',
                'type': 'text'
            }
        ),
        required=False
    )
