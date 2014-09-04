from corehq.apps.receiverwrapper.models import FormRepeater, RegisterGenerator

from django import forms


class GenericRepeaterForm(forms.Form):
    url = forms.URLField(
        required=True,
        label='URL to forward to',
        help_text='Please enter the full url, like http://www.example.com/forwarding/',
        widget=forms.TextInput(attrs={"class": "url"})
    )


class FormRepeaterForm(GenericRepeaterForm):
    exclude_device_reports = forms.BooleanField(
        required=False,
        label='Exclude device reports',
        initial=True
    )

    def __init__(self, *args, **kwargs):
        self.domain = kwargs.pop('domain')
        super(FormRepeaterForm, self).__init__(*args, **kwargs)

        self.formats = RegisterGenerator.all_formats_by_repeater(FormRepeater, for_domain=self.domain)

        if self.formats and len(self.formats) > 1:
            self.fields['format'] = forms.ChoiceField(
                required=True,
                label='Payload Format',
                choices=self.formats,
            )

    def clean(self):
        cleaned_data = super(FormRepeaterForm, self).clean()
        if 'format' not in cleaned_data:
            cleaned_data['format'] = self.formats[0][0]

        return cleaned_data