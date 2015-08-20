from django import forms


class LoginForm(forms.Form):
    inputUsername = forms.CharField(label='',
                                    max_length=30,
                                    required=True,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Username'})
                                    )
    inputPassword = forms.CharField(label='',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                      'placeholder': 'Password'}))


class RegisterForm(forms.Form):
    inputUsername = forms.CharField(label='',
                                    max_length=30,
                                    required=True,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Username'})
                                    )
    inputFirstName = forms.CharField(label='',
                                     max_length=50,
                                     required=False,
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': 'First name (optional)'})
                                     )
    inputLastName = forms.CharField(label='',
                                    max_length=50,
                                    required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Last name (optional)'})
                                     )
    inputEmail = forms.EmailField(label='',
                                  max_length=50,
                                  required=True,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Email'})
                                     )
    inputPassword = forms.CharField(label='',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                      'placeholder': 'Password'}))
    inputPassword2 = forms.CharField(label='',
                                     widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'Repeat password'}))


class AddForm(forms.Form):
    inputTitle = forms.CharField(label='',
                                 max_length=150,
                                 required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Challenge title/name'})
                                 )
    inputDescription = forms.CharField(label='',
                                       max_length=5000,
                                       required=True,
                                       widget=forms.Textarea(attrs={'class': 'form-control',
                                                                    'placeholder': 'Challenge description'}),
                                       )


class MessageForm(forms.Form):
    inputTitle = forms.CharField(label='',
                                 max_length=50000,
                                 required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Title'})
                                 )
    inputContent = forms.CharField(label='',
                                   max_length=2000000000,
                                   required=True,
                                   widget=forms.Textarea(attrs={'class': 'form-control',
                                                                'placeholder': 'Message'})
                                   )


class SearchForm(forms.Form):
    inputUsername = forms.CharField(label='',
                                     max_length=50000,
                                     required=False,
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': 'Username'})
                                     )
    inputFirstName = forms.CharField(label='',
                                      max_length=50000,
                                      required=False,
                                      widget=forms.TextInput(attrs={'class': 'form-control',
                                                                    'placeholder': 'First name'})
                                      )
    inputLastName = forms.CharField(label='',
                                     max_length=50000,
                                     required=False,
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': 'Last name'})
                                     )
    inputEmail = forms.CharField(label='',
                                  max_length=50000,
                                  required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Email'})
                                     )
