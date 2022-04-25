from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, SetPasswordForm, \
    PasswordChangeForm

from .models import CustomUser, Product, ImageProduct, Order, StatusOrder, ProductInOrder


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'phone_number')


class CustomSetPasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    #
    # class Meta(SetPasswordForm):
    #     model = CustomUser
    #     fields = ('email', 'phone_number')


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'surname',
            'first_name',
            'phone_number',
        )


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Product
        fields = (
            'title',
            'description',
            'cost',
            'vendor_code',
            'category',
            'characteristics',
        )
        widgets = {
            'characteristics': forms.Textarea(),
            'description': forms.Textarea(),
        }


class ChangeQuanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = ProductInOrder
        fields = (
            'quantity',
        )


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Order
        fields = (
            'address',
        )
        widgets = {
            'address': forms.Textarea(),
        }


class TrackNumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Order
        fields = (
            'track_num',
        )


class StatusOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = StatusOrder
        fields = (
            'status',
        )


class ImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'is_main':
                continue
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = ImageProduct
        fields = (
            'title',
            'is_main',
            'image',
        )
        widgets = {

        }
