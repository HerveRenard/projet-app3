from rest_framework import serializers
from .models import DonneeBoeuf,Boeuf,Eleveur

# class DonneeBoeufSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DonneeBoeuf
#         fields = ['temp_interne','humidite','position','mvt_detecte']


class DonneeBoeufSerializer(serializers.ModelSerializer):
    boeuf_nom = serializers.CharField(source='boeuf.nom', read_only=True)

    class Meta:
        model = DonneeBoeuf
        fields = ['humidite', 'temp_interne', 'mvt_detecte', 'position']

class BoeufSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boeuf
        fields = ['nom','date_naissance','sexe','eleveur']

class EleveurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eleveur
        fields = ['nom_complet','email','tel','mot_de_passe']