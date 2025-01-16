from django import forms
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from .models import Eleveur,Administrateur

# Etablir le formulaire d'inscription
class InscriptionForm(forms.Form):

    nom_complet = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'border w-full h-[70px]',
            'placeholder': 'Nom Complet',
            'id': 'name',
            'required': 'required'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'border w-full h-[70px]',
            'placeholder': 'E-mail',
            'id': 'email',
            'required': 'required'
        })
    )
    mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'border w-full h-[70px]',
            'placeholder': 'Mot de passe',
            'id': 'password',
            'required': 'required'
        })
    )
    tel = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'border w-full h-[70px]',
            'placeholder': 'Téléphone',
            'id': 'phone',
            'required': 'required'
        })
    )
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Eleveur.objects.filter(email=email).exists():
            self.add_error(self,"Cet e-mail est déjà utilisé.")
        return email
    
    def clean_tel(self):
        tel = self.cleaned_data.get('tel')
        if Eleveur.objects.filter(tel=tel).exists():
            self.add_error(self,"Ce numéro de téléphone est déjà utilisé.")
        return tel

    def save(self):
        data = self.cleaned_data
        new_eleveur = Eleveur(
            nom_complet=data['nom_complet'],
            mail_utilisateur=data['email'],
            mot_de_passe=make_password(data['mot_de_passe']),  # Hash le mot de passe
            tel = data['tel']
        )
        new_eleveur.save()
        return new_eleveur


# Etablir le formulaire de connexion
class ConnexionForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'border w-full h-[70px]',
            'placeholder': 'E-mail',
            'id': 'email',
            'required': 'required'
        })
    )
    mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'border w-full h-[70px]',
            'placeholder': 'Mot de passe',
            'id': 'password',
            'required': 'required'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        mot_de_passe = cleaned_data.get('mot_de_passe')

        #vérifier si cela existe dans la bd
        if email and password:
            eleveur = self.authentifier_eleveur(email, mot_de_passe)
            if not eleveur:
                self.add_error(self,"E-mail ou mot de passe incorrect")

        return cleaned_data

    def authentifier_eleveur(self, email, password):
        try:
            eleveur = Eleveur.objects.get(email=email)  # Recherche de l'utilisateur par email
            if check_password(password, eleveur.mot_de_passe):  # Vérifie si le mot de passe est correct
                return eleveur
            else:
                return None
        except Eleveur.DoesNotExist:
            return None

#code de connexion admin
class ConnexionCodeForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'border w-full h-[70px] md:w-[500px]',  # Classes CSS pour le style
                'placeholder': 'Entrez le code reçu ',
                'id': 'email',
                'required': 'required',
            }
        ),
        label="Code",
        max_length=6,  # Longueur maximale d'un code
        required=True,  # Le code est obligatoire
    )