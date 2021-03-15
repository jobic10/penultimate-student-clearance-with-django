from django import forms
from django.contrib.auth.hashers import make_password
from django.forms.widgets import DateInput, TextInput
from .models import *


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    # email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'size': 11, 'maxlength': 11}))

    widget = {
        'password': forms.PasswordInput(),
    }

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            instance = kwargs.get('instance').__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                print("CustomUser.objects.filter(phone=formPhone).exists()")
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).email.lower()
            if dbEmail != formEmail:  # There has been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError(
                        "The given email is already registered")
        return formEmail

    def clean_password(self):
        password = self.cleaned_data.get("password", None)
        if self.instance.pk is not None:
            if not password:
                print("EMPTY DAN => " + self.instance.password)
                # return None
                return self.instance.password

        return make_password(password)

    class Meta:
        model = CustomUser
        fields = ['email',  'phone', 'password', ]


class StudentForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

    def clean_phone(self, *args, **kwargs):
        formPhone = self.cleaned_data['phone'].lower()
        if len(formPhone) > 11:
            raise forms.ValidationError(
                "The given phone number exceeds 11 characters")
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(phone=formPhone).exists():
                raise forms.ValidationError(
                    "The given phone number is already registered")
        else:  # Update
            dbPhone = self.Meta.model.objects.get(
                id=self.instance.pk).phone.lower()
            if dbPhone != formPhone:  # There has been changes
                if CustomUser.objects.filter(phone=formPhone).exists():
                    raise forms.ValidationError(
                        "The given phone has already registered")

        return formPhone

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields + \
            ['fullname', 'regno', 'picture', 'phone', 'department']


class DepartmentForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LogForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Department
        fields = ['name']


class StudentEditForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Student
        fields = ['fullname', 'regno', 'picture', 'phone']
