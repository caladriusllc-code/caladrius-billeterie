from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser 

class login_organisateur(UserCreationForm): 

    class Meta: 
        model = CustomUser
        field = ['username', 'email', 'password1', 'password2', 'phone_number', 'organisation_name', 'city', 'country']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'organisation_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom de l'organisation"}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pays'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mot de passe'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmer mot de passe'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'organisateur'      # Définir le rôle
        user.is_organisateur = True     # Marquer comme organisateur
        user.is_verified = False        # En attente de vérification email
        if commit:
            user.save()
        return user
    
class Login_organisateur(AuthenticationForm): 
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': "Nom d'utilisateur ou Email"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mot de passe'
    }))