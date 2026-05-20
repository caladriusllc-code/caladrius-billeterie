from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

# Formulaire d'INSCRIPTION ORGANISATEUR 
class OrganisateurRegistrationForm(UserCreationForm): 
    
    class Meta: 
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'organisation_name', 'city', 'country']  # ✅ fields (pas field)
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
        user.role = 'organisateur'
        user.is_organisateur = True
        user.is_verified = False
        if commit:
            user.save()
        return user

# Formulaire de CONNEXION ORGANISATEUR 
class OrganisateurLoginForm(AuthenticationForm):  
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': "Nom d'utilisateur ou Email"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mot de passe'
    }))

# FORMULAIRE D'INSCRIPTION UTILISATEUR 
class UtilisateurRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 
            'email', 
            'password1', 
            'password2',
            'first_name', 
            'last_name', 
            'phone_number',
            'date_of_birth',
            'address',  
            'city', 
            'country'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder': "Nom d'utilisateur"}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nom'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control','type': 'date','placeholder': 'Date de naissance' }),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pays'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control','placeholder': 'Mot de passe'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'})
    
    def save(self, commit=True):
        """Sauvegarder l'utilisateur avec le rôle 'utilisateur'"""
        user = super().save(commit=False)
        user.role = 'utilisateur'      
        user.is_organisateur = False   
        user.is_verified = False       
        
        if commit:
            user.save()
        return user
    

# FORMULAIRE UTILISATEUR (CONNEXION)
class UtilisateurLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': "Nom d'utilisateur ou Email"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mot de passe'
    }))

