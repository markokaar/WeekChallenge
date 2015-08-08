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
