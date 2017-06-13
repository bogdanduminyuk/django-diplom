from django import forms


class CustomTextInput(forms.TextInput):
    def __init__(self):
        super(CustomTextInput, self).__init__(attrs={'class': 'form-control'})


class CustomTextArea(forms.Textarea):
    def __init__(self, size_tuple):
        rows, cols = size_tuple
        super(CustomTextArea, self).__init__(attrs={
            'class': 'form-control',
            'rows': rows,
            'cols': cols,
        })
