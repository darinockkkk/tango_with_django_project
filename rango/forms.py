from django import forms
from rango.models import Page, Category


# make sure the form gonna contain and pass on all the data that is required to populate your model correctly

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                            help_text="Please enter the category name.")
    # widget=forms.HiddenInput() hides the field in the form (users can’t see or edit it).
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # required=False means the field is not required by the form
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # inline class to provide additional information on the form.
    class Meta:
        # connect this form to the Category model
        model = Category
        # specify which fields from the model should be included in the form
        fields = ('name', )

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200,
                            help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        # we can either exclude the category field from the form,
        exclude = ('category',)
        # equivalent to fields = ('title', 'url', 'views')
    
    # overriding clean method to clean and validate user input before saving the form
    def clean(self):
        # self refers to the current instance of the form
        
        # gets all user-submitted data after Django’s default validation
        # cleaned_data is dict where keys = form fields, values = user input
        cleaned_data = self.cleaned_data

        # gets the url field from the form (from our dict)
        url = cleaned_data.get('url')

        # fix and update URL entered by the user before saving it
        if url and not url.startswith('http://'):
            
            # f-string (formatted string) to add "http://" to the beginning
            url = f'http://{url}'
            
            # updates the cleaned form data so that the corrected URL is saved
            cleaned_data['url'] = url
        
        # without this line, changes won’t be applied
        return cleaned_data