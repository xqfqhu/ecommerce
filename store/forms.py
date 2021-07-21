from django import forms
from .models import Category, Product

class searchForm(forms.Form):


    choices = [('all','All')]

    for c in Category.objects.filter(parent=None):
        choices.append((c.slug, c.name))

    
    category = forms.ChoiceField(choices =choices)
    keyword = forms.CharField(
        label = "keyword",
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control mb-3',
                'placeholder': 'Search by Title, Author, Keyword, or ISBN',
                'id': 'search-keyword',
                }),
                required = False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({
            'class': 'form-select me-0',
            "style": "width: 20%"
            })
        self.fields['keyword'].widget.attrs.update({
            'class': 'form-control me-0',
            "style": "width: 60%"
            })