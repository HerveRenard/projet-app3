from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Eleveur(models.Model):
    nom_complet = models.CharField(max_length=100, verbose_name="Nom complet")
    email = models.EmailField(unique=True)
    tel = models.CharField(max_length=15, verbose_name="Téléphone")
    mot_de_passe = models.CharField(max_length=128,default='password123')

    class Meta:
        verbose_name = "Éleveur"
        verbose_name_plural = "Éleveurs"

    def __str__(self):
        return self.nom_complet

class Boeuf(models.Model):
    SEXE_CHOICES = [
        ('M', 'Mâle'),
        ('F', 'Femelle'),
    ]

    id_boeuf = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=50)
    date_naissance = models.DateField(verbose_name="Date de naissance")
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    eleveur = models.ForeignKey(Eleveur, on_delete=models.CASCADE, related_name='boeufs')

    class Meta:
        verbose_name = "Bœuf"
        verbose_name_plural = "Bœufs"

    def __str__(self):
        return f"{self.nom} ({self.id_boeuf})"

class DonneeBoeuf(models.Model):
    boeuf = models.ForeignKey(Boeuf, on_delete=models.CASCADE, related_name='donnees')
    timestamp = models.DateTimeField(auto_now_add=True)
    humidite = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Humidité (%)"
    )
    temp_interne = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        verbose_name="Température interne (°C)"
    )
    # temp_externe = models.DecimalField(
    #     max_digits=4,
    #     decimal_places=1,
    #     verbose_name="Température externe (°C)"
    # )
    mvt_detecte = models.BooleanField(
        default=False,
        verbose_name="Mouvement détecté"
    )
    position = models.JSONField(
        help_text="Format: {'lat': float, 'lng': float}"
    )
    # freq_cardiaque = models.IntegerField(
    #     validators=[MinValueValidator(0), MaxValueValidator(300)],
    #     verbose_name="Fréquence cardiaque (bpm)"
    # )
    # freq_respiratoire = models.IntegerField(
    #     validators=[MinValueValidator(0), MaxValueValidator(100)],
    #     verbose_name="Fréquence respiratoire (rpm)"
    # )

    class Meta:
        verbose_name = "Donnée bœuf"
        verbose_name_plural = "Données bœufs"
        ordering = ['-timestamp']

    def __str__(self):
        return f"Données de {self.boeuf.nom} du {self.timestamp}"


# Modèle pour les administrateurs 
class Administrateur(models.Model):
    nom = models.CharField(max_length=255)
    mail_admin = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=128,default='password123')


# Modèle pour le code de connexion de l'administrateur
class CodeConnexionAdmin(models.Model):
    admin = models.ForeignKey('Administrateur', on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=6)