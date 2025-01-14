from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .forms import *
from .models import DonneeBoeuf, Boeuf, Eleveur,Administrateur,CodeConnexionAdmin
from .serializers import DonneeBoeufSerializer, BoeufSerializer,EleveurSerializer
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.shortcuts import redirect
import random
import string
from django.core.mail import send_mail


#inscription eleveur
@api_view(['POST'])
def inscription(request):
    # Vérifier si les données sont dans la requête
    data = request.data
    
    # Vérifier que les champs requis sont présents
    if 'email' not in data or 'mot_de_passe' not in data or 'nom_complet' not in data or 'tel'not in data:
        return Response({'message': 'Tous les champs sont obligatoires.'}, status=status.HTTP_400_BAD_REQUEST)

    # Vérifier si l'eleveur  existe déjà
    if Eleveur.objects.filter(email=data['email']).exists() or Eleveur.objects.filter(tel=data['tel']).exists():
        return Response({'message': 'Cet email ou ce numéro est déjà utilisé.'}, status=status.HTTP_400_BAD_REQUEST)

    # Créer un nouvel utilisateur
    eleveur = Eleveur.objects.create(
        email=data['email'],
        tel=data['tel'],
        nom_complet=data['nom_complet'],
        mot_de_passe=data['mot_de_passe']
    )

   
    # Retourner une réponse JSON
    return Response({'message': 'Inscription réussie !'}, status=status.HTTP_201_CREATED)

#connexion eleveur

@api_view(['POST'])
def connexion_api(request):
    if request.method == 'POST':
        email = request.data.get('email')
        mot_de_passe = request.data.get('mot_de_passe')

        try:
            eleveur = Eleveur.objects.get(email=email)

            # Comparer directement les mots de passe
            if eleveur.mot_de_passe == mot_de_passe:
                return Response({
                    'message': 'Connexion réussie',
                    'email': eleveur.email,
                    'nom': eleveur.nom_complet,
                    'token': 'exemple_de_token'
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Mot de passe incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
        except Eleveur.DoesNotExist:
            return Response({'message': 'Utilisateur non trouvé'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message': 'Méthode non autorisée'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


#deconnexion eleveur
def deconnexion_eleveur(request):
    try:
        # Vérifie si l'utilisateur est connecté et supprime l'email de la session
        if 'email' in request.session:
            del request.session['email']
        # Si l'utilisateur n'est pas connecté, ne rien faire
        else:
            return JsonResponse({'message': 'Aucun utilisateur connecté'}, status=400)
        
        # Renvoie une réponse JSON confirmant la déconnexion
        return JsonResponse({'message': 'Déconnexion réussie'}, status=200)
    
    except KeyError:
        # En cas d'erreur, renvoie une réponse d'erreur
        return JsonResponse({'message': 'Erreur de déconnexion'}, status=500)



#connexion admin
@api_view(['POST'])
def connexion_admin(request):
    """Connexion de l'admin via email."""
    if 'emailAdmin' in request.session:
        return JsonResponse({'message': 'Admin déjà connecté'}, status=200)

    # Récupérer les données du formulaire
    email = request.data.get('email')
    if not email:
        return JsonResponse({'message': 'Email manquant'}, status=400)

    # Vérifier si l'email existe dans la base de données
    try:
        admini = Administrateur.objects.get(mail_admin=email)
    except Administrateur.DoesNotExist:
        return JsonResponse({'message': 'Email non valide'}, status=404)

    # Générer un code de connexion aléatoire
    code = generate_random_code()

    # Sauvegarder le code dans la base de données
    code_validation, created = CodeConnexionAdmin.objects.get_or_create(admin=admini)
    code_validation.code = code
    code_validation.save()

    # Envoyer un email avec le code
    sujet = "Code de connexion de l'administrateur"
    message = f"Bonjour/Bonsoir, Voici votre code: {code}."
    send_mail(sujet, message, 'ousbigullit@gmail.com', [email])

    # Retourner une réponse positive avec un message
    return JsonResponse({'message': 'Code envoyé par email'}, status=200)


def generate_random_code(length=6):
    """Génère un code aléatoire de 6 caractères (lettres majuscules et chiffres)."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

#code connexion admin
@api_view(['POST'])
def connexion_admin_code(request):
    # Vérifie si l'email est en session
    email = request.session.get('emailPasAdmin')

    if not email:
        return Response(
            {'message': 'Aucun email trouvé en session. Veuillez vous connecter d\'abord.'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Vérifie que la requête est POST
    if request.method == 'POST':
        # Récupère le code envoyé depuis le front
        code = request.data.get('code')

        if not code:
            return Response({'message': 'Le code est requis.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Récupère l'admin et le code de validation correspondant
            admini = Administrateur.objects.get(mail_admin=email)
            code_validation = CodeConnexionAdmin.objects.get(admin=admini)

            # Vérifie si le code est valide
            if code == code_validation.code:
                # Connexion réussie
                request.session['emailAdmin'] = email
                del request.session['emailPasAdmin']  # Supprime l'email temporaire de la session

                return Response({
                    'message': 'Connexion réussie',
                    'admin': {
                        'id': admini.id,
                        'nom': admini.nom_complet,
                        'email': admini.mail_admin
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Code invalide.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Administrateur.DoesNotExist:
            return Response({'message': 'Administrateur introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        except CodeConnexionAdmin.DoesNotExist:
            return Response({'message': 'Code de connexion introuvable.'}, status=status.HTTP_404_NOT_FOUND)

#deco admin
@api_view(['POST'])
def admin_deconnexion(request):
    """
    API pour déconnecter un administrateur.
    """
    try:
        # Vérifie si l'administrateur est connecté
        if 'emailAdmin' in request.session:
            # Supprime l'email de la session
            del request.session['emailAdmin']

            return Response(
                {'message': 'Déconnexion réussie.'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'message': 'Aucun administrateur connecté.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    except KeyError:
        return Response(
            {'message': 'Erreur lors de la déconnexion.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

#recevoir les données api
class RecevoirDonneesAPIView(APIView):
    """
    API pour recevoir et enregistrer les données des capteurs associées à un boeuf.
    """

    def post(self, request):
        try:
            # Charger les données JSON reçues
            donnees = request.data

            # Récupérer l'instance de Boeuf via l'UUID fourni
            id_boeuf = donnees.get('boeuf')
            try:
                boeuf_instance = Boeuf.objects.get(id_boeuf=id_boeuf)
            except Boeuf.DoesNotExist:
                return Response(
                    {'status': 'error', 'message': 'Boeuf non trouvé'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Créer une instance de DonneeBoeuf
            donnees_boeuf = DonneeBoeuf.objects.create(
                temp_interne=donnees.get('temperature'),
                humidite=donnees.get('humidity'),
                position=donnees.get('distance'),
                mvt_detecte=donnees.get('motionDetected'),
                boeuf=boeuf_instance
            )

            # Sérialiser les données du boeuf et des capteurs
            boeuf_serializer = BoeufSerializer(boeuf_instance)
            donnee_boeuf_serializer = DonneeBoeufSerializer(donnees_boeuf)

            return Response(
                {
                    'status': 'success',
                    'message': 'Données enregistrées avec succès',
                    'boeuf': boeuf_serializer.data,
                    'donnee_boeuf': donnee_boeuf_serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'status': 'error', 'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


#récuperer les données récentes
class DernieresDonneesAPIView(APIView):
    def get(self, request):
        # Récupérer la dernière entrée de DonneeBoeuf
        derniere_donnee = DonneeBoeuf.objects.select_related('boeuf').last()
        if derniere_donnee:
            # Préparer les données pour le frontend
            data = {
                "boeuf": {
                    "nom": derniere_donnee.boeuf.nom,
                    "date_naissance": derniere_donnee.boeuf.date_naissance,
                    "sexe": derniere_donnee.boeuf.sexe,
                    "eleveur": derniere_donnee.boeuf.eleveur
                },
                "donnee_boeuf": {
                    "temp_interne": derniere_donnee.temp_interne,
                    "humidite": derniere_donnee.humidite,
                    "position": derniere_donnee.position,
                    "mvt_detecte": derniere_donnee.mvt_detecte
                }
            }
            return Response(data, status=200)
        else:
            return Response({"message": "Aucune donnée disponible"}, status=404)


#lister la liste des éleveurs
@api_view(['GET'])
def list_eleveur(request):
    if "emailAdmin" in request.session:
        eleveurs = Eleveur.objects.all()
        serializer = EleveurSerializer(eleveurs, many=True)
        return Response(serializer.data, status=200)
    else:
        return Response({'message': 'Non autorisé. Veuillez vous connecter.'}, status=403)


#lister les boeufs
@api_view(['GET'])
def list_boeuf(request):
    if "emailAdmin" in request.session:
        boeufs = Boeuf.objects.all()
        serializer = BoeufSerializer(boeufs, many=True)
        return Response(serializer.data, status=200)
    else:
        return Response({'message': 'Non autorisé. Veuillez vous connecter.'}, status=403)


#lister donner boeufs
# API pour lister les données bœufs
@api_view(['GET'])
def list_donnees_boeuf(request):
    if "emailAdmin" in request.session:
        donnees_boeufs = DonneeBoeuf.objects.all()
        serializer = DonneeBoeufSerializer(donnees_boeufs, many=True)
        return Response(serializer.data, status=200)
    else:
        return Response({'message': 'Non autorisé. Veuillez vous connecter.'}, status=403)