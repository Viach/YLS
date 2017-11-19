import json
from django import forms
from mainapp.models import Lab


class JsonWidget(forms.MultiWidget):
    # template_name = 'django/forms/widgets/row_input.html'
    def __init__(self):
        _widget = [
            forms.widgets.TextInput(),
            forms.widgets.TextInput(),
            forms.widgets.TextInput(),
        ]
        super(JsonWidget, self).__init__(widgets=_widget)

    def decompress(self, value):
        value = ['1', '2', '3']
        return value


class RowWidget(forms.MultiWidget):
    def __init__(self):
        _widget = [
            JsonWidget(),
            JsonWidget(),
        ]
        super(RowWidget, self).__init__(widgets=_widget)

    def decompress(self, value):
        # value = json.loads(value) if value else  ['', '']
        value = ['1', '2']
        return value

    def render(self, name, value, attrs=None, renderer=None):
        self.template_name = 'widgets/row_input.html'
        super(RowWidget, self).render(name, value, attrs=None, renderer=None)


class LabForm(forms.ModelForm):
    json_field = forms.CharField(widget=RowWidget, max_length=500)

    class Meta:
        model = Lab
        fields = ['name', 'json_field']

    def is_valid(self):
        self.save()


class DLabForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        l = 3
        super(DLabForm, self).__init__(*args, **kwargs)
        for i in range(l):
            self.fields['f' + str(i)] = forms.FloatField(label='f' + str(i))

    def clean_json_field(self):
        data = self.data['f1'] + self.data['f2'] + self.data['f0']
        return data

    class Meta:
        model = Lab
        fields = ['name', 'json_field']
        widgets = {'json_field': forms.HiddenInput}
