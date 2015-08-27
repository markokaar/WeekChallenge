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
                                  max_length=255,
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


# profile edit forms
class EditUsernameForm(forms.Form):
    inputUsername = forms.CharField(label='',
                                    max_length=50000,
                                    required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Username'})
                                    )
    inputPassword = forms.CharField(label='',
                                    required=True,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                      'placeholder': 'Password'}))


class EditNameForm(forms.Form):
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


class EditEmailForm(forms.Form):
    inputEmail = forms.CharField(label='',
                                 max_length=50000,
                                 required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Email'})
                                 )


class EditPasswordForm(forms.Form):
    inputPassword = forms.CharField(label='',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                      'placeholder': 'Old password'}))
    inputNewPassword = forms.CharField(label='',
                                       widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'New password'}))
    inputNewPassword2 = forms.CharField(label='',
                                        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                          'placeholder': 'Repeat new password'}))


class EditBioForm(forms.Form):
    inputBio = forms.CharField(label='',
                               max_length=5000,
                               required=True,
                               widget=forms.Textarea(attrs={'class': 'form-control',
                                                            'placeholder': 'Bio'}),
                               )
