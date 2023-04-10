from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, generics
from .serializers import *
import pandas as pd
from pandas import Timestamp
import os
import time
from .models import *
from django.conf import settings
import random
from scipy.stats import rankdata
from django.db.models import Sum, Avg, Min, Max
import re
from datetime import datetime,date
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from .permissions import *
from .type_role import *
import urllib.parse
from pymongo import MongoClient
import base64
from base64 import b64decode
from django.core.files.base import ContentFile
from pathlib import Path

from .utilities_functions import _list_etabs,_list_sousetabs,_list_cycles,\
_list_annee_scolaire,_list_niveaux,_list_classes,_list_matieres,_list_matieres_classe,_list_cours,_list_matricules,\
_list_hierarchies,_list_classes_examens,_list_quota_cursus,_list_type_payement_eleve,_list_type_payement_divers,\
_list_type_enseignants,_list_type_payement_enseignants,_list_type_payement_adminstaffs,_list_trimestres,_list_sequences,\
_list_specialites,_list_jours,_list_pauses,_list_tranche_horaires,_list_user_roles,_list_enseignant_matieres_specialites,\
_list_users_desactives,_list_payement_eleve,formater_heure,generate_random_string


chemin_fichier_excel = "media/"
logo_repertoire = "media/etabs/"

# class TokenViewBase(generics.GenericAPIView):
#     permission_classes = ()
#     authentication_classes = ()

#     serializer_class = None
#     _serializer_class = ""

#     www_authenticate_realm = "api"

#     def get_serializer_class(self) -> Serializer:
#         """
#         If serializer_class is set, use it directly. Otherwise get the class from settings.
#         """

#         if self.serializer_class:
#             return self.serializer_class
#         try:
#             return import_string(self._serializer_class)
#         except ImportError:
#             msg = "Could not import serializer '%s'" % self._serializer_class
#             raise ImportError(msg)

#     def get_authenticate_header(self, request: Request) -> str:
#         return '{} realm="{}"'.format(
#             AUTH_HEADER_TYPES[0],
#             self.www_authenticate_realm,
#         )

#     def post(self, request: Request, *args, **kwargs) -> Response:
#         serializer = self.get_serializer(data=request.data)

#         try:
#             serializer.is_valid(raise_exception=True)
#         except TokenError as e:
#             raise InvalidToken(e.args[0])

#         return Response(serializer.validated_data, status=status.HTTP_200_OK)

def getInfoEtab():
    info_annees = []
    activated_year = {}
    info_setabs = []
    info_cycles = []
    info_niveaux = []
    info_classes = []
    id_etab_init = 0
    # etabs = Etab.objects.all()

    annee_active = AnneeScolaire.objects.filter(is_active__in=[True])
    annees = AnneeScolaire.objects.filter()

    sousetabs = []

    if len(annee_active)>0:
        annee_active = annee_active[0]
        activated_year = {"id_annee":annee_active.id,"libelle":annee_active.libelle}

        sousetabs = annee_active.sous_etabs.all()
        if len(sousetabs)>0:
            id_etab_init = sousetabs[0].id

    # for etab in etabs:
    #     info_etabs.append({"id_etab":etab.id,"libelle":etab.libelle})
    #     sousetabs = SousEtab.objects.filter(etabs=etab)
    for s in sousetabs:
        info_setabs.append({"id_setab":s.id,"libelle":s.libelle,"id_annee":annee_active.id})
        cycles = Cycle.objects.filter(sous_etabs=s)
        for c in cycles:
            info_cycles.append({"id_cycle":c.id,"libelle":c.libelle,"id_setab":s.id})
            niveaux = Niveau.objects.filter(cycles=c)
            for n in niveaux:
                info_niveaux.append({"id_niveau":n.id,"libelle":n.libelle,"id_setab":s.id,
                    "id_cycle":c.id})
                classes = Classe.objects.filter(niveaux=n)
                for cl in classes:
                    info_classes.append({"id_classe":cl.id,"libelle":cl.libelle,"id_setab":s.id,
                    "id_cycle":c.id,"id_niveau":n.id})

    for ann in annees:
        info_annees.append({"id_annee":ann.id,"libelle":ann.libelle})

    return info_annees,activated_year,info_setabs,info_cycles,info_niveaux,info_classes,id_etab_init

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        user = User.objects.filter(username=username,is_active__in=[True])
        id_user= 0
        info_annees = []
        activated_year = {}
        info_setabs = []
        info_cycles = []
        info_niveaux = []
        info_classes = []
        id_etab_init = 0

        if len(user)>0:
            user = user[0]
            id_user = user.id
            info_annees,activated_year,info_setabs,info_cycles,info_niveaux,info_classes,id_etab_init = getInfoEtab()
            outstandingToken = OutstandingToken.objects.filter(user=user)
            print(len(outstandingToken))
            if len(outstandingToken) > 0:
                OutstandingToken.objects.filter(user=user).delete()

        # OutstandingToken.objects.filter(expires_at__lte=aware_utcnow()).delete()

        attrs = super().validate(attrs)
        return {
            "id_user": id_user,
            "info_annees":info_annees,"activated_year":activated_year,"id_etab_init":id_etab_init,"info_setabs":info_setabs,"info_cycles":info_cycles,
            "info_niveaux":info_niveaux,"info_classes":info_classes,
            # "email": self.user.email,
            # "permissions": self.user.user_permissions.values_list("codename", flat=True),
            # "groups": self.user.groups.values("name","id"),
            # "groups": self.user.groups.values_list("name",flat=True),
            **attrs,
        }

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class BlacklistTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        try:
            print("SALUT")
            refresh_token = request.data["refresh_token"]
            # print(refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()
            print("ICI ICI")
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # Response({"status":"Ok, Token deleted!"})

class UploadConfiguration(APIView):

    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            # file_name = request.FILES['file']
            # file_exists = File.objects.filter(file__iexact=file_name).exists()
            # if file_exists:
            #     File.objects.filter(file__iexact=file_name).delete()
            fichier = file_serializer.save()

            # print(fichier.file)
            # path = settings.MEDIA_ROOT
            config_file = chemin_fichier_excel + fichier.file.name
            print(config_file)

            return Response({"status":"Fichier de configuration uploade avec Success!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status":"Probleme dans l upload du fichier de configuration!"}, status=status.HTTP_400_BAD_REQUEST)

class UploadFicheProgression(APIView):

    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            # file_name = request.FILES['file']
            # file_exists = File.objects.filter(file__iexact=file_name).exists()
            # if file_exists:
            #     File.objects.filter(file__iexact=file_name).delete()
            fichier = file_serializer.save()

            # print(fichier.file)
            # path = settings.MEDIA_ROOT
            config_file = chemin_fichier_excel + fichier.file.name
            print(config_file)

            return Response({"status":"Fiche de progression uploade avec Success!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status":"Probleme dans l upload de la fiche de progression!"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

# class TokenRefreshView(TokenViewBase):
#     """
#     Takes a refresh type JSON web token and returns an access type JSON web
#     token if the refresh token is valid.
#     """

#     _serializer_class = api_settings.TOKEN_REFRESH_SERIALIZER


#     token_refresh = TokenRefreshView.as_view()

# @api_view(('GET',))
@api_view(['POST'])
def SauvegarderFicheProgression(request):
    start = time.time()
    # avant de sauvegarder une fiche de progression on supprime d'abord la précédente
    id_cours = request.data["id_cours"]
    id_sousetab = request.data["id_sousetab"]
    cours = Cours.objects.get(id=id_cours)
    sousetab = SousEtab.objects.get(id=id_sousetab)

    FicheDeProgression.objects.filter(cours__pk=id_cours).delete()

    file_name = "FicheProgression.xlsx"
    config_file_path = chemin_fichier_excel + file_name
    # print("Fiche Progression: ",config_file_path)

    classeur_excel = pd.ExcelFile(config_file_path)
    nb_sheet = len(classeur_excel.sheet_names)
    # print("Nombre de feuilles du classeur: ",nb_sheet)
    cpt_sheet = 0
    # sheet_content = pd.read_excel(config_file_path, sheet_name="A4")

    while cpt_sheet < nb_sheet:
        i = 0
        selected_sheet = classeur_excel.sheet_names[cpt_sheet]
        sheet_content = pd.read_excel(config_file_path, sheet_name=selected_sheet)
        # print(pd.isnull(sheet_content.columns[0]))
        if len(sheet_content.columns)>0 and sheet_content.columns[0]=="DATE":
            nb_ligne = len(sheet_content["DATE"])
            current_module = ""
            current_chapitre = ""
            current_lecon = ""
            while i<nb_ligne:
                date_deb = str(sheet_content["DATE"].values[i]).split("T")[0]
                current_lecon = sheet_content["UNITE D'ENSEIGNEMENT(LECON)"].values[i]
                if pd.isnull(current_lecon)==False and current_lecon.startswith("*")==False :
                    # print(current_lecon,current_lecon.startswith("*"))
                    if pd.isnull(sheet_content["MODULE"].values[i])==False:
                        current_module = sheet_content["MODULE"].values[i]
                        print(current_module)
                    if pd.isnull(sheet_content["UNITE D'APPRENTISSAGE(CHAPITRE)"].values[i])==False:
                        current_chapitre = sheet_content["UNITE D'APPRENTISSAGE(CHAPITRE)"].values[i]
                        print(current_chapitre)
                    fiche = FicheDeProgression()
                    fiche.date_deb = date_deb
                    fiche.module = current_module
                    fiche.chapitre = current_chapitre
                    fiche.lecon = current_lecon
                    fiche.save()
                    fiche.cours.add(cours)
                    fiche.sous_etabs.add(sousetab)
                    # print(fiche)


                i+=1

        cpt_sheet += 1

    end_time = time.time()
    duree = end_time-start
    print("DURATION: ", duree)
    return Response({"status":"Success !","duree":duree})

@api_view(['GET'])
def ExecuterConfiguration(request):
    start = time.time()

    file_name = "Working.xlsm"
    config_file_path = chemin_fichier_excel + file_name
    print("Config File: ",config_file_path)

    classeur_excel = pd.ExcelFile(config_file_path)
    nb_sheet = len(classeur_excel.sheet_names)
    print("Nombre de feuilles du classeur: ",nb_sheet)
    cpt_sheet = 0

    sheet_content = pd.read_excel(config_file_path, sheet_name="Start")

    annee_scolaire = AnneeScolaire()
    annee_scolaire.libelle = sheet_content[sheet_content.columns[1]].values[4]
    annee_scolaire.save()

    etab = Etab()
    etab.libelle = sheet_content[sheet_content.columns[1]].values[0]
    etab.save()

    annee_scolaire.etabs.add(etab)

    PredefinedRole(type_role="secondaire",libelle="principal",accreditation=PRINCIPAL).save()
    PredefinedRole(type_role="secondaire",libelle="censeur",accreditation=CENSEUR).save()
    PredefinedRole(type_role="secondaire",libelle="surveillant",accreditation=SURVEILLANT).save()
    PredefinedRole(type_role="secondaire",libelle="enseignant",accreditation=ENSEIGNANT).save()
    PredefinedRole(type_role="secondaire",libelle="intendant",accreditation=INTENDANT).save()

    PredefinedRole(type_role="primaire",libelle="directeur",accreditation=DIRECTEUR).save()


    while cpt_sheet < nb_sheet:
        selected_sheet = classeur_excel.sheet_names[cpt_sheet]
        if "Sous_Etab" in selected_sheet or "Sub_School" in selected_sheet:
            numero_sous_etab = selected_sheet.split("Sous_Etab")[1]
            sheet_content = pd.read_excel(config_file_path, sheet_name=selected_sheet)

            sous_etab = SousEtab()
            sous_etab.libelle = sheet_content.columns[1]
            nom_sousetab = sous_etab.libelle
            sous_etab.type_sousetab = sheet_content.columns[2]
            type_sousetab = sous_etab.type_sousetab
            sous_etab.save()
            sous_etab.etabs.add(etab)
            annee_scolaire.sous_etabs.add(sous_etab)

            nb_cycles = int(sheet_content[sheet_content.columns[1]].values[0])
            nb_classe_niveau_max = int(sheet_content[sheet_content.columns[5]].values[1])
            utilise_coef = sheet_content[sheet_content.columns[1]].values[6]

            matiere_classee_en_groupe = True if pd.isnull(sheet_content[sheet_content.columns[4]].values[1])== False and sheet_content[sheet_content.columns[4]].values[1].lower() == "oui" else False
            config_annee = ConfigAnnee()
            config_annee.appellation_apprenant = sheet_content[sheet_content.columns[1]].values[1]
            config_annee.appellation_formateur = sheet_content[sheet_content.columns[1]].values[2]
            config_annee.langue = sheet_content[sheet_content.columns[1]].values[3]
            config_annee.bulletin_base_sur = sheet_content[sheet_content.columns[1]].values[4]
            config_annee.notation_sur = sheet_content[sheet_content.columns[1]].values[5]
            config_annee.utilise_coef = sheet_content[sheet_content.columns[1]].values[6]
            config_annee.appellation_module = sheet_content[sheet_content.columns[1]].values[7]
            config_annee.abbreviation_module = sheet_content[sheet_content.columns[2]].values[7]
            config_annee.appellation_chapitre = sheet_content[sheet_content.columns[1]].values[8]
            config_annee.abbreviation_chapitre = sheet_content[sheet_content.columns[2]].values[8]
            config_annee.appellation_lecon = sheet_content[sheet_content.columns[1]].values[9]
            config_annee.abbreviation_lecon = sheet_content[sheet_content.columns[2]].values[9]
            config_annee.matricule_auto_genere = True if sheet_content[sheet_content.columns[1]].values[10].lower() == "oui" else False
            matricule_auto_genere = config_annee.matricule_auto_genere
            config_annee.has_group_matiere = matiere_classee_en_groupe
            config_annee.save()
            config_annee.sous_etabs.add(sous_etab)
            config_annee.annee_scolaires.add(annee_scolaire)

            # Le Premier cycle
            numero_cycle = 1
            cycle = Cycle()
            cycle.libelle =  "Cycle 1"
            cycle.save()
            cycle.etabs.add(etab)
            cycle.sous_etabs.add(sous_etab)

            # ligne permet de parcourir les niveaux et aussi les classes
            ligne = 12
            proceed = True
            # Ici on veut prédeterminer le nombre de lignes ou les classes sont definies
            while proceed == True:
                if pd.isnull(sheet_content['Unnamed: 3'].values[ligne])== True:
                    if pd.isnull(sheet_content['Unnamed: 3'].values[ligne+1])== False:
                        ligne += 2
                    else:
                        proceed = False
                else:
                    ligne += 1

            nb_ligne_classe = ligne -1
            indice_matiere = ligne + 2
            indice_type_personnel_administratif = ligne + 2
            indice_type_enseignant = ligne + 2

            compteur_matiere = indice_matiere
            nb_matieres = 0
            print("LES MATIERES DU SOUSETAB:")
            while pd.isnull(sheet_content['Unnamed: 8'].values[compteur_matiere])== False:
                print(sheet_content['Unnamed: 8'].values[compteur_matiere])
                matiere = Matiere()
                matiere.libelle = sheet_content['Unnamed: 8'].values[compteur_matiere]
                matiere.save()
                matiere.sous_etabs.add(sous_etab)
                compteur_matiere +=1
                nb_matieres += 1

            print("TYPE HIERARCHIE DU SOUSETAB:")
            compteur_type_personnel_administratif = indice_type_personnel_administratif
            while pd.isnull(sheet_content['Unnamed: 7'].values[compteur_type_personnel_administratif])== False:
                hierarchie = HierarchieEtab()
                hierarchie.libelle = sheet_content['Unnamed: 7'].values[compteur_type_personnel_administratif]
                hierarchie.save()
                hierarchie.sous_etabs.add(sous_etab)
                compteur_type_personnel_administratif +=1

            print("TYPE ENSEIGNANT DU SOUSETAB:")
            compteur_type_enseignant = indice_type_enseignant
            while pd.isnull(sheet_content['Unnamed: 10'].values[compteur_type_enseignant])== False:
                type_enseignant = TypeEnseignant()
                type_enseignant.libelle = sheet_content['Unnamed: 10'].values[compteur_type_enseignant]
                type_enseignant.save()
                type_enseignant.sous_etabs.add(sous_etab)

                compteur_type_enseignant +=1

            ligne = 12
            nb_niveaux = 0
            # nb_classe_niveau = 0
            # nb_classe_niveau_max = 0
            liste_groupe_matiere = []
            indice_matiere_classe = 148
            groupe = []
            while ligne <= nb_ligne_classe:
                # Ici on fait un saut supplémentaire car c'est un nouveau cycle qui commence
                if pd.isnull(sheet_content['Unnamed: 3'].values[ligne])== True and ligne < nb_ligne_classe:
                    numero_cycle += 1
                    cycle = Cycle()
                    cycle.libelle =  "Cycle "+str(numero_cycle)
                    cycle.save()
                    cycle.etabs.add(etab)
                    cycle.sous_etabs.add(sous_etab)
                    ligne += 1
                if "Niveau" in sheet_content['Unnamed: 3'].values[ligne]:
                    nb_niveaux += 1
                    niveau = Niveau()
                    niveau.libelle = sheet_content['Unnamed: 4'].values[ligne]
                    niveau.save()
                    niveau.etabs.add(etab)
                    niveau.sous_etabs.add(sous_etab)
                    niveau.cycles.add(cycle)

                    # Predetermination du nombre de classes du niveau
                    # nb_classe_niveau = 0
                    indice_local = ligne + 1
                    liste_groupe_matiere = []
                    indice_classe_niveau_courant = 0

                    # while pd.isnull(sheet_content['Unnamed: 3'].values[indice_local])== False and "_" in sheet_content['Unnamed: 3'].values[indice_local]:
                    #     nb_classe_niveau += 1
                    #     indice_local += 1

                    if nb_niveaux > 1:
                        indice_matiere_classe += nb_matieres + 1
                # C'est une classe
                else:
                    indice_classe_niveau_courant += 1
                    classe = Classe()
                    classe.libelle = sheet_content['Unnamed: 4'].values[ligne]

                    nom_fichier_classe = numero_sous_etab+"_"+classe.libelle
                    sheet_eleve = pd.read_excel(config_file_path, sheet_name=nom_fichier_classe)
                    nb_eleve_classe = len(sheet_eleve[sheet_eleve.columns[0]])

                    classe.nombre_eleves = nb_eleve_classe
                    classe.save()
                    classe.etabs.add(etab)
                    classe.sous_etabs.add(sous_etab)
                    classe.cycles.add(cycle)
                    classe.niveaux.add(niveau)
                    # On veut créer les groupes de matieres de la classe

                    indice_eleve_classe = 0
                    print(classe.libelle)
                    # Enregistrement des élèves de la classe courante
                    liste_eleve = []
                    if matricule_auto_genere == True:
                        while nb_eleve_classe > 0 :
                            enreg_eleve = False
                            if pd.isnull(sheet_eleve[sheet_eleve.columns[0]].values[indice_eleve_classe])== False:
                                # Le nom de l'eleve
                                # print(sheet_eleve[sheet_eleve.columns[0]].values[indice_eleve_classe])
                                enreg_eleve = True
                                eleve = Eleve()
                                eleve.nom = sheet_eleve[sheet_eleve.columns[0]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[1]].values[indice_eleve_classe])== False:
                                    eleve.prenom = sheet_eleve[sheet_eleve.columns[1]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[2]].values[indice_eleve_classe])== False:
                                    eleve.sexe = sheet_eleve[sheet_eleve.columns[2]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[3]].values[indice_eleve_classe])== False:
                                    # eleve.date_naissance = sheet_eleve[sheet_eleve.columns[3]].values[indice_eleve_classe]
                                    eleve.date_naissance =str(Timestamp(sheet_eleve[sheet_eleve.columns[3]].values[indice_eleve_classe])).split(" ")[0]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[4]].values[indice_eleve_classe])== False:
                                    eleve.lieu_naissance = sheet_eleve[sheet_eleve.columns[4]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[5]].values[indice_eleve_classe])== False:
                                    eleve.date_entree = sheet_eleve[sheet_eleve.columns[5]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[6]].values[indice_eleve_classe])== False:
                                    eleve.redouble = True if sheet_eleve[sheet_eleve.columns[6]].values[indice_eleve_classe] =="O" else False
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[7]].values[indice_eleve_classe])== False:
                                    eleve.nom_pere = sheet_eleve[sheet_eleve.columns[7]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[8]].values[indice_eleve_classe])== False:
                                    eleve.email_pere = sheet_eleve[sheet_eleve.columns[8]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[9]].values[indice_eleve_classe])== False:
                                    eleve.tel_pere = sheet_eleve[sheet_eleve.columns[9]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[10]].values[indice_eleve_classe])== False:
                                    eleve.nom_mere = sheet_eleve[sheet_eleve.columns[10]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[11]].values[indice_eleve_classe])== False:
                                    eleve.email_mere = sheet_eleve[sheet_eleve.columns[11]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[12]].values[indice_eleve_classe])== False:
                                    eleve.tel_mere = sheet_eleve[sheet_eleve.columns[12]].values[indice_eleve_classe]
                            else:
                                enreg_eleve = False

                            nb_eleve_classe -= 1
                            indice_eleve_classe += 1

                            if enreg_eleve == True:
                                eleve.save()
                                liste_eleve.append(eleve)
                    else:
                        while nb_eleve_classe > 0 :
                            enreg_eleve = False
                            # On verifie l'existence du nom de l'élève car plus fiable
                            if pd.isnull(sheet_eleve[sheet_eleve.columns[1]].values[indice_eleve_classe])== False:
                                # Le nom de l'eleve
                                # print(sheet_eleve[sheet_eleve.columns[0]].values[indice_eleve_classe])
                                enreg_eleve = True
                                eleve = Eleve()
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[0]].values[0])== False:
                                    eleve.matricule = sheet_eleve[sheet_eleve.columns[0]].values[0]
                                eleve.nom = sheet_eleve[sheet_eleve.columns[1]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[2]].values[indice_eleve_classe])== False:
                                    eleve.prenom = sheet_eleve[sheet_eleve.columns[2]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[3]].values[indice_eleve_classe])== False:
                                    eleve.sexe = sheet_eleve[sheet_eleve.columns[3]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[4]].values[indice_eleve_classe])== False:
                                    # eleve.date_naissance = sheet_eleve[sheet_eleve.columns[4]].values[indice_eleve_classe]
                                    eleve.date_naissance =str(Timestamp(sheet_eleve[sheet_eleve.columns[4]].values[indice_eleve_classe])).split(" ")[0]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[5]].values[indice_eleve_classe])== False:
                                    eleve.lieu_naissance = sheet_eleve[sheet_eleve.columns[5]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[6]].values[indice_eleve_classe])== False:
                                    eleve.date_entree = sheet_eleve[sheet_eleve.columns[6]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[7]].values[indice_eleve_classe])== False:
                                    eleve.redouble = True if sheet_eleve[sheet_eleve.columns[7]].values[indice_eleve_classe]=="O" else False
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[8]].values[indice_eleve_classe])== False:
                                    eleve.nom_pere = sheet_eleve[sheet_eleve.columns[8]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[9]].values[indice_eleve_classe])== False:
                                    eleve.email_pere = sheet_eleve[sheet_eleve.columns[9]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[10]].values[indice_eleve_classe])== False:
                                    eleve.tel_pere = sheet_eleve[sheet_eleve.columns[10]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[11]].values[indice_eleve_classe])== False:
                                    eleve.nom_mere = sheet_eleve[sheet_eleve.columns[11]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[12]].values[indice_eleve_classe])== False:
                                    eleve.email_mere = sheet_eleve[sheet_eleve.columns[12]].values[indice_eleve_classe]
                                if pd.isnull(sheet_eleve[sheet_eleve.columns[13]].values[indice_eleve_classe])== False:
                                    eleve.tel_mere = sheet_eleve[sheet_eleve.columns[13]].values[indice_eleve_classe]
                            else:
                                enreg_eleve = False

                            nb_eleve_classe -= 1
                            indice_eleve_classe += 1

                            if enreg_eleve == True:
                                eleve.save()
                                liste_eleve.append(eleve)

                    classe.eleves.add(*liste_eleve)

                    if matiere_classee_en_groupe:
                        # On veut lire et creer les groupe de matiere de la classe
                        if pd.isnull(sheet_content['Unnamed: 8'].values[ligne])== False:
                            # Alors la classe utilise les memes groupes que la classe précédente
                            if sheet_content['Unnamed: 8'].values[ligne].startswith("_") == False:
                                groupe = []
                                indice_local_groupe = 8
                                liste_groupe_matiere = []
                                while pd.isnull(sheet_content['Unnamed: '+str(indice_local_groupe)].values[ligne])== False:
                                    groupe = GroupeMatiere()
                                    groupe.libelle = sheet_content['Unnamed: '+str(indice_local_groupe)].values[ligne]
                                    groupe.save()
                                    groupe.classes.add(classe)
                                    liste_groupe_matiere.append(groupe)
                                    indice_local_groupe += 1
                            else:
                                liste_groupe_matiere_copy = liste_groupe_matiere
                                liste_groupe_matiere = []
                                for grp in liste_groupe_matiere_copy:
                                    groupe = GroupeMatiere()
                                    groupe.libelle = grp.libelle
                                    groupe.save()
                                    groupe.classes.add(classe)
                                    liste_groupe_matiere.append(groupe)
                                # [groupe.classes.add(classe) for groupe in liste_groupe_matiere]
                        matiere_courante = 1

                        total_coefs_groupe = 0
                        while matiere_courante <= nb_matieres:
                            coef = "_"
                            indice = indice_classe_niveau_courant+2
                            libelle_groupe_selected = sheet_content['Unnamed: '+str(indice+nb_classe_niveau_max+1)].values[indice_matiere_classe+matiere_courante]
                            global_coef = sheet_content[type_sousetab].values[indice_matiere_classe+matiere_courante]
                            if global_coef !="_":
                                coef = global_coef
                            else:
                                coef = sheet_content['Unnamed: '+str(indice)].values[indice_matiere_classe+matiere_courante]

                            if coef != "_":
                                # matiere = Matiere()
                                # matiere.libelle = sheet_content[nom_sousetab].values[indice_matiere_classe+matiere_courante]
                                # matiere.save()
                                # matiere.classes.add(classe)
                                # matiere.sous_etabs.add(sous_etab)

                                matiere = Matiere.objects.get(libelle__iexact=sheet_content[nom_sousetab].values[indice_matiere_classe+matiere_courante],sous_etabs=sous_etab)
                                matiere.classes.add(classe)
                                cours = Cours()
                                cours.description = classe.libelle+" - "+matiere.libelle
                                cours.libelle = matiere.libelle
                                cours.coef = float(coef)
                                cours.save()
                                cours.classes.add(classe)
                                cours.matieres.add(matiere)
                                total_coefs_groupe += float(coef)

                                groupe = [grp for grp in liste_groupe_matiere if grp.libelle == libelle_groupe_selected]
                                # teste si la liste n'est pas vide
                                # if groupe:
                                # groupe[0].classes.add(classe)
                                groupe[0].total_coefs += float(coef)
                                groupe[0].save()
                                # groupe[0].matieres.add(matiere)
                                groupe[0].cours.add(cours)

                            matiere_courante += 1
                        classe.total_coefs += float(total_coefs_groupe)
                        classe.save()
                    else:
                        matiere_courante = 1
                        while matiere_courante <= nb_matieres:
                            coef = "_"
                            indice = indice_classe_niveau_courant+2
                            global_coef = sheet_content[type_sousetab].values[indice_matiere_classe+matiere_courante]
                            if global_coef !="_":
                                coef = global_coef
                            else:
                                coef = sheet_content['Unnamed: '+str(indice)].values[indice_matiere_classe+matiere_courante]

                            if coef != "_":
                                # matiere = Matiere()
                                # matiere.libelle = sheet_content[nom_sousetab].values[indice_matiere_classe+matiere_courante]
                                # matiere.save()
                                # matiere.classes.add(classe)
                                # matiere.sous_etabs.add(sous_etab)
                                matiere = Matiere.objects.get(libelle__iexact=sheet_content[nom_sousetab].values[indice_matiere_classe+matiere_courante],sous_etabs=sous_etab)
                                matiere.classes.add(classe)

                                cours = Cours()
                                cours.description = classe.libelle+" - "+matiere.libelle
                                cours.libelle = matiere.libelle
                                cours.coef = float(coef) if utilise_coef != "Aucun" else 1
                                cours.save()
                                cours.classes.add(classe)
                                cours.matieres.add(matiere)

                            matiere_courante += 1
                ligne += 1
            print("nombre niveau: ", nb_niveaux)
            print("nombre classe niveau max: ", nb_classe_niveau_max)
            print("nombre matieres: ", nb_matieres)

        cpt_sheet += 1

    # PredefinedRole.create(type_role="secondaire",libelle="principal")
    # PredefinedRole.create(type_role="secondaire",libelle="censeur")
    # PredefinedRole.create(type_role="secondaire",libelle="surveillant")
    # PredefinedRole.create(type_role="secondaire",libelle="intendant")
    # PredefinedRole.create(type_role="secondaire",libelle="enseignant")

    # PredefinedRole.create(type_role="primaire",libelle="directeur")
    # PredefinedRole.create(type_role="primaire",libelle="enseignant")



    end_time = time.time()
    duree = end_time-start
    print("DURATION: ", duree)

    return Response({"status":"Success !","duree":duree})

@api_view(('GET',))
def TesterRequete(request):
    start = time.time()
    # print("**Liste SousEtab:")
    sous_etabs = SousEtab.objects.all()
    # res = [print(s) for s in sous_etabs]
    # print("**Liste Classes :")
    sous_etab = sous_etabs[0]
    # classes = sous_etab.classe_set.all()
    # [print(c.id,c.libelle) for c in classes]
    # # print(sous_etab.classe_set.all())

    # print("**Liste matieres de 6eA")
    # matieres = Matiere.objects.filter(classes__id= 1)
    # [print(m.id,m.libelle) for m in matieres]

    # print("**Liste cours de 6eA")
    # cours = Cours.objects.filter(classes__id= 1)
    # [print(c.id,c.libelle) for c in cours]

    # print("**Liste groupes matieres de 6eA")
    # groupes = GroupeMatiere.objects.filter(classes__id= 1)
    # # groupes = groupes.filter(matieres__id=1)
    # [print(g.id,g.libelle) for g in groupes]

    # print("**Liste matieres du groupe 1 de 6eA")
    # groupes = GroupeMatiere.objects.get(id=1,classes__id= 1).matieres.all()

    # # groupes = groupes.filter(matieres__id=1)
    # # [print(g.id,g.libelle) for g in groupes]
    # [print(g) for g in groupes]

    N = 50000
    print("**Generation de ",N," Nombres aléatoires:")
    random_notes = []

    # random_notes = random.sample(range(8,20),N)
    for i in range(0,N):
        score = random.randint(8,20)
        random_notes.append(score)
    # print(random_notes)
    # for i in range(0,N):
    #     b = random_notes.pop(0)
        # print(b)
    # print(random_notes)

    # coef = cours[0].coef
    # matiere = cours[0].matieres.all()[0]
    # groupe = GroupeMatiere.objects.filter(matieres = matiere)[0]
    # print("coef:",coef)
    # print("matiere:",matiere)
    # print("groupe:",groupe)
    # eleves = Classe.objects.get(id=1).eleves.all()

    trimestre = Trimestre()
    trimestre.numero = 1
    trimestre.is_active = True
    trimestre.save()

    sequence = Sequence()
    sequence.numero = 1
    sequence.is_active = True
    sequence.save()
    sequence.trimestres.add(trimestre)

    # Sequence (quota_notes,competence_visee,note_min,note_max,nombre_notes,sequences,cours)
    # sequence = Sequence()
    # sequence.save()
    # sequence.sequences.add(sequence)
    # sequence.cours.add(cours[0])


    classes = sous_etab.classe_set.all()
    # classes = sous_etab.classe_set.filter(id=1)
    for classe in classes:
        cours = Cours.objects.filter(classes= classe)
        for crs in cours:
            noteClasseMatiereSequence = InfoNoteClasseMatiereSequence()
            noteClasseMatiereSequence.save()
            noteClasseMatiereSequence.sequences.add(sequence)
            noteClasseMatiereSequence.cours.add(crs)
            noteClasseMatiereSequence.classes.add(classe)

            coef = crs.coef
            matiere = crs.matieres.all()[0]
            groupe = GroupeMatiere.objects.filter(cours = crs)[0]
            print(crs)
            eleves = Classe.objects.get(id=classe.id).eleves.all()
            for eleve in eleves:
                # print(eleve.nom)
                note = Note()
                note.eleves.add(eleve)
                note.sequences.add(sequence)
                note.cours.add(crs)
                note.groupes.add(groupe)
                score = random_notes.pop(0)
                note.score = score
                note.scorexcoef = coef * score
                note.save()

    # eleve = Eleve.objects.get(id = 1)
    # cycle = Cycle.objects.get(id = 1)
    # cycle.libelle = "Cycle 1"
    # cycle.save()
    # print("*** ",eleve, cycle)

    # res = [{"id": "1","nom": "OLEMBE","prenom": "Salomon",},{"id": "2","nom": "HAMADOU","prenom": "Pascal",},
    # {"id": "3","nom": "FONKOU","prenom": "Martin",},{"id": "4","nom": "TCHINDA","prenom": "Germain",}
    # ,{"id": "5","nom": "MBALLA","prenom": "Jean",}]

    print("***** APPEL *****");

    end_time = time.time()
    duree = end_time-start
    print("DURATION: ", duree)
    return Response({"Status:":"Success!","duree":duree})
    # return Response({"res":res, "eleve":EleveSerializer(eleve).data,"cycle":CycleSerializer(cycle).data})

# En parametre il faut id cours, id classe, id sequence, id eleve
@api_view(('GET',))
def SaveSingleNoteMatiereClasse(request):
    start = time.time()
    id_classe = 1
    id_matiere = 1
    id_cours = 1
    id_sequence = 1
    id_eleve = 2
    id_groupe = 1
    score = 16.5
    coef = 4
    scorexcoef = score * coef
    # Note.objects.all().delete()
    eleve = Eleve.objects.get(id=id_eleve)
    classe = Classe.objects.get(id=id_classe)
    groupe = GroupeMatiere.objects.get(id=id_groupe)
    sequence = Sequence.objects.get(id=id_sequence)
    cours = Cours.objects.get(id=id_cours)

    note = Note.objects.filter(eleves__pk=id_eleve,sequences__pk=1,cours__pk=1)
    if len(note) <=0:
        print(note)
        note = Note()
        note.score = score
        note.scorexcoef = scorexcoef
        note.eleves.add(eleve)
        note.cours.add(cours)
        note.sequences.add(sequence)
        note.groupes.add(groupe)
        note.save()
        print(note)
    else:
        Note.objects.filter(eleves__pk=id_eleve,sequences__pk=1,cours__pk=1).update(
            score=score,scorexcoef=scorexcoef,est_pris_en_compte=True)

    # Update des info de la sequence

    notes = Note.objects.filter(eleves__pk=id_eleve,sequences__pk=1,groupes__pk=2,est_pris_en_compte__in=[True])
    print(notes)

    courss = [note.cours.all()[0].id for note in notes]
    scores = sum([n.score for n in notes])
    scorexcoefs = sum([n.scorexcoef for n in notes])
    id_cours = [int(re.sub(r'[{}]', '', str(n.cours_id))) for n in notes]
    print("COURS:", courss)
    coefs =Cours.objects.filter(id__in=id_cours).aggregate(Sum('coef'))['coef__sum']
    # coefs =Cours.objects.filter(id__in=courss).aggregate(Sum('coef'))['coef__sum']
    print(coefs)

    groupe_update = RecapitulatifGroupeMatiereSequenceEleve.objects.filter(eleves__pk=id_eleve,sequences__pk=1,groupes__pk=2)
    if len(groupe_update) == 0:
        recap = RecapitulatifGroupeMatiereSequenceEleve()
        recap.total_coef = coefs
        recap.score = scores
        recap.moy = round(scorexcoefs/coefs,2)
        recap.nxc = scorexcoefs
        recap.eleves.add(eleve)
        recap.groupes.add(groupe)
        recap.sequences.add(sequence)
        recap.classes.add(classe)
        recap.save()
    else:
        RecapitulatifGroupeMatiereSequenceEleve.objects.filter(eleves__pk=id_eleve,sequences__pk=1,groupes__pk=2).update(
            total_coef=coefs,score=score,moy=round(scorexcoefs/coefs,2),nxc=scorexcoefs
            )
    print("moy groupe:",round(scorexcoefs/coefs,2))

    # Update des info de la sequence
    print("SEQUENCE:")
    notes = Note.objects.filter(eleves=eleve,sequences__pk=1,est_pris_en_compte__in=[True])
    # courss = [note.cours.all()[0].id for note in notes]
    print(notes)
    scores = sum([n.score for n in notes])
    scorexcoefs = sum([n.scorexcoef for n in notes])
    # id_cours = [int(re.sub(r'[{}]', '', str(n.cours_id))) for n in notes]

    coefs =Cours.objects.filter(id__in=id_cours).aggregate(Sum('coef'))['coef__sum']
    # coefs =Cours.objects.filter(id__in=courss).aggregate(Sum('coef'))['coef__sum']
    # print("coefs:",coefs)

    seq_update = ResultatEleveSequence.objects.filter(eleves__pk=id_eleve,sequences__pk=1)
    if len(seq_update) == 0:
        recap = ResultatEleveSequence()
        recap.total_coefs = coefs
        recap.total_points = scores
        recap.nxc = scorexcoefs
        recap.moyenne = round(scorexcoefs/coefs,2)
        recap.eleves.add(eleve)
        recap.sequences.add(sequence)
        recap.classes.add(classe)
        recap.save()
    else:
        ResultatEleveSequence.objects.filter(eleves__pk=id_eleve,sequences__pk=1).update(
            total_coefs=coefs,total_points=score,moyenne=round(scorexcoefs/coefs,2),nxc=scorexcoefs)
    print("moy  Seq:",round(scorexcoefs/coefs,2))


    end_time = time.time()
    duree = end_time-start
    print("DURATION: ", duree)
    return Response({"status":"Success !","duree":duree})

# En parametre il faut id cours, id classe, id sequence, id eleve
def SaveSingleNoteMatiereClasseBackend(classe,groupe,sequence,cours,eleve,score,scorexcoef):
    # start = time.time()
    # id_classe = 1
    # id_matiere = 1
    # id_cours = 1
    # id_sequence = 1
    # id_eleve = 2
    # id_groupe = 1
    # score = 16.5
    # coef = 4
    # scorexcoef = score * coef
    # # Note.objects.all().delete()
    # eleve = Eleve.objects.get(id=id_eleve)
    # classe = Classe.objects.get(id=id_classe)
    # groupe = GroupeMatiere.objects.get(id=id_groupe)
    # sequence = Sequence.objects.get(id=id_sequence)
    # cours = Cours.objects.get(id=id_cours)
    # print(score)
    note = Note.objects.filter(eleves=eleve,sequences=sequence,cours=cours)
    if len(note) <=0:
        # print(note)
        note = Note()
        note.score = score
        note.scorexcoef = scorexcoef
        note.eleves.add(eleve)
        note.cours.add(cours)
        note.sequences.add(sequence)
        note.groupes.add(groupe)
        note.save()
        # print(note)
    else:
        Note.objects.filter(eleves=eleve,sequences=sequence,cours=cours).update(
            score=score,scorexcoef=scorexcoef,est_pris_en_compte=True)

    # Update des info de la sequence

    notes = Note.objects.filter(eleves=eleve,sequences=sequence,groupes=groupe,est_pris_en_compte__in=[True])
    # print(notes)
    scores = sum([n.score for n in notes])
    scorexcoefs = sum([n.scorexcoef for n in notes])
    id_cours = [int(re.sub(r'[{}]', '', str(n.cours_id))) for n in notes]
    # id_cours = [1,2,3]
    # print("id_groupe",id_cours)

    coefs =Cours.objects.filter(id__in=id_cours).aggregate(Sum('coef'))['coef__sum']
    # coefs = 10
    # print(coefs)

    groupe_update = RecapitulatifGroupeMatiereSequenceEleve.objects.filter(eleves=eleve,sequences=sequence,groupes=groupe)
    if len(groupe_update) == 0:
        recap = RecapitulatifGroupeMatiereSequenceEleve()
        recap.total_coef = coefs
        recap.score = scores
        recap.moy = round(scorexcoefs/coefs,2)
        recap.nxc = scorexcoefs
        recap.eleves.add(eleve)
        recap.groupes.add(groupe)
        recap.sequences.add(sequence)
        recap.classes.add(classe)
        recap.save()
    else:
        RecapitulatifGroupeMatiereSequenceEleve.objects.filter(eleves=eleve,sequences=sequence,groupes=groupe).update(
            total_coef=coefs,score=scores,moy=round(scorexcoefs/coefs,2),nxc=scorexcoefs
            )
    # print("moy groupe:",round(scorexcoefs/coefs,2))
    # print("[0, 2, 3, 2] : ",rankdata([0, 2, 3, 2], method='min'))

    # Update des info de la sequence
    # print("SEQUENCE:")
    notes = Note.objects.filter(eleves=eleve,sequences=sequence,est_pris_en_compte__in=[True])
    # print(notes)
    scores = sum([n.score for n in notes])
    scorexcoefs = sum([n.scorexcoef for n in notes])
    # id_cours = [int(re.sub(r'[{}]', '', str(n.cours_id))) for n in notes]
    id_cours = [1, 2, 3, 4, 5, 6, 7, 8]
    # print("id_cours",id_cours)
    # coefs =Cours.objects.filter(id__in=id_cours).aggregate(Sum('coef'))['coef__sum']
    coefs = 20
    # print("coefs seq:",coefs,scorexcoefs,round(scorexcoefs/coefs,2))

    seq_update = ResultatEleveSequence.objects.filter(eleves=eleve,sequences=sequence)
    if len(seq_update) == 0:
        recap = ResultatEleveSequence()
        recap.total_coefs = coefs
        recap.total_points = scores
        recap.nxc = scorexcoefs
        recap.moyenne = round(scorexcoefs/coefs,2)
        recap.eleves.add(eleve)
        recap.sequences.add(sequence)
        recap.classes.add(classe)
        recap.save()
    else:
        ResultatEleveSequence.objects.filter(eleves=eleve,sequences=sequence).update(
            total_coefs=coefs,total_points=scores,moyenne=round(scorexcoefs/coefs,2),nxc=scorexcoefs)
    # print("moy  Seq:",round(scorexcoefs/coefs,2))


    # end_time = time.time()
    # duree = end_time-start
    # print("DURATION: ", duree)
    return "ok"

# En parametre il faut id cours, id classe, id sequence
@api_view(('POST',))
def SaveNoteMatiereClasse(request):
    start = time.time()
    print(request.data['id_classe'])
    id_classe = request.data['id_classe']
    id_cours = request.data['id_cours']
    id_groupe = request.data['id_groupe']
    id_sequence = request.data['id_sequence']
    coef = int(request.data['coef'])

    classe = Classe.objects.get(id=id_classe)
    groupe = GroupeMatiere.objects.get(id=id_groupe)
    sequence = Sequence.objects.get(id=id_sequence)
    cours = Cours.objects.get(id=id_cours)
    print(classe)

    # eleves = Eleve.classe_set.filter(id=id_classe)
    # eleves_id = classe.eleves_id
    eleves = classe.eleves.all()
    N =len(eleves)
    scores = []
    scorexcoefs = []
    for i in range(0,N):
        score = random.randint(8,20)
        scorexcoef = score*coef
        scores.append(score)
        scorexcoefs.append(scorexcoef)
    # print(scores,scorexcoefs)
    compteur=0
    for eleve in eleves:
        SaveSingleNoteMatiereClasseBackend(classe,groupe,sequence,cours,eleve,scores[compteur],scorexcoefs[compteur])
        # print(eleve,scores[compteur],scorexcoefs[compteur])
        compteur +=1
        # break
    # print(eleves)

    end_time = time.time()
    duree = end_time-start
    print("DURATION: ", duree)
    return Response({"status":"Success !","duree":duree})

@api_view(('POST',))
def list_note_matiere_classe(request):
    id_classe = request.data['id_classe']
    id_sequence = request.data['id_sequence']
    id_cours = request.data['id_cours']
    id_sousetab = request.data['id_sousetab']

    res_notes = []

    classe = Classe.objects.get(pk=id_classe)
    cours = Cours.objects.get(pk=id_cours)
    sequence = Sequence.objects.filter(pk=id_sequence)
    eleves = classe.eleves.all().order_by('nom','prenom')

    if sequence:
        notes = Note.objects.filter(sequences=sequence,cours=cours)
        if len(notes)>0:
            for eleve in eleves:
                note = Note.objects.filter(eleves=eleve,sequences=sequence,cours=cours)
                # note= notes.
                if len(note)>0:
                    res_notes.append({"id":el.id,"matricule":el.matricule,"nom":el.nom,"prenom":el.prenom,"score":note[0].score})
                else:
                    res_notes.append({"id":el.id,"matricule":el.matricule,"nom":el.nom,"prenom":el.prenom,"score":""})

        else:
            for el in eleves:
                res_notes.append({"id":el.id,"matricule":el.matricule,"nom":el.nom,"prenom":el.prenom,"score":""})
    else:
        for el in eleves:
            res_notes.append({"id":el.id,"matricule":el.matricule,"nom":el.nom,"prenom":el.prenom,"score":""})
    sequences = Sequence.objects.filter(sous_etabs__id=id_sousetab,is_active__in=[True])

    seqs =[]
    for seq in sequences:
        seqs.append({"id":seq.id,"libelle":seq.libelle,"date_deb":seq.date_deb,"date_fin":seq.date_fin})
    print("sequences: ", sequences)

    return Response({"sequences":seqs,"notes":res_notes})

# En parametre il faut id classe, id sequence
@api_view(('POST',))
def GenererBulletinClasse(request):
    start = time.time()

    # id_cours = [1,2,3,4,5,6,7,8]
    id_cours = []
    coefs = []
    id_sequence = 1
    id_classe = 1
    id_groupe = 2
    notation_sur = 20
    note_recap = ""
    groupe_recap = ""
    seq_recap = ""
    eleve_recap = ""
    cpt_cours = 0


    id_classe = int(request.data['id_classe'])
    id_sequence =  int(request.data['id_sequence'])

    classe = Classe.objects.get(pk=id_classe)
    sequence = Sequence.objects.get(pk=id_sequence)
    eleves = classe.eleves.all()
    groupes = GroupeMatiere.objects.filter(classes__pk=id_classe)
    matiere_listes = []

    for groupe in groupes:
        # print(re.sub(r'[{}]', '', str(groupe.matieres_id)))
        # print(groupe)
        ## matieres = groupe.matieres.all()
        cours = groupe.cours.all()
        for c in cours:
            # print(matiere.cours_set.all()[0])
            id_cours.append(c.id)
            coefs.append(c.coef)
            matiere_listes.append(cours.libelle)
        id_cours.append(-1)
    # print(id_cours,len(id_cours))
        # [print(m.cours_set.all()[0]) for m in matieres]
    # id_cours = [int(re.sub(r'[{}]', '', str(groupe.matieres_id))) for groupe in groupes]
    print(matiere_listes)


    # BulletinSeqTrimEleve
    # BulletinSeqTrimNoteRecap
    # BulletinSeqTrimGroupeNoteRecap
    # BulletinSeqTrimRecapTotal
    # for matiere in matieres du groupe
    #     on prend le recap des infos du groupe courant et rang et moy eleve
    #     on prend la note rang de l eleve dans le cours
    #     on prend aussi note_lin et max des eleves du cours
    # Note(cours=id_cours,eleves=id_eleve)

    print("RECAPITULATIFS NOTES, GROUPES, SEUENCE EN TRAITEMENT...")

    for id_c in id_cours:
        if id_c != -1:
            notes = Note.objects.filter(cours__pk=id_c,sequences__pk=id_sequence,est_pris_en_compte__in=[True])
            nb_eleves = len(notes)

            # Determiner min, max et moy par matiere et save
            min_note_matiere = notes.aggregate(Min('score'))['score__min']
            max_note_matiere = notes.aggregate(Max('score'))['score__max']
            moy_note_matiere = round(notes.aggregate(Avg('score'))['score__avg'],2)
            print(min_note_matiere,max_note_matiere,round(moy_note_matiere,2))
            note_recap += "~~"+str(coefs[cpt_cours])+"²²"+str(min_note_matiere)+"²²"+str(max_note_matiere)+"²²"+str(moy_note_matiere)+"²²"+str(matiere_listes[cpt_cours])
            note_classe_matiere = InfoNoteClasseMatiereSequence.objects.filter(cours__pk=id_c,sequences__pk=id_sequence,classes__pk=id_classe)
            cpt_cours += 1
            # cours = Cours.objects.get(pk=id_c)
            # classe = Classe.objects.get(pk=id_classe)
            # sequence = Sequence.objects.get(pk=id_sequence)
            # if len(note_classe_matiere) <= 0:
            #     note_classe_matiere = InfoNoteClasseMatiereSequence()
            #     note_classe_matiere.note_min = min_note_matiere
            #     note_classe_matiere.note_max = max_note_matiere
            #     note_classe_matiere.moy = round(moy_note_matiere,2)
            #     note_classe_matiere.save()
            #     note_classe_matiere.cours.add(cours)
            #     note_classe_matiere.classes.add(classe)
            #     note_classe_matiere.sequences.add(sequence)
            # else:
            InfoNoteClasseMatiereSequence.objects.filter(cours__pk=id_c,sequences__pk=id_sequence,classes__pk=id_classe).update(
                note_min = min_note_matiere,note_max = max_note_matiere,moy = moy_note_matiere,nb_eleves=nb_eleves)


            # Attribution des rangs aux eleves pour la matiere

            scores = [notation_sur-note.score for note in notes]
            rangs = rankdata(scores, method='min')
            # print(scores ,rangs)
            compteur = 0
            for note in notes:
                note.rang = rangs[compteur]
                note.save()
                compteur +=1
                # break
    print(note_recap)
    note_recaps = BulletinSeqTrimNoteRecap.objects.filter(classes__pk=id_classe,sequences__pk=id_sequence)
    if len(note_recaps) <= 0:
        bulletinSeqTrimNoteRecap = BulletinSeqTrimNoteRecap()
        bulletinSeqTrimNoteRecap.resultat = note_recap
        bulletinSeqTrimNoteRecap.save()
        bulletinSeqTrimNoteRecap.classes.add(classe)
        bulletinSeqTrimNoteRecap.sequences.add(sequence)
    else:
        BulletinSeqTrimNoteRecap.objects.filter(classes__pk=id_classe,sequences__pk=id_sequence).update(resultat = note_recap)
    # # Determiner rang pour les groupes et save

    for groupe in groupes:
        id_groupe = groupe.id
        recap_groupe_eleves = RecapitulatifGroupeMatiereSequenceEleve.objects.filter(groupes__pk=id_groupe,sequences__pk=id_sequence,classes_id=id_classe)
        moyennes = [notation_sur-recap.moy for recap in recap_groupe_eleves]
        rangs = rankdata(moyennes, method='min')
        # print(scores ,rangs)
        compteur = 0
        for recap in recap_groupe_eleves:
            recap.rang = rangs[compteur]
            recap.save()
            compteur +=1
        # Determiner min, max et moy  par groupe et save
        min_note_groupe = recap_groupe_eleves.aggregate(Min('moy'))['moy__min']
        max_note_groupe = recap_groupe_eleves.aggregate(Max('moy'))['moy__max']
        moy_note_groupe = round(recap_groupe_eleves.aggregate(Avg('moy'))['moy__avg'],2)
        print(min_note_groupe,max_note_groupe,moy_note_groupe)
        groupe_recap += "~~"+str(min_note_groupe)+"²²"+str(max_note_groupe)+"²²"+str(moy_note_groupe)+"²²"+str(groupe.libelle)
        # recap = RecapitulatifGroupeMatiereSequence.objects.filter(groupes__pk=id_groupe,sequences__pk=id_sequence,classes_id=id_classe)
        # if len(recap) <= 0:
        #     recap = RecapitulatifGroupeMatiereSequence()
        #     recap.note_min = min_note_groupe
        #     recap.note_max = max_note_groupe
        #     recap.moy = moy_note_groupe
        #     recap.save()
        #     recap.groupes.add(groupe)
        #     recap.classes.add(classe)
        #     recap.sequences.add(sequence)
        # else:
        #     RecapitulatifGroupeMatiereSequence.objects.filter(groupes__pk=id_groupe,sequences__pk=id_sequence,classes_id=id_classe).update(
        #         note_min = min_note_groupe,note_max = max_note_groupe,moy = moy_note_groupe)

    groupe_recaps = BulletinSeqTrimGroupeNoteRecap.objects.filter(classes__pk=id_classe,sequences__pk=id_sequence)
    if len(groupe_recaps) <= 0:
        bulletinSeqTrimGroupeNoteRecap = BulletinSeqTrimGroupeNoteRecap()
        bulletinSeqTrimGroupeNoteRecap.resultat = groupe_recap
        bulletinSeqTrimGroupeNoteRecap.save()
        bulletinSeqTrimGroupeNoteRecap.classes.add(classe)
        bulletinSeqTrimGroupeNoteRecap.sequences.add(sequence)
    else:
        BulletinSeqTrimGroupeNoteRecap.objects.filter(classes__pk=id_classe,sequences__pk=id_sequence).update(resultat = groupe_recap)
    print(groupe_recap)
    # Determiner rang pour sequence et save
    recap_sequence = ResultatEleveSequence.objects.filter(sequences__pk=id_sequence,classes_id=id_classe)
    moyennes = [notation_sur-recap.moyenne for recap in recap_sequence]
    rangs = rankdata(moyennes, method='min')
    # print(scores ,rangs)

    compteur = 0
    for recap in recap_sequence:
        recap.rang = rangs[compteur]
        recap.save()
        compteur +=1

    # Determiner min, max et moy  pour sequence et save
    min_note_seq = recap_sequence.aggregate(Min('moyenne'))['moyenne__min']
    max_note_seq = recap_sequence.aggregate(Max('moyenne'))['moyenne__max']
    moy_note_seq = round(recap_sequence.aggregate(Avg('moyenne'))['moyenne__avg'],2)
    print(min_note_seq,max_note_seq,round(moy_note_seq,2))
    middle = notation_sur/2
    nombre_moyenne = len(ResultatEleveSequence.objects.filter(sequences__pk=id_sequence,classes_id=id_classe,moyenne__gte=middle))
    nb_eleves = len(recap_sequence)
    taux_reussite_classe = nombre_moyenne * 100/nb_eleves

    seq_recap += str(min_note_seq)+"²²"+str(max_note_seq)+"²²"+str(moy_note_seq)+"²²"+str(nombre_moyenne)+"²²"+str(taux_reussite_classe)+"²²"+str(nb_eleves)
    # recap = RecapitulatifTotalSequence.objects.filter(classes_id=id_classe,sequences__pk=id_sequence)
    # if len(recap) <= 0:
    #     recap = RecapitulatifTotalSequence()
    #     recap.note_min = min_note_seq
    #     recap.note_max = max_note_seq
    #     recap.moyenne = moy_note_seq
    #     recap.nombre_moyenne = nombre_moyenne
    #     recap.taux_reussite_classe = taux_reussite_classe
    #     recap.nombre_eleves = nb_eleves
    #     recap.save()
    #     recap.classes.add(classe)
    #     recap.sequences.add(sequence)
    # else:
    #     RecapitulatifTotalSequence.objects.filter(classes_id=id_classe,sequences__pk=id_sequence).update(
    #         note_min = min_note_seq,note_max = max_note_seq,moyenne = moy_note_seq,
    #         taux_reussite_classe = taux_reussite_classe,nombre_moyenne = nombre_moyenne,nombre_eleves = nb_eleves)

    seq_recaps = BulletinSeqTrimRecapTotal.objects.filter(classes__pk=id_classe,sequences__pk=id_sequence)
    if len(seq_recaps) <= 0:
        bulletinSeqTrimRecapTotal = BulletinSeqTrimRecapTotal()
        bulletinSeqTrimRecapTotal.resultat = seq_recap
        bulletinSeqTrimRecapTotal.save()
        bulletinSeqTrimRecapTotal.classes.add(classe)
        bulletinSeqTrimRecapTotal.sequences.add(sequence)
    else:
        BulletinSeqTrimRecapTotal.objects.filter(classes__pk=id_classe,sequences__pk=id_sequence).update(resultat = seq_recap)
    print(groupe_recap)

    # Faire les copies dans la collection BulletinSequence
    # BulletinSequence
    print("INFO ELEVES EN TRAITEMENT...")
    ind_cours = 0
    debut = True
    for eleve in eleves:
        debut = True
        eleve.matricule = "HT22P200"
        eleve_recap = "~~~"+eleve.nom+"²²"+eleve.prenom+"²²"+eleve.matricule+"²²"+eleve.sexe+"²²"+str(eleve.redouble)+"²²"+str(eleve.date_naissance).split("T")[0]+"²²"+eleve.lieu_naissance+"~~~"
        ind_grp = 0
        # notes = Note.objects.filter(eleves__pk=1,sequences__pk=id_sequence,est_pris_en_compte__in=[True])
        indice_cours = 0
        for id_c in id_cours:
            if id_c != -1:
                indice_cours +=1
                # print(id_c)
                # print(notes[ind_cours].cours.filter(id=id_c))
                notes = Note.objects.filter(eleves=eleve,cours__pk=id_c,sequences__pk=id_sequence,est_pris_en_compte__in=[True])
                if debut == True:
                    eleve_recap +=str(notes[0].score)+"²²"+str(notes[0].scorexcoef)+"²²"+str(notes[0].appreciation_notes)+"²²"+str(notes[0].rang)+"²²"+str(indice_cours)
                    debut = False
                else:
                    eleve_recap +="~~"+str(notes[0].score)+"²²"+str(notes[0].scorexcoef)+"²²"+str(notes[0].appreciation_notes)+"²²"+str(notes[0].rang)+"²²"+str(indice_cours)
            else:
                recap_groupe = RecapitulatifGroupeMatiereSequenceEleve.objects.filter(eleves=eleve,sequences__pk=id_sequence,groupes__pk=groupes[ind_grp].id,classes_id=id_classe)[0]
                eleve_recap += "~~"+str(recap_groupe.total_coef)+"²²"+str(recap_groupe.score)+"²²"+str(recap_groupe.nxc)+"²²"+str(recap_groupe.rang)+"²²"+str(recap_groupe.moy)+"²²"+str(recap_groupe.appreciation_notes)+"~"
                ind_grp += 1
            ind_cours += 1
            # ResultatEleveSequence
        recap_seq = ResultatEleveSequence.objects.filter(eleves=eleve,sequences__pk=id_sequence,classes_id=id_classe)[0]
        eleve_recap += "~~"+str(recap_seq.total_points)+"²²"+str(recap_seq.total_coefs)+"²²"+str(recap_seq.moyenne)+"²²"+str(recap_seq.nxc)+"²²"+str(recap_seq.est_classe)+"²²"+str(recap_seq.rang)+"²²"+str(recap_seq.appreciation)
        note_recaps = BulletinSeqTrimEleve.objects.filter(eleves=eleve,sequences__pk=id_sequence,classes__pk=id_classe)
        if len(note_recaps) <= 0:
            bulletinSeqTrimEleve = BulletinSeqTrimEleve()
            bulletinSeqTrimEleve.resultat = eleve_recap
            bulletinSeqTrimEleve.rang = recap_seq.rang
            bulletinSeqTrimEleve.save()
            bulletinSeqTrimEleve.eleves.add(eleve)
            bulletinSeqTrimEleve.classes.add(classe)
            bulletinSeqTrimEleve.sequences.add(sequence)
        else:
            BulletinSeqTrimEleve.objects.filter(eleves=eleve,sequences__pk=id_sequence,classes__pk=id_classe).update(resultat = eleve_recap,rang = recap_seq.rang)
        print(eleve_recap)


    end_time = time.time()
    duree = end_time-start
    print("DURATION: ", duree)
    return Response({"status":"Success !","duree":duree})

# En parametre il faut id classe, id sequence ou id_trim
@api_view(['POST'])
def ImprimerBulletinClasse(request):
    start = time.time()
    # BulletinSeqTrimEleve,BulletinSeqTrimNoteRecap, BulletinSeqTrimGroupeNoteRecap, BulletinSeqTrimRecapTotal
    id_classe = int(request.data['id_classe'])
    id_sequence =  int(request.data['id_sequence'])
    print(id_classe,id_sequence)
    eleve_results = BulletinSeqTrimEleve.objects.filter(classes__pk=id_classe,sequences__pk=id_sequence).order_by('rang')
    eleve_results = eleve_results[0:10] if len(eleve_results) >0 else []
    eleve_results = BulletinSeqTrimEleveSerializer(eleve_results,many=True).data

    note_recap_results = BulletinSeqTrimNoteRecap.objects.filter(classes__pk=id_classe,sequences__pk=id_sequence)
    note_recap_results = BulletinSeqTrimNoteRecapSerializer(note_recap_results,many=True).data

    groupe_recap_results = BulletinSeqTrimGroupeNoteRecap.objects.filter(classes__pk=id_classe,sequences__pk=id_sequence)
    # groupe_recap_results = "" if len(BulletinSeqTrimGroupeNoteRecap.objects.filter(classes__pk=id_classe,sequences__pk=id_sequence))==0 else BulletinSeqTrimGroupeNoteRecap.objects.filter(classes__pk=id_classe,sequences__pk=id_sequence)[0].resultat
    groupe_recap_results = BulletinSeqTrimGroupeNoteRecapSerializer(groupe_recap_results,many=True).data

    recap_results = BulletinSeqTrimRecapTotal.objects.filter(classes__pk=id_classe,sequences__pk=id_sequence)
    # recap_results = "" if len(BulletinSeqTrimRecapTotal.objects.filter(classes__pk=id_classe,sequences__pk=id_sequence))==0 else BulletinSeqTrimRecapTotal.objects.filter(classes__pk=id_classe,sequences__pk=id_sequence)[0].resultat
    recap_results = BulletinSeqTrimRecapTotalSerializer(recap_results,many=True).data

    entete_fr = {"pays":"REPUBLIQUE DU CAMEROUN","ministere":"MINISTÈRE DES ENSEIGNEMENTS SECONDAIRE","etab":"LYCEE GENERAL LECLERC",
    "devise":"Discipline-Travail-Succès","bp":" 116","tel":"678094568","annee_scolaire":"2022/2023"}
    entete_en = {"pays":"REPUBLIC OF CAMEROON","ministere":"MINISTRY OF SECONDARY EDUCATION","etab":"GHS GENERAL LECLERC",
    "devise":"Discipline-Hardwork-Success","bp":" 116","tel":"678094568"}

    titre_bulletin = {"titre":"BULLETIN DU TRIMESTRE N°1"}

    end_time = time.time()
    duree = end_time-start
    print("DURATION: ", duree)
    return Response({"duree":duree,
                     "eleve_results":eleve_results,
                     "entete_fr":entete_fr,
                     "entete_en":entete_en,
                     "titre_bulletin":titre_bulletin,
                     "note_recap_results":note_recap_results,
                     "groupe_recap_results":groupe_recap_results,
                     "recap_results":recap_results})

#################### MATRICULE DEFINITION ####################

@api_view(['POST'])
def definition_matricule(request):
    # id_etab = request.POST.get('id_etab',None)
    # id_etab = int(id_etab) if (id_etab != "" and id_etab != None) else ""
    id_sousetab = request.data['id_sousetab']
    mat_fixed = request.data['fixe']
    mat_number_size = int(request.data['nombre'])
    mat_year = request.data['annee']
    mat_format = request.data['mat_format']
    matricule_partage = request.data['matricule_partage']
    # id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""

    print("mat_year: ",mat_year)

    # mat_fixed = request.data['mat_fixed']
    # mat_number_size = request.data['mat_number_size']
    # mat_year = request.data['mat_year']
    # mat_format = request.data['mat_format']

    # if isinstance(id_etab, int):
    #     etab = Etab.objects.get(id=id_etab)
    #     etab.same_matricule_sousetab = True
    #     etab.mat_fixed = mat_fixed
    #     etab.mat_number_size = mat_number_size
    #     etab.mat_year = mat_year
    #     etab.format_matricule = mat_format
    #     etab.save()
    # else:
    if matricule_partage == "1":
        etab = Etab.objects.all()[0]
        etab.same_matricule_sousetab = True
        etab.save()
        sousetabs = SousEtab.objects.all()
        for sousetab in sousetabs:
            config_annee = sousetab.configannee_set.all()[0]
            config_annee.mat_fixed = mat_fixed
            config_annee.mat_number_size = mat_number_size
            config_annee.mat_year = mat_year
            config_annee.format_matricule = mat_format
            config_annee.save()
            Classe.objects.filter(sous_etabs__id=sousetab.id).update(matricule_deja_attribues=False)

    else:
        sousetab = SousEtab.objects.get(id=id_sousetab)
        config_annee = sousetab.configannee_set.all()[0]
        config_annee.mat_fixed = mat_fixed
        config_annee.mat_number_size = mat_number_size
        config_annee.mat_year = mat_year
        config_annee.format_matricule = mat_format
        config_annee.save()
        Classe.objects.filter(sous_etabs__id=id_sousetab).update(matricule_deja_attribues=False)
        print(config_annee)

        etab = sousetab.etabs.all()[0]
        etab.same_matricule_sousetab = False
        etab.save()

    sousetabs = SousEtab.objects.all()
    res = _list_matricules(sousetabs)

    return Response({"status":1,"matricules":res})

def create_matricules(nb_eleves,mat_number_last=0,mat_number_size=1):
    matricules = []
    i = 0
    current_number = mat_number_last
    current_number_str = ""
    while i<nb_eleves:
        current_number += 1
        current_number_str = str(current_number)
        nb_zero_to_complete = mat_number_size - len(current_number_str)
        zeros = "0"*nb_zero_to_complete
        current_number_str = zeros+""+current_number_str
        matricules.append(current_number_str)
        # print(current_number_str)
        i +=1
    return matricules

@api_view(['POST'])
def attribution_matricule(request):
    start = time.time()
    # id_etab = request.POST.get('id_etab',None)
    # id_etab = int(id_etab) if (id_etab != "" and id_etab != None) else ""
    id_sousetab = request.data['id_sousetab']
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    # id_cycle = request.POST.get('id_cycle',None)
    # id_cycle = int(id_cycle) if (id_cycle != "" and id_cycle != None) else ""
    # id_niveau = request.POST.get('id_niveau',None)
    # id_niveau = int(id_niveau) if (id_niveau != "" and id_niveau != None) else ""
    # id_classe = request.POST.get('id_classe',None)
    # id_classe = int(id_classe) if (id_classe != "" and id_classe != None) else ""

    matricules = []
    mat_number_last = 0
    mat_number_size = 0
    sousetabs = []
    nb_eleves = 0
    passe = False
    classes = []
    s =""
    eleves = []
    elvs = ""
    format_matricule = ""
    mat_fixed = ""
    mat_year = ""

    # matricules = create_matricules(1,mat_number_last=0,mat_number_size=5)
    # matricules = create_matricules(1,mat_number_last=11,mat_number_size=5)
    # matricules = create_matricules(1,mat_number_last=123,mat_number_size=5)
    # matricules = create_matricules(1,mat_number_last=5689,mat_number_size=5)
    # if isinstance(id_etab, int):
    #     etab = Etab.objects.get(id=id_etab)
    #     sousetabs = SousEtab.objects.filter(etabs__id=id_etab)

    #     if etab.same_matricule_sousetab:
    #         classes = Classe.objects.filter(etabs__id=id_etab, matricule_deja_attribues__in=[False])
    #         nb_eleves = 0
    #         for c in classes:
    #             elvs = c.eleves.all()
    #             nb_eleves += len(elvs)
    #             # eleves.append(elvs)
    #             eleves+=elvs
    #         print("ELEVES: ",len(eleves))
    #         mat_number_last = etab.mat_number_last
    #         mat_number_size = etab.mat_number_size
    #         format_matricule = etab.format_matricule
    #         mat_fixed = etab.mat_fixed
    #         mat_year = etab.mat_year
    #         matricules = create_matricules(nb_eleves,mat_number_last=mat_number_last,mat_number_size=mat_number_size)
    #     else:


    if isinstance(id_sousetab,int):
        s = SousEtab.objects.get(id=id_sousetab)
        classes = Classe.objects.filter(sous_etabs__id=s.id, matricule_deja_attribues__in=[False])
        nb_eleves = 0
        for c in classes:
            elvs = c.eleves.all().order_by('nom','prenom')
            nb_eleves += len(elvs)
            eleves+=elvs
            config_annee = s.configannee_set.all()[0]
            mat_number_last = config_annee.mat_number_last
            mat_number_size = config_annee.mat_number_size
            format_matricule = config_annee.format_matricule
            mat_fixed = config_annee.mat_fixed
            mat_year = config_annee.mat_year
            matricules = create_matricules(nb_eleves,mat_number_last=mat_number_last,mat_number_size=mat_number_size)

    else:

        for s in sousetabs:
            classes = Classe.objects.filter(sous_etabs__id=s.id, matricule_deja_attribues__in=[False])
            nb_eleves = 0
            for c in classes:
                elvs = c.eleves.all().order_by('nom','prenom')
                nb_eleves += len(elvs)
                eleves+=elvs

            config_annee = s.configannee_set.all()[0]
            mat_number_last = config_annee.mat_number_last
            mat_number_size = config_annee.mat_number_size
            format_matricule = config_annee.format_matricule
            mat_fixed = config_annee.mat_fixed
            mat_year = config_annee.mat_year
            matricules = create_matricules(nb_eleves,mat_number_last=mat_number_last,mat_number_size=mat_number_size)

    config_annee.mat_number_last += nb_eleves
    config_annee.save()


    # elif isinstance(id_sousetab, int):
    #     classes = Classe.objects.filter(sous_etabs__id=id_sousetab, matricule_deja_attribues__in=[False])
    #     nb_eleves = 0
    #     s = SousEtab.objects.get(id=id_sousetab)
    #     passe = True
    # elif isinstance(id_cycle, int):
    #     classes = Classe.objects.filter(cycles__id=id_cycle, matricule_deja_attribues__in=[False])
    #     nb_eleves = 0
    #     s = Cycle.objects.get(id=id_cycle).sous_etabs.all()[0]
    #     passe = True
    # elif isinstance(id_niveau, int):
    #     classes = Classe.objects.filter(niveaux__id=id_niveau, matricule_deja_attribues__in=[False])
    #     nb_eleves = 0
    #     s = Niveau.objects.get(id=id_niveau).sous_etabs.all()[0]
    #     passe = True
    # elif isinstance(id_classe, int):
    #     classes = Classe.objects.filter(id=id_classe, matricule_deja_attribues__in=[False])
    #     nb_eleves = 0
    #     s = Classe.objects.get(id=id_classe).sous_etabs.all()[0]
    #     passe = True

    # if passe == True:
    #     for c in classes:
    #         elvs = c.eleves.all()
    #         nb_eleves += len(elvs)
    #         eleves+=elvs

    #     config_annee = s.configannee_set.all()[0]
    #     mat_number_last = config_annee.mat_number_last
    #     mat_number_size = config_annee.mat_number_size
    #     format_matricule = config_annee.format_matricule
    #     mat_fixed = config_annee.mat_fixed
    #     mat_year = config_annee.mat_year
    #     matricules = create_matricules(nb_eleves,mat_number_last=mat_number_last,mat_number_size=mat_number_size)
    matricules_ok =[""]*nb_eleves
    print(format_matricule)
    print(len(eleves))
    cpt = 0
    for m in matricules:
        for c in format_matricule:
            # print(c)
            if c.lower()=="f":
                matricules_ok[cpt] += mat_fixed
            elif c.lower()=="y":
                matricules_ok[cpt] += mat_year
            elif c.lower()=="n":
                matricules_ok[cpt] += m
        eleves[cpt].matricule = matricules_ok[cpt]
        eleves[cpt].save()
        cpt += 1
    for c in classes:
        c.matricule_deja_attribues = True
        c.save()

    end_time = time.time()
    duree = end_time-start
    print("DURATION: ", duree)


    # return Response({"status":"Matricules Attribués !","duree":duree})
    sousetabs = SousEtab.objects.all()
    res = _list_matricules(sousetabs)

    return Response({"status":1,"matricules":res})

@api_view(['POST'])
def list_matricules(request):
    res = []
    sousetabs = SousEtab.objects.all()
    for s in sousetabs:
        config_annee = s.configannee_set.all()[0]
        mat_fixed = config_annee.mat_fixed
        mat_number = config_annee.mat_number_size
        mat_year = config_annee.mat_year
        mat_format = config_annee.format_matricule
        result = ""
        if mat_format != "":
            for c in mat_format:
                if c=="F":
                    result += mat_fixed
                elif c=="N":
                    result += "0"*mat_number
                else:
                    result += mat_year
            res.append({"id":s.id,"libelle_etab":s.libelle,"format_matricule":result})
        else:
            res.append({"id":s.id,"libelle_etab":s.libelle,"format_matricule":""})

    return Response(res)

#################### CRUD ETAB ####################

@api_view(['GET'])
def list_etabs(request):
    # try:
    etabs = Etab.objects.all()
    etabs = EtabSerializer(etabs,many=True).data
    return Response(etabs)
    # except:
    #     return Response({"error":1})

@api_view(['POST'])
def create_etab(request):
    # try:
    # for r in request.FILES:
    #     print(r,request.FILES[r])
    photo_ = request.data['logo']
    # print(request.data['logo'])
    etab = Etab()
    etab.libelle = request.data['libelle']
    etab.date_creation = request.data['date_creation']
    etab.nom_fondateur = request.data['nom_fondateur']
    etab.localisation = request.data['localisation']
    etab.bp = request.data['bp']
    etab.email = request.data['email']
    etab.tel = request.data['tel']
    etab.devise = request.data['devise']
    # etab.logo = request.data['logo']
    etab.langue = request.data['langue']
    etab.site_web = request.data['site_web']
    etab.save()

    if (photo_ != "" and photo_ != None ):
        forma, imgstr = photo_.split(';base64,')
        ext = forma.split('/')[-1]
        print("format: ", forma, " ext: ",ext)

        photo_raw = b64decode(imgstr)
        # photo_content = ContentFile(photo_raw)
        # photo = photo_content

        file_name = str(etab.id)+"_"+etab.libelle+"."+ ext
        print("file_name ", file_name)
        # print(os.listdir())
        BASE_DIR = Path(__file__).resolve().parent.parent
        filepath = os.path.join(BASE_DIR, "media\\etabs")
        filepath+="\\"+file_name
        print(filepath)
        os.umask(0)
        with open(os.open(filepath,os.O_WRONLY|os.O_CREAT,0o777), 'wb') as fh:
            fh.write(photo_raw)
            fh.close()
        etab.logo = filepath
        etab.logo_url = logo_repertoire+file_name
        etab.save()

    etabs = _list_etabs()
    etabs = EtabSerializer(etabs,many=True).data
    return Response({"status":1,"etabs":etabs},status=status.HTTP_201_CREATED)
        # return Response({"status":"Ok, Etab Created!"}, status=status.HTTP_201_CREATED)
    # except:
    #     return Response({"error":1})

@api_view(['POST'])
def update_etab(request):
    try:
        id = int(request.data['id'])
        photo_ = request.data['logo']
        libelle = request.data['libelle']
        date_creation = request.data['date_creation']
        nom_fondateur = request.data['nom_fondateur']
        localisation = request.data['localisation']
        bp = request.data['bp']
        email = request.data['email']
        tel = request.data['tel']
        devise = request.data['devise']
        # logo = request.data['logo']
        langue = request.data['langue']
        site_web = request.data['site_web']
        print(langue)
        etab = Etab.objects.get(pk=id)
        if libelle != "" and libelle != None:
            etab.libelle = libelle
        if date_creation != "" and date_creation != None:
            etab.date_creation = date_creation
        if nom_fondateur != "" and nom_fondateur != None:
            etab.nom_fondateur = nom_fondateur
        if localisation != "" and localisation != None:
            etab.localisation = localisation
        if bp != "" and bp != None:
            etab.bp = bp
        if email != "" and email != None:
            etab.email = email
        if tel != "" and tel != None:
            etab.tel = tel
        if devise != "" and devise != None:
            etab.devise = devise
        # if logo != "" and logo != None:
        #     etab.logo = logo
        if langue != "" and langue != None:
            etab.langue = langue
        if site_web != "" and site_web != None:
            etab.site_web = site_web
        etab.save()
        print("Taille logo: ",len(photo_))
        if (photo_ != "" and photo_ != None ):
            forma, imgstr = photo_.split(';base64,')
            ext = forma.split('/')[-1]
            print("format: ", forma, " ext: ",ext)

            photo_raw = b64decode(imgstr)
            # photo_content = ContentFile(photo_raw)
            # photo = photo_content

            file_name = str(etab.id)+"_"+etab.libelle+"."+ ext
            print("file_name ", file_name)
            # print(os.listdir())
            BASE_DIR = Path(__file__).resolve().parent.parent
            filepath = os.path.join(BASE_DIR, "media\\etabs")
            filepath+="\\"+file_name
            print(filepath)
            os.umask(0)
            with open(os.open(filepath,os.O_WRONLY|os.O_CREAT,0o777), 'wb') as fh:
                fh.write(photo_raw)
                fh.close()
            etab.logo = filepath
            etab.logo_url = logo_repertoire+file_name
            etab.save()

        # Etab.objects.filter(id=id).update(libelle=libelle,date_creation=date_creation,nom_fondateur=nom_fondateur,
        #     localisation=localisation,bp=bp,email=email,tel=tel,devise=devise,logo=logo,langue=langue,site_web=site_web)

        etabs = _list_etabs()
        etabs = EtabSerializer(etabs,many=True).data
        return Response({"status":1,"etabs":etabs})
    except:
        return Response({"error":1})

@api_view(['POST'])
def delete_etab(request):
    # try:
    id = int(request.data['id'])
    file = Etab.objects.get(id=id).logo
    print(file)
    Etab.objects.filter(id=id).delete()
    if file != "" and file != None:
        if os.path.exists(str(file)):
            os.remove(str(file))
    etabs = _list_etabs()
    etabs = EtabSerializer(etabs,many=True).data
    return Response({"status":1,"etabs":etabs})
    # except:
    #     return Response({"error":1})

#################### CRUD SOUSETAB ####################

@api_view(['POST'])
def list_sousetabs(request):
    # try:
    id_annee = request.data['id_annee']
    print("id_annee: ",id_annee)
    annee = AnneeScolaire.objects.get(id=id_annee)
    sous_etabs = annee.sous_etabs.all()
    sous_etabs = SousEtabSerializer(sous_etabs,many=True).data
    return Response(sous_etabs)
    # except:
    #     return Response({"error":1})

@api_view(['POST'])
def create_sousetab(request):
    # try:
    sousetab = SousEtab()

    # id_etab = request.data.get('id_etab',None)
    # id_etab = int(id_etab) if (id_etab != "" and id_etab != None)else ""
    id_annee = request.data['id_annee']
    photo_ = request.data['logo']

    sousetab.libelle = request.data['libelle']
    sousetab.type_sousetab = request.data['type_sousetab']
    sousetab.date_creation = request.data['date_creation']
    sousetab.nom_fondateur = request.data['nom_fondateur']
    sousetab.localisation = request.data['localisation']
    sousetab.bp = request.data['bp']
    sousetab.email = request.data['email']
    sousetab.tel = request.data['tel']
    sousetab.devise = request.data['devise']
    sousetab.logo = request.data['logo']
    sousetab.langue = request.data['langue']
    sousetab.site_web = request.data['site_web']
    sousetab.save()

    annee = AnneeScolaire.objects.get(id=id_annee)
    annee_scolaire.sous_etabs.add(sousetab)

    if (photo_ != "" and photo_ != None ):
        forma, imgstr = photo_.split(';base64,')
        ext = forma.split('/')[-1]
        print("format: ", forma, " ext: ",ext)

        photo_raw = b64decode(imgstr)

        file_name = str(sousetab.id)+"_"+sousetab.libelle+"."+ ext
        print("file_name ", file_name)
        # print(os.listdir())
        BASE_DIR = Path(__file__).resolve().parent.parent
        filepath = os.path.join(BASE_DIR, "media\\etabs")
        filepath+="\\"+file_name
        print(filepath)
        os.umask(0)
        with open(os.open(filepath,os.O_WRONLY|os.O_CREAT,0o777), 'wb') as fh:
            fh.write(photo_raw)
            fh.close()
        sousetab.chemin_logo = filepath
        sousetab.logo_url = logo_repertoire+file_name
        sousetab.save()

    sous_etabs = _list_sousetabs(id_annee)
    sous_etabs = SousEtabSerializer(sous_etabs,many=True).data
    return Response({"status":1,"etabs":sous_etabs})
    # except:
    #     return Response({"error":1})

@api_view(['POST'])
def update_sousetab(request):
    # try:
    # id_etab = request.data.get('id_etab',None)
    # id_etab = int(id_etab) if (id_etab != "" and id_etab != None)else ""
    id_annee = request.data['id_annee']
    photo_ = request.data['logo']
    id = int(request.data['id'])
    libelle = request.data['libelle']
    type_sousetab = request.data['type_sousetab']
    date_creation = request.data['date_creation']
    # a = date.today()
    # print(a)
    # print(str(a).toLocaleString())
    nom_fondateur = request.data['nom_fondateur']
    localisation = request.data['localisation']
    bp = request.data['bp']
    email = request.data['email']
    tel = request.data['tel']
    devise = request.data['devise']
    langue = request.data['langue']
    site_web = request.data['site_web']

    annee = AnneeScolaire.objects.get(id=id_annee)
    sousetab = annee.sous_etabs.filter(id=id)[0]
    old_file = sousetab.chemin_logo


    print("libelle: ",libelle)
    if libelle != "" and libelle != None:
        sousetab.libelle = libelle
    if type_sousetab != "" and type_sousetab != None:
        sousetab.type_sousetab = type_sousetab
    if date_creation != "" and date_creation != None:
        sousetab.date_creation = date_creation
    if nom_fondateur != "" and nom_fondateur != None:
        sousetab.nom_fondateur = nom_fondateur
    if localisation != "" and localisation != None:
        sousetab.localisation = localisation
    if bp != "" and bp != None:
        sousetab.bp = bp
    if email != "" and email != None:
        sousetab.email = email
    if tel != "" and tel != None:
        sousetab.tel = tel
    if devise != "" and devise != None:
        sousetab.devise = devise
    if langue != "" and langue != None:
        sousetab.langue = langue
    if site_web != "" and site_web != None:
        sousetab.site_web = site_web
    sousetab.save()

    print("Taille logo: ",len(photo_))
    if (photo_ != "" and photo_ != None ):
        print("old_file: ",old_file)
        if old_file != "" and old_file != None:
            if os.path.exists(str(old_file)):
                os.remove(str(old_file))

        forma, imgstr = photo_.split(';base64,')
        ext = forma.split('/')[-1]
        print("format: ", forma, " ext: ",ext)

        photo_raw = b64decode(imgstr)
        # photo_content = ContentFile(photo_raw)
        # photo = photo_content

        file_name = str(sousetab.id)+"_"+sousetab.libelle+"."+ ext
        print("file_name ", file_name)
        # print(os.listdir())
        BASE_DIR = Path(__file__).resolve().parent.parent
        filepath = os.path.join(BASE_DIR, "media\\etabs")
        filepath+="\\"+file_name
        print(filepath)
        os.umask(0)
        with open(os.open(filepath,os.O_WRONLY|os.O_CREAT,0o777), 'wb') as fh:
            fh.write(photo_raw)
            fh.close()
        sousetab.chemin_logo = filepath
        sousetab.logo_url = logo_repertoire+file_name
        sousetab.save()

    # SousEtab.objects.filter(id=id).update(libelle=libelle,date_creation=date_creation,
    #     nom_fondateur=nom_fondateur,localisation=localisation,bp=bp,email=email,tel=tel,devise=devise,logo=logo,
    #     langue=langue,site_web=site_web)

    sous_etabs = _list_sousetabs(id_annee)
    sous_etabs = SousEtabSerializer(sous_etabs,many=True).data
    return Response({"status":1,"etabs":sous_etabs})
    # except:
    #     return Response({"error":1})

@api_view(['POST'])
def delete_sousetab(request):
    try:
        id_annee = request.data['id_annee']
        id = int(request.data['id'])
        file = SousEtab.objects.get(id=id).chemin_logo

        SousEtab.objects.filter(id=id).delete()
        print(file)
        Etab.objects.filter(id=id).delete()
        if file != "" and file != None:
            if os.path.exists(str(file)):
                os.remove(str(file))

        sous_etabs = _list_sousetabs(id_annee)
        sous_etabs = SousEtabSerializer(sous_etabs,many=True).data
        return Response({"status":1,"etabs":sous_etabs})
    except:
        return Response({"error":1})

#################### CRUD CYCLE ####################

@api_view(['POST'])
def list_cycles(request):
    id_sousetab = request.data['id_sousetab']
    print("id_sousetab: ",id_sousetab)
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    if isinstance(id_sousetab, int)==True:
        cycles = Cycle.objects.filter(sous_etabs__id=id_sousetab)
    else:
        cycles = []
    cycles = CycleSerializer(cycles,many=True).data
    return Response(cycles)

@api_view(['POST'])
def create_cycle(request):
    id_sousetab = request.data['id_sousetab']
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""

    libelle = request.data['libelle']
    code = request.data['code']

    if isinstance(id_sousetab, int)==True:
        sousetab = SousEtab.objects.get(id=id_sousetab)
        cycle = Cycle()
        cycle.libelle = libelle
        cycle.code = code
        cycle.save()
        cycle.sous_etabs.add(sousetab)

    cycles = _list_cycles(id_sousetab)
    cycles = CycleSerializer(cycles,many=True).data
    return Response({"status":1,"cycles":cycles})

@api_view(['POST'])
def update_cycle(request):

    id = int(request.data['id'])
    libelle = request.data['libelle']
    code = request.data['code']
    id_sousetab = int(request.data['id_sousetab'])

    cycle = Cycle.objects.get(id=id)
    if libelle != "" and libelle != None:
        cycle.libelle = libelle
    if code != None:
        cycle.code = code
    cycle.save()

    cycles = _list_cycles(id_sousetab)
    cycles = CycleSerializer(cycles,many=True).data
    return Response({"status":1,"cycles":cycles})

@api_view(['POST'])
def delete_cycle(request):

    id = int(request.data['id'])
    id_sousetab = int(request.data['id_sousetab'])
    Cycle.objects.filter(id=id).delete()

    cycles = _list_cycles(id_sousetab)
    cycles = CycleSerializer(cycles,many=True).data
    return Response({"status":1,"cycles":cycles})

#################### CRUD NIVEAU ####################

@api_view(['POST'])
def list_niveaux(request):
    id_sousetab = int(request.data['id_sousetab'])
    print("id_sousetab: ",id_sousetab)
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    # id_cycle = request.data['id_cycle']
    # id_cycle = int(id_cycle) if (id_cycle != "" and id_cycle != None) else ""
    # if isinstance(id_sousetab, int)==True:
    niveaux = Niveau.objects.filter(sous_etabs__id=id_sousetab)
    # else:
    #     niveaux = Niveau.objects.filter(cycles__id=id_cycle)
    res = []
    sousetab = SousEtab.objects.get(id=id_sousetab)
    cycles = sousetab.cycle_set.all()

    for c in cycles:
        niveaux = c.niveau_set.all()
        for n in niveaux:
            res.append({"id":n.id,"libelle":n.libelle,"code":n.code,"id_cycle":c.id,"libelle_cycle":c.libelle})
    return Response(res)

@api_view(['POST'])
def create_niveau(request):
    id_sousetab = request.data['id_sousetab']
    # id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    id_cycle = request.data['id_cycle']
    # id_cycle = int(id_cycle) if (id_cycle != "" and id_cycle != None) else ""

    libelle = request.data['libelle']
    code = request.data['code']

    cycle = Cycle.objects.get(id=id_cycle)
    sousetab = SousEtab.objects.get(id=id_sousetab)

    niveau = Niveau()
    niveau.libelle = libelle
    niveau.code = code
    niveau.save()
    niveau.sous_etabs.add(sousetab)
    niveau.cycles.add(cycle)

    cycles = sousetab.cycle_set.all()
    niveaux = _list_niveaux(cycles)
    # niveaux = NiveauSerializer(niveaux,many=True).data
    return Response({"status":1,"niveaux":niveaux})

@api_view(['POST'])
def update_niveau(request):

    id = int(request.data['id'])
    libelle = request.data['libelle']
    code = request.data['code']
    id_sousetab = request.data['id_sousetab']
    id_cycle = request.data['id_cycle']

    niveau = Niveau.objects.get(id=id)
    cycle = niveau.cycles.filter(id=id_cycle)
    sousetab = SousEtab.objects.get(id=id_sousetab)

    if len(cycle) >0:
        if libelle != "" and libelle != None:
            niveau.libelle = libelle
        if code != None:
            niveau.code = code
        niveau.save()
    else:
        niveau.delete()
        cycle = Cycle.objects.get(id=id_cycle)
        niveau = Niveau()
        niveau.libelle = libelle
        niveau.code = code
        niveau.save()
        niveau.sous_etabs.add(sousetab)
        niveau.cycles.add(cycle)

    cycles = sousetab.cycle_set.all()
    niveaux = _list_niveaux(cycles)
    # niveaux = NiveauSerializer(niveaux,many=True).data
    return Response({"status":1,"niveaux":niveaux})

@api_view(['POST'])
def delete_niveau(request):

    id = int(request.data['id'])
    id_sousetab = request.data['id_sousetab']
    Niveau.objects.filter(id=id).delete()

    sousetab = SousEtab.objects.get(id=id_sousetab)
    cycles = sousetab.cycle_set.all()
    niveaux = _list_niveaux(cycles)
    # niveaux = NiveauSerializer(niveaux,many=True).data
    return Response({"status":1,"niveaux":niveaux})

#################### CRUD CLASSE ####################

@api_view(['POST'])
def list_classes(request):
    id_sousetab = request.data['id_sousetab']

    classes = Classe.objects.filter(sous_etabs__id=id_sousetab)

    sousetab = SousEtab.objects.get(id=id_sousetab)
    cycles = sousetab.cycle_set.all()
    res = []
    for c in cycles:
        niveaux = c.niveau_set.all()
        for n in niveaux:
            classes = n.classe_set.all()
            for cl in classes:
                res.append({"id":cl.id,"libelle":cl.libelle,"code":cl.code,
                "id_cycle":c.id,"libelle_cycle":c.libelle,"id_niveau":n.id,"libelle_niveau":n.libelle})

    return Response(res)

@api_view(['POST'])
def create_classe(request):
    id_sousetab = request.data['id_sousetab']
    id_cycle = request.data['id_cycle']
    id_niveau = request.data['id_niveau']

    libelle = request.data['libelle']
    code = request.data['code']

    sousetab = SousEtab.objects.get(id=id_sousetab)
    cycle = Cycle.objects.get(id=id_cycle)
    niveau = Niveau.objects.get(id=id_niveau)

    classe = Classe()
    classe.libelle = libelle
    classe.code = code
    classe.save()
    classe.sous_etabs.add(sousetab)
    classe.cycles.add(cycle)
    classe.niveaux.add(niveau)

    cycles = sousetab.cycle_set.all()

    classes = _list_classes(cycles)

    return Response({"status":1,"classes":classes})

@api_view(['POST'])
def update_classe(request):

    id = int(request.data['id'])
    libelle = request.data['libelle']
    code = request.data['code']
    id_sousetab = request.data['id_sousetab']
    id_cycle = request.data['id_cycle']
    id_niveau = request.data['id_niveau']

    classe = Classe.objects.get(id=id)
    classe_a_changer= len(Classe.objects.filter(id=id,cycles__id=id_cycle,niveaux__id=id_niveau))==0
    sousetab = SousEtab.objects.get(id=id_sousetab)
    print(classe_a_changer)
    if classe_a_changer==False:
        if libelle != "" and libelle != None:
            classe.libelle = libelle
        if code != None:
            classe.code = code
        classe.save()
    else:
        classe.delete()
        cycle = Cycle.objects.get(id=id_cycle)
        niveau = Niveau.objects.get(id=id_niveau)
        classe = Classe()
        classe.libelle = libelle
        classe.code = code
        classe.save()
        classe.sous_etabs.add(sousetab)
        classe.cycles.add(cycle)
        classe.niveaux.add(niveau)

    cycles = sousetab.cycle_set.all()

    classes = _list_classes(cycles)

    return Response({"status":1,"classes":classes})

@api_view(['POST'])
def delete_classe(request):

    id = int(request.data['id'])
    id_sousetab = request.data['id_sousetab']
    Classe.objects.filter(id=id).delete()

    sousetab = SousEtab.objects.get(id=id_sousetab)
    cycles = sousetab.cycle_set.all()
    classes = _list_classes(cycles)
    # niveaux = NiveauSerializer(niveaux,many=True).data
    return Response({"status":1,"classes":classes})

#################### CRUD CLASSE D'EXAMEN ####################

@api_view(['POST'])
def set_classe_examen(request):

    id_sousetab = request.data['id_sousetab']
    id_classes = request.data['id_classes'].split("_")
    n = len(id_classes)
    print(n,id_classes)
    Classe.objects.filter(sous_etabs__id=id_sousetab).update(is_classes_examen=False)
    if n>2:
        # Enlève la virgule du début et d la fin
        id_classes = id_classes[1:-1]
        print(id_classes)
        id_classes = [int(idc) for idc in id_classes]
        Classe.objects.filter(id__in=id_classes).update(is_classes_examen=True)
    res = _list_classes_examens(id_sousetab)

    return Response({"status":1,"classes":res})

@api_view(['POST'])
def list_classes_examens(request):
    id_sousetab = request.data['id_sousetab']
    classes = Classe.objects.filter(sous_etabs__id=id_sousetab)
    res = []
    for c in classes:
        res.append({"id":c.id,"libelle":c.libelle,"is_classe_examen":c.is_classes_examen})
    return Response(res)

#################### CRUD CLASSE DE SPECIALITE ####################

@api_view(['POST'])
def create_classe_specialite(request):

    id_sousetab = request.data['id_sousetab']
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    libelle = request.data['libelle']
    code = request.data['code']
    id_classes = request.data['id_classes']

    id_classes = id_classes.split('_')
    id_classes = id_classes[1:-1]
    id_classes = [int(idc) for idc in id_classes]


    sp_classe = SpecialiteClasse()
    sp_classe.libelle = libelle
    sp_classe.code = code
    sp_classe.save()

    for idc in id_classes:
        classe = Classe.objects.get(id=idc)
        sp_classe.classes.add(classe)

    if isinstance(id_sousetab, int)==False:
        sousetabs = SousEtab.objects.all()
        for se in sousetabs:
            sp_classe.sous_etabs.add(se)
    else:
        sousetab = SousEtab.objects.get(id=id_sousetab)
        sp_classe.sous_etabs.add(sousetab)

    res = _list_specialites(id_sousetab)
    return Response({"status":1,"specialites":res})

@api_view(['POST'])
def associer_classe_specialite(request):
    id_sousetab = request.data['id_sousetab']
    id_classes = request.data['id_classes']
    id_specialite = request.data['id_specialite']
    id_classes = request.data['id_classes']
    libelle = request.data['libelle']
    code = request.data['code']

    id_classes = id_classes.split('_')
    id_classes = id_classes[1:-1]
    id_classes = [int(idc) for idc in id_classes]


    sp_classe = SpecialiteClasse.objects.get(id=id_specialite)
    sp_classe.libelle = libelle
    sp_classe.code = code
    sp_classe.save()
    old_classes = sp_classe.classes.all()

    for oc in old_classes:
        classe = Classe.objects.get(id=oc.id)
        sp_classe.classes.remove(classe)

    for idc in id_classes:
        classe = Classe.objects.get(id=idc)
        sp_classe.classes.add(classe)

    res = _list_specialites(id_sousetab)
    return Response({"status":1,"specialites":res})

@api_view(['POST'])
def delete_specialite(request):
    id = int(request.data['id'])
    id_sousetab = request.data['id_sousetab']
    SpecialiteClasse.objects.filter(id=id).delete()


    res = _list_specialites(id_sousetab)
    return Response({"status":1,"specialites":res})

@api_view(['POST'])
def list_specialites(request):
    id_sousetab = request.data['id_sousetab']
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""

    res = []

    if isinstance(id_sousetab, int)==False:
        specialites = SpecialiteClasse.objects.all()
    else:
        specialites = SpecialiteClasse.objects.filter(sous_etabs__id=id_sousetab)

    for spe in specialites:
        id_classes = ""
        libelle_classes = ""
        cpt = 0
        classes = spe.classes.all()
        for c in classes:
            cpt+=1
            if cpt < len(classes):
                id_classes +=str(c.id)+","
                libelle_classes +=str(c.libelle)+","
            else:
                id_classes +=str(c.id)
                libelle_classes +=str(c.libelle)
        res.append({"id":spe.id,"libelle":spe.libelle,"code":spe.code,"id_classes":id_classes,"libelle_classes":libelle_classes})

    # specialites = SpecialiteClasseSerializer(specialites,many=True).data
    return Response(res)

#################### CRUD MATIERE ####################

@api_view(['POST'])
def create_matiere(request):

    id_sousetab = request.data['id_sousetab']
    libelle = request.data['libelle']
    code = request.data['code']

    matiere = Matiere()
    matiere.libelle = libelle
    matiere.code = code
    matiere.save()
    sousetab = SousEtab.objects.get(id=id_sousetab)
    matiere.sous_etabs.add(sousetab)

    matieres = _list_matieres(id_sousetab)
    matieres = MatiereSerializer(matieres,many=True).data
    return Response({"status":1,"matieres":matieres})

@api_view(['POST'])
def list_matieres(request):
    # On passe id_sousetab ou id_classe en paramètre
    id_sousetab = request.data['id_sousetab']
    matieres = []

    matieres = Matiere.objects.filter(sous_etabs__id=id_sousetab)

    matieres = MatiereSerializer(matieres,many=True).data
    return Response(matieres)

@api_view(['POST'])
def update_matiere(request):

    id = int(request.data['id'])
    libelle = request.data['libelle']
    code = request.data['code']
    id_sousetab = int(request.data['id_sousetab'])

    matiere = Matiere.objects.get(id=id)
    if libelle != "" and libelle != None:
        matiere.libelle = libelle
    if code != None:
        matiere.code = code
    matiere.save()

    matieres = _list_matieres(id_sousetab)
    matieres = MatiereSerializer(matieres,many=True).data
    return Response({"status":1,"matieres":matieres})

@api_view(['POST'])
def associer_matiere_classe(request):
    id_sousetab = request.data['id_sousetab']
    id_classe = request.data['id_classe']
    id_matieres = request.data['id_matieres']
    classe = Classe.objects.get(id=id_classe)
    n = len(id_matieres)

    matieres = Matiere.objects.filter(sous_etabs__id=id_sousetab,classes__id=id_classe)
    for m in matieres:
        m.classes.remove(classe)

    if n>1:
        # Enlève la virgule du début et d la fin
        id_matieres = id_matieres[1:-1]

        id_matieres = id_matieres.split(",")
        if request.data['id_matieres'] != "":
            id_matieres = [int(id) for id in id_matieres]

        if request.data['id_matieres'] != "":
            for idm in id_matieres:
                m = Matiere.objects.get(id=idm)
                m.classes.add(classe)
    matieres = Matiere.objects.filter(sous_etabs__id=id_sousetab)
    classes = Classe.objects.filter(sous_etabs__id=id_sousetab)
    res = _list_matieres_classe(matieres,classes)
    return Response({"status":1,"matieres":res})

@api_view(['POST'])
def list_matieres_classe(request):
    id_sousetab = request.data['id_sousetab']
    res = []

    matieres = Matiere.objects.filter(sous_etabs__id=id_sousetab)
    classes = Classe.objects.filter(sous_etabs__id=id_sousetab)
    for c in classes:
        libelle_matieres = ""
        id_matieres = ""
        for m in matieres:
            classses = m.classes.all()
            if c in classses:
                libelle_matieres += m.libelle+","
                id_matieres += str(m.id)+","

        res.append({"id":c.id,"classe":c.libelle,"libelle_matieres":libelle_matieres,
            "id_matieres":id_matieres})
    matieres = Matiere.objects.filter(sous_etabs__id=id_sousetab)
    matieres = MatiereSerializer(matieres,many=True).data
    return Response({"res":res,"matieres":matieres})

@api_view(['POST'])
def delete_matiere(request):
    id_sousetab = request.data['id_sousetab']
    id_classe = request.data['id_classe']
    id = request.data['id']

    if id_sousetab != "":
        Matiere.objects.get(id=id).delete()
        matieres = _list_matieres(id_sousetab)
    else:
        classe = Classe.objects.get(id=id_classe)
        Matiere.objects.get(id=id).classes.remove(classe)
        matieres = Matiere.objects.filter(classes=classe)


    matieres = MatiereSerializer(matieres,many=True).data
    return Response({"status":1,"matieres":matieres})

#################### CRUD COURS ####################

@api_view(['POST'])
def create_cours(request):

    id_classe = request.data["id_classe"]
    libelles = request.data["libelles"]
    coefs = request.data['coefs'].split("²²")
    qhs = request.data['qhs'].split("²²")
    qas = request.data['qas'].split("²²")
    id_sousetab = request.data["id_sousetab"]
    classe = Classe.objects.get(id=id_classe)
    print(coefs)
    print(qhs)
    print(qas)
    # libelles ="12--maths²²15--info²²".split("²²")
    libelles =libelles.split("²²")
    n = len(libelles)-1
    i=0
    while i<n:
        id_matiere, libelle_m = libelles[i].split("--")
        id_matiere = int(id_matiere)
        cours = Cours.objects.filter(classes_id=id_classe,matieres__id=id_matiere)
        # print(len(cours),coefs[i]=="")
        if len(cours)>0:
            if coefs[i] !="":
                print("ici")
                cours = cours[0]
                cours.coef = float(coefs[i])
                cours.libelle = libelle_m
                cours.volume_horaire_hebdo = qhs[i]
                cours.volume_horaire_annuel = qas[i]
                # print("qas[i]: ",qas[i],cours.volume_horaire_annuel,cours.id)
                cours.save()
            else:
                # print("ici la, ",cours[0].id)
                matiere = Matiere.objects.get(id=id_matiere)
                Cours.objects.filter(classes_id=id_classe,matieres__id=id_matiere).delete()
        else:
            if coefs[i] !="":
                cours = Cours()
                cours.coef = float(coefs[i])
                cours.libelle = libelle_m
                cours.volume_horaire_hebdo = qhs[i]
                cours.volume_horaire_annuel = qas[i]
                cours.save()
                matiere = Matiere.objects.get(id=id_matiere)
                cours.classes.add(classe)
                cours.matieres.add(matiere)
                print("lala")

        i+=1

    # matiere, classes = "", []

    # if id_matiere != "" and id_matiere != None:
    #     matiere = Matiere.objects.get(id=id_matiere)
    # if id_classes != "" and id_classes != None:
    #     id_classes = id_classes.split("_")
    #     classes = [Classe.objects.get(id=int(id)) for id in id_classes]

    # for classe in classes:
    #     cr = Cours()
    #     cr.libelle = libelle
    #     cr.description = matiere.libelle+" - "+classe.libelle
    #     cr.code = code
    #     cr.coef = coef
    #     cr.volume_horaire_hebdo = quota_hebdo
    #     cr.volume_horaire_annuel = quota_annuel
    #     cr.save()
    #     cr.classes.add(classe)
    #     cr.matieres.add(matiere)
    res = _list_cours(id_sousetab)

    return Response({"status":1,"cours":res})

@api_view(['POST'])
# @permission_classes([IsAdminUser|IsPrincipalAndClassesAllowed])
def list_cours(request):
    id_sousetab = int(request.data['id_sousetab'])
    # id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    id_classe = request.data['id_classe']
    id_classe = int(id_classe) if (id_classe != "" and id_classe != None) else ""
    crs = []


    if isinstance(id_sousetab, int):
        classes = Classe.objects.filter(sous_etabs__id=id_sousetab)
        for cl in classes:
            liste_ids = ""
            liste_libelles = ""
            libelle_matieres = ""
            id_matieres = ""
            info_cours =""
            matieres = Matiere.objects.filter(classes=cl)
            cpt = 0
            nb_cours = 0
            for c in matieres:
                cpt += 1
                cr = Cours.objects.filter(matieres=c,classes=cl)
                print("len(cr): ",len(cr),cl.libelle,c.libelle)
                if len(cr)>0:
                    cr = cr[0]
                    nb_cours += 1
                    if cpt < len(matieres):
                        liste_ids +=str(cr.id)+"_"
                        liste_libelles +=str(cr.libelle)+","
                        info_cours+=str(cr.coef)+","+cr.volume_horaire_hebdo+","+cr.volume_horaire_annuel+"²²"
                    else:
                        liste_ids +=str(cr.id)
                        liste_libelles +=str(cr.libelle)
                        info_cours+=str(cr.coef)+","+cr.volume_horaire_hebdo+","+cr.volume_horaire_annuel
                else:
                    if cpt < len(matieres):
                        liste_ids +="_"
                        # liste_libelles +=","
                        info_cours+=",,²²"
                    else:
                        liste_ids +=""
                        # liste_libelles +=""
                        info_cours+=",,"

                if cpt < len(matieres):
                    id_matieres +=str(c.id)+"_"
                    libelle_matieres +=str(c.libelle)+","
                else:
                    id_matieres +=str(c.id)
                    libelle_matieres +=str(c.libelle)

            # cours = Cours.objects.filter(classes=cl)
            # cpt = 0
            # for c in cours:
            #     cpt += 1
            #     if cpt < len(cours):
            #         liste_ids +=str(c.id)+"_"
            #         liste_libelles +=str(c.libelle)+","
            #         info_cours+=str(c.coef)+","+c.volume_horaire_hebdo+","+c.volume_horaire_annuel+"²²"
            #     else:
            #         liste_ids +=str(c.id)
            #         liste_libelles +=str(c.libelle)
            #         info_cours+=str(c.coef)+","+c.volume_horaire_hebdo+","+c.volume_horaire_annuel

            # cours_libelle = [c.libelle for c in cours]
            # nb_cours_definis = len(liste_ids.split("_"))
            nb_cours_attendus = len(matieres)
            crs.append({"id":cl.id,
                "libelle_classe":cl.libelle,
                "definis":nb_cours,
                "prevus":nb_cours_attendus,
                "id_cours":liste_ids,
                "info_cours":info_cours,
                "libelle_cours":liste_libelles,
                "libelle_matieres":libelle_matieres,
                "id_matieres":id_matieres})
    # else:
    #     # Ici isinstance(id_classe, int) est True
    #     classe = Classe.objects.get(id=id_classe)
    #     liste_ids = ""
    #     liste_libelles = ""
    #     cours = Cours.objects.filter(classes=classe)
    #     matieres = Matiere.objects.filter(classes=classe)
    #     cpt = 0
    #     for c in cours:
    #         cpt += 1
    #         if cpt < len(cours):
    #             liste_ids +=str(c.id)+"_"
    #             liste_libelles +=str(c.libelle)+" , "
    #         else:
    #             liste_ids +=str(c.id)
    #             liste_libelles +=str(c.libelle)

    #     cours_libelle = [c.libelle for c in cours]
    #     nb_cours_definis = len(cours)
    #     nb_cours_attendus = len(matieres)
    #     crs.append({"id_classe":classe.id,
    #         "libelle_classe":classe.libelle,
    #         "definis":nb_cours_definis,
    #         "prevus":nb_cours_attendus,
    #         "id_cours":liste_ids,
    #         "libelle_cours":liste_libelles})

    # crs = CoursSerializer(crs,many=True).data
    return Response(crs)

@api_view(['POST'])
def delete_cours(request):
    id = int(request.data['id'])
    Cours.objects.filter(id=id).delete()

    return Response({"status":"Ok, Cours deleted!"})

#################### CRUD GROUPE ####################

@api_view(['POST'])
def create_groupe(request):

    # id_cours_to_add = request.data["id_cours_to_add"]
    # id_classe = int(request.data["id_classe"])
    # libelle = request.data['libelle']
    # code = request.data['code']
    # has_coef = request.data['has_coef']
    # groupe_de_specialite = request.data['groupe_de_specialite']
    # total_coefs = 1

    id_groupe = request.data["id_groupe"]
    id_classe = request.data["id_classe"]
    id_cours = request.data["id_cours"]
    grp_spe = request.data["grp_spe"]
    supprimer = request.data["supprimer"]
    id_sousetab = request.data["id_sousetab"]

    print(id_groupe,id_classe,id_cours,grp_spe,supprimer,id_sousetab)

    # id_cours_to_add = id_cours_to_add.split("_")
    # cours_to_add = [Cours.objects.get(id=int(id)) for id in id_cours_to_add]
    # if has_coef == "1":
    #     total_coefs = sum([c.coef for c in cours_to_add])

    # # La portion de code suivante permet d avoir les courrs de la classes qui ne sont pas dans un groupe
    # cours_in_a_groupe, cours_not_in_groupe = [], []
    # classe = Classe.objects.get(id=id_classe)
    # groupes = GroupeMatiere.objects.filter(classes=classe)
    # for g in groupes:
    #     cours = g.cours.all()
    #     for c in cours:
    #         cours_in_a_groupe.append(c)
    # # print(cours_in_a_groupe)
    # cours = Cours.objects.filter(classes=classe)
    # # print(cours)
    # for c in cours:
    #     if c not in cours_in_a_groupe:
    #         cours_not_in_groupe.append(c)
    # print(cours_not_in_groupe)
    # # print(total_coefs)
    # # print(cours_to_add)

    # groupe = GroupeMatiere()
    # groupe.libelle = libelle
    # groupe.code = code
    # groupe.total_coefs = total_coefs
    # if groupe_de_specialite == "1":
    #     groupe.groupe_matiere_de_specialite = True
    # groupe.save()
    # for c in cours_to_add:
    #     if c in cours_not_in_groupe:
    #         groupe.classes.add(classe)
    #         groupe.cours.add(c)

    return Response({"status":"Groupe Created !"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def update_groupe(request):
    id_groupe = request.data["id_groupe"]
    id_classe = request.data["id_classe"]
    id_cours = request.data["id_cours"]
    grp_spe = request.data["grp_spe"]
    supprimer = request.data["supprimer"]
    new_groupe = request.data["new_groupe"]
    id_sousetab = request.data["id_sousetab"]

    print(id_groupe,id_classe,id_cours,grp_spe,supprimer,new_groupe,id_sousetab)
    if grp_spe == "1":
        groupes = GroupeMatiere.objects.filter(classes__id=id_classe)
        for g in groupes:
            g.groupe_matiere_de_specialite = False
            g.save()
    total_coefs = 0
    # Suppression d'un groupe
    if supprimer == "1":
        print("supprimer: ",id_groupe)
        GroupeMatiere.objects.filter(id=id_groupe).delete()
    # Creation d'un nouveau groupe
    elif new_groupe != "":
        classe = Classe.objects.get(id=id_classe)
        print("new_groupe: ",new_groupe)
        groupe = GroupeMatiere()
        groupe.libelle = new_groupe
        if grp_spe == "1":
            groupe.groupe_matiere_de_specialite = True
        groupe.save()
        groupe.classes.add(classe)
        if id_cours !="_":
            id_cours = id_cours.split("_")
            id_cours = id_cours[1:-1]
            id_cours = [int(id) for id in id_cours]
            for id in id_cours:
                cours = Cours.objects.get(id=id)
                total_coefs += cours.coef
                groupe.cours.add(cours)
        groupe.total_coefs = total_coefs
        groupe.save()
    # Update d'un groupe
    else:
        print("id_cours",id_cours)
        groupe = GroupeMatiere.objects.get(id=id_groupe)
        cours_old = groupe.cours.all()
        for co in cours_old:
            groupe.cours.remove(co)
        if id_cours !="_":
            id_cours = id_cours.split("_")
            id_cours = id_cours[1:-1]
            id_cours = [int(id) for id in id_cours]
            for id in id_cours:
                cours = Cours.objects.get(id=id)
                total_coefs += cours.coef
                groupe.cours.add(cours)
        if grp_spe == "1":
            groupe.groupe_matiere_de_specialite = True
        groupe.total_coefs = total_coefs
        groupe.save()


    # id_cours_to_add = id_cours_to_add.split("_")
    # cours_to_add = [Cours.objects.get(id=int(id)) for id in id_cours_to_add]
    # if has_coef == "1":
    #     total_coefs = sum([c.coef for c in cours_to_add])

    # # La portion de code suivante permet d avoir les courrs de la classes qui ne sont pas dans un groupe
    # cours_in_a_groupe, cours_not_in_groupe = [], []
    # classe = Classe.objects.get(id=id_classe)
    # groupes = GroupeMatiere.objects.filter(classes=classe)
    # for g in groupes:
    #     cours = g.cours.all()
    #     for c in cours:
    #         cours_in_a_groupe.append(c)
    # # print(cours_in_a_groupe)
    # cours = Cours.objects.filter(classes=classe)
    # # print(cours)
    # for c in cours:
    #     if c not in cours_in_a_groupe:
    #         cours_not_in_groupe.append(c)
    # print(cours_not_in_groupe)
    # # print(total_coefs)
    # # print(cours_to_add)

    # groupe = GroupeMatiere()
    # groupe.libelle = libelle
    # groupe.code = code
    # groupe.total_coefs = total_coefs
    # if groupe_de_specialite == "1":
    #     groupe.groupe_matiere_de_specialite = True
    # groupe.save()
    # for c in cours_to_add:
    #     if c in cours_not_in_groupe:
    #         groupe.classes.add(classe)
    #         groupe.cours.add(c)

    return Response({"status":"Groupe Created !"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def list_groupes(request):
    start = time.time()

    id_sousetab = request.data['id_sousetab']
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    id_classe = request.data['id_classe']
    # id_classe = int(id_classe) if (id_classe != "" and id_classe != None) else ""

    grps =[]
    cours_in_a_groupe, cours_not_in_groupe = [], []

    if isinstance(id_sousetab, int):
        classes = Classe.objects.filter(sous_etabs__id=id_sousetab)
        for cl in classes:
            liste_ids_groupe = ""
            liste_libelles_groupe = ""
            liste_ids_cours = ""
            liste_libelles_cours = ""
            liste_ids_cours_groupe = ""
            liste_libelles_cours_groupe = ""
            # liste_ids_cours_in_groupe = ""
            # liste_libelles_cours_in_groupe = ""
            cours_in_a_groupe, cours_not_in_groupe = [], []
            nb_cours_non_groupes = 0
            groupes = GroupeMatiere.objects.filter(classes=cl)
            nb_groupes = len(groupes)
            cpt = 0
            for g in groupes:
                # print(g,cl)
                cpt += 1
                if cpt < len(groupes):
                    liste_ids_groupe +=str(g.id)+"_"
                    liste_libelles_groupe +=str(g.libelle)+","
                else:
                    liste_ids_groupe +=str(g.id)
                    liste_libelles_groupe +=str(g.libelle)

                cours = g.cours.all()
                # print(cours,cl)
                cpt2 = 0
                for c in cours:
                    cpt2 += 1
                    if cpt2 < len(cours):
                        liste_ids_cours_groupe +=str(c.id)+"_"
                        liste_libelles_cours_groupe +=str(c.libelle)+","
                    else:
                        liste_ids_cours_groupe +=str(c.id)+"²²"
                        liste_libelles_cours_groupe +=str(c.libelle)+"²²"
                    cours_in_a_groupe.append(c)


            cours = Cours.objects.filter(classes=cl)
            for c in cours:
                if c not in cours_in_a_groupe:
                    cours_not_in_groupe.append(c)
            # print(cours_not_in_groupe)
            # cpteur = 0
            # for c in cours_in_a_groupe:
            #     cpteur += 1
            #     if cpteur < len(cours_in_a_groupe):
            #         liste_ids_cours_in_groupe +=str(c.id)+"_"
            #         liste_libelles_cours_in_groupe +=str(c.libelle)+" , "
            #     else:
            #         liste_ids_cours_in_groupe +=str(c.id)
            #         liste_libelles_cours_in_groupe +=str(c.libelle)

            nb_cours_non_groupes = len(cours_not_in_groupe)
            cpt_cours = 0
            for c in cours_not_in_groupe:
                cpt_cours += 1
                if cpt_cours < len(cours_not_in_groupe):
                    liste_ids_cours +=str(c.id)+"_"
                    liste_libelles_cours +=str(c.libelle)+","
                else:
                    liste_ids_cours +=str(c.id)
                    liste_libelles_cours +=str(c.libelle)
            print(liste_libelles_cours)

            grps.append({"id":cl.id,
                "libelle_classe":cl.libelle,
                "nb_groupes":nb_groupes,
                "liste_ids_groupe":liste_ids_groupe,
                "liste_libelles_groupe":liste_libelles_groupe,
                "liste_ids_cours":liste_ids_cours,
                "liste_libelles_cours":liste_libelles_cours,
                "nb_cours_non_groupes":nb_cours_non_groupes,
                "liste_libelles_cours_groupe":liste_libelles_cours_groupe,
                "liste_ids_cours_groupe":liste_ids_cours_groupe,
                # "liste_ids_cours_in_groupe":liste_ids_cours_in_groupe,
                # "liste_libelles_cours_in_groupe":liste_libelles_cours_in_groupe,
                })
    else:
        # Ici isinstance(id_classe, int) est True
        cl = Classe.objects.get(id=id_classe)

        liste_ids_groupe = ""
        liste_libelles_groupe = ""
        liste_ids_cours = ""
        liste_libelles_cours = ""
        # liste_ids_cours_in_groupe = ""
        # liste_libelles_cours_in_groupe = ""
        cours_in_a_groupe, cours_not_in_groupe = [], []
        nb_cours_non_groupes = 0
        groupes = GroupeMatiere.objects.filter(classes=cl)
        nb_groupes = len(groupes)
        # cpt = 0
        for g in groupes:
        #     cpt += 1
        #     if cpt < len(groupes):
        #         liste_ids_groupe +=str(g.id)+"_"
        #         liste_libelles_groupe +=str(g.libelle)+" , "
        #     else:
        #         liste_ids_groupe +=str(g.id)
        #         liste_libelles_groupe +=str(g.libelle)

            cours = g.cours.all()
            for c in cours:
                cours_in_a_groupe.append(c)


        cours = Cours.objects.filter(classes=cl)
        for c in cours:
            if c not in cours_in_a_groupe:
                cours_not_in_groupe.append(c)
        # print(cours_not_in_groupe)
        # cpteur = 0
        # for c in cours_in_a_groupe:
        #     cpteur += 1
        #     if cpteur < len(cours_in_a_groupe):
        #         liste_ids_cours_in_groupe +=str(c.id)+"_"
        #         liste_libelles_cours_in_groupe +=str(c.libelle)+" , "
        #     else:
        #         liste_ids_cours_in_groupe +=str(c.id)
        #         liste_libelles_cours_in_groupe +=str(c.libelle)

        nb_cours_non_groupes = len(cours_not_in_groupe)
        cpt_cours = 0
        for c in cours_not_in_groupe:
            cpt_cours += 1
            if cpt_cours < len(cours_not_in_groupe):
                liste_ids_cours +=str(c.id)+"_"
                liste_libelles_cours +=str(c.libelle)+","
            else:
                liste_ids_cours +=str(c.id)
                liste_libelles_cours +=str(c.libelle)
        print(liste_libelles_cours)

        grps.append({"id_classe":cl.id,
                "libelle_classe":cl.libelle,
                "nb_groupes":nb_groupes,
                "liste_ids_groupe":liste_ids_groupe,
                "liste_libelles_groupe":liste_libelles_groupe,
                "liste_ids_cours":liste_ids_cours,
                "liste_libelles_cours":liste_libelles_cours,
                "nb_cours_non_groupes":nb_cours_non_groupes,
                # "liste_ids_cours_in_groupe":liste_ids_cours_in_groupe,
                # "liste_libelles_cours_in_groupe":liste_libelles_cours_in_groupe,
                })

    end_time = time.time()
    duree = end_time-start
    print("DURATION: ", duree)
    # crs = CoursSerializer(crs,many=True).data
    return Response(grps)

@api_view(['POST'])
def delete_groupe(request):
    id = int(request.data['id'])
    Groupe.objects.filter(id=id).delete()

    return Response({"status":"Ok, Groupe deleted!"})

#################### CRUD ANNEESCOLAIRE ####################

@api_view(['POST'])
def list_annee_scolaire(request):
    res = []
    annee_scolaires = AnneeScolaire.objects.all()
    for ann in annee_scolaires:
        res.append({"id":ann.id,"libelle":ann.libelle,"is_active":ann.is_active})
    print(res)
    return Response(res)

@api_view(['POST'])
def set_annee_scolaire(request):
    libelle = request.data['libelle']
    is_active = request.data['is_active']

    sousetabs = SousEtab.objects.filter()

    annee_scolaire = AnneeScolaire()
    annee_scolaire.libelle = libelle

    if is_active == "1":
        old_annees = AnneeScolaire.objects.filter()
        for old_annee in old_annees:
            old_annee.is_active = False
            old_annee.save()
        annee_scolaire.is_active = True
    else:
        annee_scolaire.is_active = False
    annee_scolaire.save()

    for s in sousetabs:
        annee_scolaire.sous_etabs.add(s)

    res = []
    annee_scolaires = AnneeScolaire.objects.all()
    for ann in annee_scolaires:
        res.append({"id":ann.id,"libelle":ann.libelle,"is_active":ann.is_active})

    return Response({"status":1,"annees":res})

@api_view(['POST'])
def delete_annee_scolaire(request):
    id = int(request.data['id'])
    AnneeScolaire.objects.filter(id=id).delete()
    res = []
    annee_scolaires = AnneeScolaire.objects.all()
    for ann in annee_scolaires:
        res.append({"id":ann.id,"libelle":ann.libelle,"is_active":ann.is_active})

    return Response({"status":1,"annees":annees})

#################### CRUD CONFIG_ANNEE ####################

@api_view(['POST'])
def list_config_annee(request):

    id_sousetab = request.data['id_sousetab']
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    # id_annee_scolaire = request.POST.get('id_annee_scolaire',None)
    # id_annee_scolaire = int(id_sousetab) if (id_annee_scolaire != "" and id_annee_scolaire != None) else ""
    res = []
    id_annee_scolaire = ""
    if isinstance(id_sousetab, int)==False:
        if isinstance(id_annee_scolaire, int)==False:
            config_annees = ConfigAnnee.objects.filter()
        else:
            config_annees = ConfigAnnee.objects.filter(annee_scolaires__id=id_annee_scolaire)
    else:
        # if isinstance(id_annee_scolaire, int)==False:
         config_annees = ConfigAnnee.objects.filter(sous_etabs__id=id_sousetab)
        # else:
        #     config_annees = ConfigAnnee.objects.filter(sous_etabs__id=id_sousetab,annee_scolaires__id=id_annee_scolaire)

    config_annees = ConfigAnneeSerializer(config_annees,many=True).data

    # for conf in config_annees:
    #     s_etab = conf.sous_etabs.all()[0]
    #     res.append({"id_sousetab":s_etab.id,"libelle_sousetab":s_etab.libelle,"libelle":conf.libelle,
    #         "langue":conf.langue,"nombre_trimestres":conf.nombre_trimestres,"nombre_sequences":conf.nombre_sequences,
    #         "duree_periode":conf.duree_periode,"has_group_matiere":conf.has_group_matiere,"utilise_coef":conf.utilise_coef,
    #         "date_deb":conf.date_deb,"date_fin":conf.date_fin})
    return Response(config_annees)

@api_view(['POST'])
def create_config_annee(request):

    id_sousetab = request.data['id_sousetab']
    operation = request.data['operation']
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    # id_annee_scolaire = request.data['id_annee']

    if operation =="create":
        config_annee = ConfigAnnee()
    else:
        config_annee = ConfigAnnee.objects.get(sous_etabs__id=id_sousetab)
    # print(" config_annee.utilise_coef: ", request.data['utilise_coef'])
    # print(" config_annee.has_group_matiere: ", request.data['has_group_matiere'])

    # if request.data['libelle']!="" and request.data['libelle']!= None:
    # config_annee.libelle = request.data['libelle']
    # if request.data['date_deb']!="" and request.data['date_deb']!= None:
    config_annee.date_deb = request.data['date_deb']
    # if request.data['date_fin']!="" and request.data['date_fin']!= None:
    config_annee.date_fin = request.data['date_fin']
    # if request.data['langue']!="" and request.data['langue']!= None:
    # config_annee.langue = request.data['langue']
    # if request.data['duree_periode']!="" and request.data['duree_periode']!= None:
    config_annee.duree_periode = request.data['duree_periode']
    if request.data['nombre_trimestres']!="" and request.data['nombre_trimestres']!= None:
        config_annee.nombre_trimestres = int(request.data['nombre_trimestres'])
    if request.data['nombre_sequences']!="" and request.data['nombre_sequences']!= None:
        config_annee.nombre_sequences = int(request.data['nombre_sequences'])
    # if request.data['notation_sur']!="" and request.data['notation_sur']!= None:
    config_annee.notation_sur = request.data['notation_sur']
    # if request.data['libelle']!="" and request.data['libelle']!= None:
    # config_annee.format_bulletin = request.data['format_bulletin']
    # if request.data['bulletin_base_sur']!="" and request.data['bulletin_base_sur']!= None:
    # config_annee.bulletin_base_sur = request.data['bulletin_base_sur']
    # if request.data['has_group_matiere']!="" and request.data['has_group_matiere']!= None:
    # config_annee.has_group_matiere = request.data['has_group_matiere']
    config_annee.has_group_matiere = True if request.data['has_group_matiere']=="true" else False
    # if request.data['appellation_bulletin']!="" and request.data['appellation_bulletin']!= None:
    config_annee.appellation_bulletin = request.data['appellation_bulletin']
    # if request.data['options_arrondi_notes']!="" and request.data['options_arrondi_notes']!= None:
    # config_annee.options_arrondi_notes = request.data['options_arrondi_notes']
    # if request.data['appellation_coef']!="" and request.data['appellation_coef']!= None:
    config_annee.appellation_coef = True if request.data['appellation_coef']=="true" else False
    # if request.data['appellation_apprenant']!="" and request.data['appellation_apprenant']!= None:
    config_annee.appellation_apprenant = request.data['appellation_apprenant']
    # if request.data['appellation_formateur']!="" and request.data['appellation_formateur']!= None:
    config_annee.appellation_formateur = request.data['appellation_formateur']
    # if request.data['appellation_sequence']!="" and request.data['appellation_sequence']!= None:
    config_annee.appellation_sequence = request.data['appellation_sequence']
    # if request.data['appellation_module']!="" and request.data['appellation_module']!= None:
    config_annee.appellation_module = request.data['appellation_module']
    # if request.data['appellation_chapitre']!="" and request.data['appellation_chapitre']!= None:
    config_annee.appellation_chapitre = request.data['appellation_chapitre']
    # if request.data['appellation_lecon']!="" and request.data['appellation_lecon']!= None:
    config_annee.appellation_lecon = request.data['appellation_lecon']
    # if request.data['abbreviation_module']!="" and request.data['abbreviation_module']!= None:
    config_annee.abbreviation_module = request.data['abbreviation_module']
    # if request.data['abbreviation_chapitre']!="" and request.data['abbreviation_chapitre']!= None:
    config_annee.abbreviation_chapitre = request.data['abbreviation_chapitre']
    # if request.data['abbreviation_lecon']!="" and request.data['abbreviation_lecon']!= None:
    config_annee.abbreviation_lecon = request.data['abbreviation_lecon']
    # if request.data['utilise_coef']!="" and request.data['utilise_coef']!= None:
    config_annee.utilise_coef = "coefficient" if request.data['utilise_coef']=="true" else "Aucun"
        # config_annee.utilise_coef = request.data['utilise_coef']
    # if request.data['matricule_auto_genere']!="" and request.data['matricule_auto_genere']!= None:
    # config_annee.matricule_auto_genere =  True if request.data['matricule_auto_genere']=="1" else False

    config_annee.save()

    # annee_scolaire = AnneeScolaire.objects.get(id=id_annee)
    # config_annee.annee_scolaires.add(annee_scolaire)

    # if isinstance(id_sousetab, int)==False:
    #     sousetabs = SousEtab.objects.all()
    #     for se in sousetabs:
    #         config_annee.sous_etabs.add(se)
    # else:
    if operation =="create":
        sousetab = SousEtab.objects.get(id=id_sousetab)
        config_annee.sous_etabs.add(sousetab)


    config_annees = ConfigAnnee.objects.filter(sous_etabs__id=id_sousetab)
    config_annees = ConfigAnneeSerializer(config_annees,many=True).data

    return Response({"status":1,"configs":config_annees})

@api_view(['POST'])
def delete_config_annee(request):
    id = int(request.data['id'])
    ConfigAnnee.objects.filter(id=id).delete()

    return Response({"status":"Ok, Config Annee deleted!"})

#################### CRUD JOUR ####################

@api_view(['POST'])
def set_jour(request):
    # id_annee_scolaire = request.data['id_annee_scolaire']
    id_sousetab = request.data['id_sousetab']
    libelle = request.data['libelle']
    heure_deb = request.data['heure_deb']
    heure_fin = request.data['heure_fin']
    numero = request.data['numero']

    # annee_scolaire = AnneeScolaire.objects.get(id=id_annee_scolaire)
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    if isinstance(id_sousetab, int):
        sousetab = SousEtab.objects.get(id=id_sousetab)
    # else:
    #     sousetabs = SousEtab.objects.all()
    #     Jour.objects.filter(annee_scolaires=annee_scolaire).delete()
    jour = Jour()
    jour.libelle = libelle
    jour.numero_jour = numero
    jour.heure_deb_cours = heure_deb
    jour.heure_fin_cours = heure_fin
    jour.save()
    jour.sous_etabs.add(sousetab)

    res = _list_jours(id_sousetab)
    return Response({"status":1,"jours":res})

@api_view(['POST'])
def update_jour(request):
    id_sousetab = request.data['id_sousetab']
    libelle = request.data['libelle']
    numero = request.data['numero']
    heure_deb = request.data['heure_deb']
    heure_fin = request.data['heure_fin']
    id = request.data['id']

    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""

    Jour.objects.filter(id=id).update(libelle=libelle,numero_jour=numero,
        heure_deb_cours=heure_deb,heure_fin_cours=heure_fin)

    res = _list_jours(id_sousetab)
    return Response({"status":1,"jours":res})

@api_view(['POST'])
def list_jours(request):

    id_sousetab = request.data['id_sousetab']
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    # id_annee_scolaire = request.POST.get('id_annee_scolaire',None)
    # id_annee_scolaire = int(id_sousetab) if (id_annee_scolaire != "" and id_annee_scolaire != None) else ""
    res = []
    if isinstance(id_sousetab, int)==False:
        # if isinstance(id_annee_scolaire, int)==False:
        jours = Jour.objects.filter().order_by('numero_jour')
        # else:
        #     jours = Jour.objects.filter(annee_scolaires__id=id_annee_scolaire)
    else:
        # if isinstance(id_annee_scolaire, int)==False:
        jours = Jour.objects.filter(sous_etabs__id=id_sousetab).order_by('numero_jour')
        # else:
        #     jours = Jour.objects.filter(sous_etabs__id=id_sousetab,annee_scolaires__id=id_annee_scolaire)


    for jour in jours:
        res.append({"id":jour.id,"libelle":jour.libelle,"numero":jour.numero_jour,"h_deb":jour.heure_deb_cours,
            "h_fin":jour.heure_fin_cours})
    return Response(res)

@api_view(['POST'])
def delete_jour(request):
    id = int(request.data['id'])
    id_sousetab = request.data['id_sousetab']
    Jour.objects.filter(id=id).delete()

    res = _list_jours(id_sousetab)
    return Response({"status":1,"jours":res})

#################### CRUD PAUSE ####################

@api_view(['POST'])
def create_pause(request):
    id_sousetab = request.data['id_sousetab']
    libelle = request.data['libelle']
    duree = request.data['duree']

    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    sousetab = SousEtab.objects.get(id=id_sousetab)
    pause = Pause()
    pause.libelle = libelle
    pause.duree = duree
    pause.save()
    pause.sous_etabs.add(sousetab)

    res = _list_pauses(id_sousetab)
    return Response({"status":1,"pauses":res})

@api_view(['POST'])
def update_pause(request):
    id_sousetab = request.data['id_sousetab']
    libelle = request.data['libelle']
    duree = request.data['duree']
    id = request.data['id']

    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    Pause.objects.filter(id=id).update(libelle=libelle, duree=duree)

    res = _list_pauses(id_sousetab)
    return Response({"status":1,"pauses":res})

@api_view(['POST'])
def list_pauses(request):
    res = []
    id_sousetab = request.data['id_sousetab']
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""

    pauses = Pause.objects.filter(sous_etabs__id=id_sousetab)

    for pause in pauses:
        res.append({"id":pause.id,"libelle":pause.libelle,"duree":pause.duree})
    return Response(res)

@api_view(['POST'])
def delete_pause(request):
    id = int(request.data['id'])
    id_sousetab = request.data['id_sousetab']
    Pause.objects.filter(id=id).delete()

    res = _list_pauses(id_sousetab)
    return Response({"status":1,"pauses":res})
#################### CRUD TRANCHE HORAIRE ####################

@api_view(['POST'])
def set_tranche_horaire(request):

    id = request.data['id']
    id_tranches_list = request.data['id_tranches_list']
    heure_list = request.data['heure_list']
    type_tranches_list = request.data['type_tranches_list']
    a_change = request.data['a_change']
    id_sousetab = request.data['id_sousetab']

    duree_periode = ConfigAnnee.objects.get(sous_etabs__id=id_sousetab).duree_periode

    print("id: ",id)
    print("id_tranches_list: ",id_tranches_list)
    print("heure_list: ",heure_list)
    type_tranches_list = type_tranches_list.split(",")
    heure_list = heure_list.split(",")
    id_tranches_list = id_tranches_list.split(",")
    print("type_tranches_list: ",type_tranches_list,a_change=='0')
    # if a_change=='2':
    #     TrancheHoraire.objects.filter(jours__id=id).delete()
    # if a_change =='1':
    if len(type_tranches_list)>0 and type_tranches_list[0]!='':
        TrancheHoraire.objects.filter(jours__id=id).delete()
        jour = Jour.objects.get(id=id)
        sousetab = SousEtab.objects.get(id=id_sousetab)


        cpt = 0
        h_fin = ""
        for id_t_tranche in type_tranches_list:
            if id_t_tranche != '':
                h_deb = formater_heure(heure_list[cpt])
                h_fin = formater_heure(heure_list[cpt+1])
                tranche = TrancheHoraire()
                tranche.heure_deb = h_deb
                tranche.heure_fin = h_fin
                print(heure_list[cpt])
                if id_t_tranche == "1":
                    print("PAUSE: ",id_tranches_list[cpt])
                    pause = Pause.objects.get(id=id_tranches_list[cpt])
                    print("c'est une pause: ",pause)
                    tranche.type_tranche = pause.id
                else:
                    tranche.type_tranche = "0"
                    print("c'est une tranche: ")
                tranche.save()
                tranche.sous_etabs.add(sousetab)
                tranche.jours.add(jour)

            cpt +=1
        if cpt >0:
            jour.heure_fin_cours = h_fin
            jour.save()

    # duree_periode = ConfigAnnee.objects.get(sous_etabs__id=id_sousetab).duree_periode
    pauses = _list_pauses(id_sousetab)
    res,duree_periode = _list_tranche_horaires(id_sousetab)
    # return Response({"status":1,"tranches":res})
    return Response({"jours":res,"duree_periode":duree_periode,"pauses":pauses})

@api_view(['POST'])
def list_tranche_horaires(request):

    start = time.time()
    id_sousetab = request.data['id_sousetab']
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    res = []
    # if isinstance(id_sousetab, int)==False:
    #     if isinstance(id_annee_scolaire, int)==False:
    #         tranches = TrancheHoraire.objects.filter()
    #     else:
    #         tranches = TrancheHoraire.objects.filter(annee_scolaires__id=id_annee_scolaire)
    # else:
    #     if isinstance(id_annee_scolaire, int)==False:
    #         tranches = TrancheHoraire.objects.filter(sous_etabs__id=id_sousetab)
    #     else:
    #         tranches = TrancheHoraire.objects.filter(annee_scolaires__id=id_annee_scolaire,sous_etabs__id=id_sousetab)

    jours = Jour.objects.filter(sous_etabs__id=id_sousetab).order_by('numero_jour')

    for jour in jours:
        tranches = TrancheHoraire.objects.filter(jours=jour).order_by('heure_deb')
        cpt = 0
        libelle_tranches = ""
        id_tranches = ""
        type_tranches = ""
        heure_deb_tranches = ""
        heure_fin_tranches = ""
        print(tranches)
        for t in tranches:
            cpt +=1
            if cpt < len(tranches):
                libelle_tranches += t.libelle+","
                type_tranches += str(t.type_tranche)+","
                heure_deb_tranches += str(t.heure_deb)+","
                heure_fin_tranches += str(t.heure_fin)+","
                if t.type_tranche != "0":
                    id_tranches += t.type_tranche+","
            else:
                libelle_tranches += t.libelle
                type_tranches += str(t.type_tranche)
                heure_deb_tranches += str(t.heure_deb)
                heure_fin_tranches += str(t.heure_fin)
                if t.type_tranche != "0":
                    id_tranches += t.type_tranche+","

        res.append({"id":jour.id,"libelle":jour.libelle,"numero":jour.numero_jour,
            "heure_deb":jour.heure_deb_cours,"heure_fin":jour.heure_fin_cours,
            "id_tranches":id_tranches,"libelle_tranches":libelle_tranches,"type_tranches":type_tranches,
            "h_debs":heure_deb_tranches,"h_fins":heure_fin_tranches})

    duree_periode = ConfigAnnee.objects.get(sous_etabs__id=id_sousetab).duree_periode
    pauses = _list_pauses(id_sousetab)
    end_time = time.time()
    duree = end_time-start
    print("DURATION: ", duree)
    return Response({"jours":res,"duree_periode":duree_periode,"pauses":pauses})

@api_view(['POST'])
def delete_tranche_horaire(request):
    id = int(request.data['id'])
    TrancheHoraire.objects.filter(id=id).delete()

    return Response({"status":"Ok, Tranche Horaire deleted!"})

#################### CRUD TRIMESTRE ####################

@api_view(['POST'])
def create_trimestre(request):

    id_sousetab = request.data['id_sousetab']
    libelle = request.data['libelle']
    date_deb = request.data['date_deb']
    date_fin = request.data['date_fin']
    is_active = request.data['is_active']
    numero = request.data['numero']

    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""

    trimestre = Trimestre()
    trimestre.libelle = libelle
    trimestre.date_deb = date_deb
    trimestre.date_fin = date_fin
    trimestre.numero = numero
    trimestre.is_active = True if is_active =="1" else False
    trimestre.save()

    if isinstance(id_sousetab,int):
        sousetab = SousEtab.objects.get(id=id_sousetab)
        trimestre.sous_etabs.add(sousetab)
    else:
        sousetabs = SousEtab.objects.filter()
        for sousetab in sousetabs:
            trimestre.sous_etabs.add(sousetab)

    res = _list_trimestres(id_sousetab)
    return Response({"status":1,"trimestres":res})

@api_view(['POST'])
def list_trimestres(request):

    id_sousetab = request.data['id_sousetab']
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    res = []
    trimestres = []
    if isinstance(id_sousetab,int):
        trimestres = Trimestre.objects.filter(sous_etabs__id=id_sousetab).order_by('date_deb')
    else:
        trimestres = Trimestre.objects.all().order_by('date_deb')

    for trimestre in trimestres:
        liste_sous_etabs_libelle = ""
        # liste_sous_etabs_id = ""
        sousetabs = trimestre.sous_etabs.all()
        # cpt = 1
        # for se in sousetabs:
        #     if cpt < len(sousetabs):
        #         liste_sous_etabs_libelle +=se.libelle+" , "
        #         # liste_sous_etabs_id +=str(se.id)+"_"
        #     else:
        #         liste_sous_etabs_libelle +=se.libelle
        #         # liste_sous_etabs_id +=str(se.id)
        #     cpt +=1
        res.append({"id":trimestre.id,"libelle":trimestre.libelle,
            "date_deb":trimestre.date_deb,"date_fin":trimestre.date_fin,"is_active":trimestre.is_active,
            "numero":trimestre.numero})

    return Response(res)

@api_view(['POST'])
def update_trimestre(request):

    id = request.data['id']
    id_sousetab = request.data['id_sousetab']
    libelle = request.data['libelle']
    date_deb = request.data['date_deb']
    date_fin = request.data['date_fin']
    is_active = request.data['is_active']
    numero = request.data['numero']

    if is_active == False:
        trimestre = Trimestre.objects.get(id=id)
        seqs = trimestre.sequence_set.all()
        for s in seqs:
            s.is_active = False
            s.save()

    Trimestre.objects.filter(id=id).update(libelle=libelle,date_deb=date_deb,
        date_fin=date_fin,numero=numero,is_active=is_active)

    res = _list_trimestres(id_sousetab)
    return Response({"status":1,"trimestres":res})

@api_view(['POST'])
def delete_trimestre(request):
    id = int(request.data['id'])
    id_sousetab = request.data['id_sousetab']

    Trimestre.objects.filter(id=id).delete()

    res = _list_trimestres(id_sousetab)
    return Response({"status":1,"trimestres":res})

#################### CRUD SEQUENCE ####################

@api_view(['POST'])
def create_sequence(request):

    id_sousetab = request.data['id_sousetab']
    libelle = request.data['libelle']
    date_deb = request.data['date_deb']
    date_fin = request.data['date_fin']
    is_active = request.data['is_active']
    numero = request.data['numero']
    id_trimestre = request.data['id_trimestre']
    # id_trimestre = 1

    trimestre = Trimestre.objects.get(id=id_trimestre)
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""

    seq = Sequence()
    seq.libelle = libelle
    seq.date_deb = date_deb
    seq.date_fin = date_fin
    seq.numero = numero
    seq.is_active = True if is_active =="1" else False
    if seq.is_active:
        seq.is_active = trimestre.is_active
    seq.save()

    seq.trimestres.add(trimestre)
    if isinstance(id_sousetab,int):
        sousetab = SousEtab.objects.get(id=id_sousetab)
        seq.sous_etabs.add(sousetab)
    else:
        sousetabs = SousEtab.objects.filter()
        for sousetab in sousetabs:
            seq.sous_etabs.add(sousetab)

    res = _list_sequences(id_sousetab,"")
    trimestres = _list_trimestres(id_sousetab)
    return Response({"status":1,"sequences":res,"trimestres":trimestres})

@api_view(['POST'])
def list_sequences(request):

    id_sousetab = request.data['id_sousetab']
    id_trimestre = request.data['id_trimestre']
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    id_trimestre = int(id_trimestre) if (id_trimestre != "" and id_trimestre != None) else ""
    res = []
    seqs = []
    if isinstance(id_sousetab,int):
        if isinstance(id_trimestre,int):
            seqs = Sequence.objects.filter(sous_etabs__id=id_sousetab,trimestres__id=id_trimestre)
        else:
            seqs = Sequence.objects.filter(sous_etabs__id=id_sousetab)
    else:
        if isinstance(id_trimestre,int):
            seqs = Sequence.objects.filter(trimestres__id=id_trimestre)
        else:
            seqs = Sequence.objects.all()

    for seq in seqs:
        liste_sous_etabs_libelle = ""
        # liste_sous_etabs_id = ""
        sousetabs = seq.sous_etabs.all()
        libelle_trimestre = seq.trimestres.all()[0].libelle
        id_trimestre = seq.trimestres.all()[0].id
        res.append({"id":seq.id,"libelle":seq.libelle,"id_trimestre":id_trimestre,"libelle_trimestre":libelle_trimestre,
            "date_deb":seq.date_deb,"date_fin":seq.date_fin,"is_active":seq.is_active,
            "numero":seq.numero})

    trimestres = _list_trimestres(id_sousetab)
    return Response({"status":1,"sequences":res,"trimestres":trimestres})

@api_view(['POST'])
def update_sequence(request):

    id = request.data['id']
    id_sousetab = request.data['id_sousetab']
    id_trimestre = request.data['id_trimestre']
    libelle = request.data['libelle']
    date_deb = request.data['date_deb']
    date_fin = request.data['date_fin']
    is_active = request.data['is_active']
    numero = request.data['numero']

    trim = Trimestre.objects.get(id=id_trimestre)
    if is_active:
        is_active = trim.is_active
    sequences = Sequence.objects.get(id=id)
    trimestres = sequences.trimestres.filter()

    for tr in trimestres:
        sequences.trimestres.remove(tr)

    sequences.trimestres.add(trim)

    Sequence.objects.filter(id=id).update(libelle=libelle,date_deb=date_deb,
        date_fin=date_fin,numero=numero,is_active=is_active)

    res = _list_sequences(id_sousetab,"")
    trimestres = _list_trimestres(id_sousetab)
    return Response({"status":1,"sequences":res,"trimestres":trimestres})

@api_view(['POST'])
def delete_sequence(request):
    id = int(request.data['id'])
    id_sousetab = request.data['id_sousetab']
    Sequence.objects.filter(id=id).delete()

    res = _list_sequences(id_sousetab,"")
    trimestres = _list_trimestres(id_sousetab)
    return Response({"status":1,"sequences":res,"trimestres":trimestres})

#################### CRUD TYPE PAYEMENT ELEVE ####################

@api_view(['POST'])
def create_type_payement_eleve(request):

    id_sousetab = request.data['id_sousetab']
    id_cycle = request.data['id_cycle']
    id_niveau = request.data['id_niveau']
    id_classe = request.data['id_classe']
    libelle = request.data['libelle']
    date_deb = request.data['date_deb']
    date_fin = request.data['date_fin']
    montant = request.data['montant']
    # ordre_paiement = request.data['ordre_paiement']
    # entree_sortie_caisee = request.data['entree_sortie_caisee']
    classes = []

    if id_cycle == "all":
        classes = Classe.objects.filter(sous_etabs__id=id_sousetab)
    elif id_niveau == "all":
        classes = Classe.objects.filter(cycles__id=int(id_cycle))
    elif id_classe == "all":
        classes = Classe.objects.filter(niveaux__id=int(id_niveau))
    else:
        classes = Classe.objects.filter(id=int(id_classe))

    print(classes)

    tpe = TypePayementEleve()
    tpe.libelle = libelle
    tpe.date_deb = date_deb
    tpe.date_fin = date_fin
    tpe.montant = montant
    tpe.ordre_paiement = 0
    tpe.entree_sortie_caisee = "e"
    tpe.save()
    for classe in classes:
        tpe.classes.add(classe)

    res = _list_type_payement_eleve(id_sousetab,"","","")
    return Response({"status":1,"payements":res})

@api_view(['POST'])
def update_type_payement_eleve(request):

    id_classe = request.data['id_classe']
    id_sousetab = request.data['id_sousetab']
    libelles = request.data['libelles']
    date_debs = request.data['date_debs']
    date_fins = request.data['date_fins']
    montants = request.data['montants']
    tranches_a_delete = request.data['tranches_a_delete']
    # print(id_classe,libelles,date_debs,date_fins,montants,tranches_a_delete)

    libelles = libelles.split("²²")
    libelles = libelles[1:-1]

    montants = montants.split("²²")
    montants = montants[1:-1]

    date_debs = date_debs.split("²²")
    date_debs = date_debs[1:-1]

    date_fins = date_fins.split("²²")
    date_fins = date_fins[1:-1]

    tranches_a_delete = tranches_a_delete.split("²²")
    tranches_a_delete = tranches_a_delete[1:-1]
    n_del = len(tranches_a_delete)

    del_list =[]
    classe = Classe.objects.get(id=id_classe)
    for item in tranches_a_delete:
        tpe = TypePayementEleve.objects.get(id=item)
        tpe.classes.remove(classe)
        del_list.append(int(item))

    i = 0
    n = len(libelles)
    while i<n:
        id_tranche,lib = libelles[i].split(",")
        id_m,montant = montants[i].split(",")
        id_deb,deb = date_debs[i].split(",")
        id_fin,fin = date_fins[i].split(",")
        id_tranche = int(id_tranche)
        if id_tranche not in del_list:
            print("pas la: ",id_tranche)
            TypePayementEleve.objects.filter(id=id_tranche).update(
                libelle=lib,date_deb=deb,date_fin=fin,montant=montant)
        i+=1


    n = len(libelles)
    print(libelles,n_del)

    # TypePayementEleve.objects.filter(id=id).update(libelle=libelle,date_deb=date_deb,
        # date_fin=date_fin,montant=montant,ordre_paiement=ordre_paiement,entree_sortie_caisee=entree_sortie_caisee)
    res = _list_type_payement_eleve(id_sousetab,"","","")
    return Response({"status":1,"payements":res})

@api_view(['POST'])
def list_type_payement_eleve(request):

    id_sousetab = request.data['id_sousetab']
    id_cycle = request.data['id_cycle']
    id_niveau = request.data['id_niveau']
    id_classes = request.data['id_classes']

    res = []
    classes = []

    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    id_cycle = int(id_cycle) if (id_cycle != "" and id_cycle != None) else ""
    id_niveau = int(id_niveau) if (id_niveau != "" and id_niveau != None) else ""

    if id_classes != "" and id_classes != None:
        id_classes = id_classes.split("_")
        classes = [Classe.objects.get(id=int(id)) for id in id_classes]

    if isinstance(id_sousetab,int):
        classes = Classe.objects.filter(sous_etabs__id=id_sousetab)
    elif isinstance(id_cycle,int):
        classes = Classe.objects.filter(cycles__id=id_cycle)
    elif isinstance(id_niveau,int):
        classes = Classe.objects.filter(niveaux__id=id_niveau)

    for cl in classes:
        tpe = TypePayementEleve.objects.filter(classes=cl,entree_sortie_caisee="e").order_by("date_deb","date_fin")
        total = 0
        cpt = 1
        info_tranches = ""
        for t in tpe:
            if cpt < len(tpe):
                info_tranches += str(t.id)+","+t.libelle+","+str(t.montant)+","+str(t.ordre_paiement)+","+str(t.date_deb)+","+str(t.date_fin)+"²²"
            else:
                info_tranches += str(t.id)+","+t.libelle+","+str(t.montant)+","+str(t.ordre_paiement)+","+str(t.date_deb)+","+str(t.date_fin)
            total += t.montant
            cpt += 1
        res.append({"id":cl.id,"classe":cl.libelle,"info_tranches":info_tranches,"total":total})

    return Response(res)

@api_view(['POST'])
def delete_type_payement_eleve(request):
    id = int(request.data['id'])
    TypePayementEleve.objects.filter(id=id).delete()

    return Response({"status":"Ok, Type Payement Eleve deleted!"})

#################### CRUD TYPE PAYEMENT DIVERS ####################

@api_view(['POST'])
def create_type_payement_divers(request):

    id_sousetab = request.data['id_sousetab']
    libelle = request.data['libelle']
    montant = request.data['montant']
    entree_sortie_caisee = request.data['e_s']

    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""

    tpd = TypePayementDivers()
    tpd.libelle = libelle
    tpd.montant = montant
    tpd.entree_sortie_caisee = entree_sortie_caisee
    tpd.save()

    sousetabs = []
    if isinstance(id_sousetab,int):
        sousetabs = SousEtab.objects.filter(id=id_sousetab)
    else:
        sousetabs = SousEtab.objects.filter()

    for se in sousetabs:
        tpd.sous_etabs.add(se)

    res = _list_type_payement_divers(id_sousetab)

    return Response({"status":1,"payements":res})

@api_view(['POST'])
def update_type_payement_divers(request):

    id = request.data['id']
    id_sousetab = request.data['id_sousetab']
    libelle = request.data['libelle']
    montant = request.data['montant']
    entree_sortie_caisee = request.data['e_s']

    TypePayementDivers.objects.filter(id=id).update(libelle=libelle,montant=montant,entree_sortie_caisee=entree_sortie_caisee)

    res = _list_type_payement_divers(id_sousetab)

    return Response({"status":1,"payements":res})

@api_view(['POST'])
def list_type_payement_divers(request):

    id_sousetab = request.data['id_sousetab']

    res = []
    tpds = []

    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""

    if isinstance(id_sousetab,int):
        tpds = TypePayementDivers.objects.filter(sous_etabs__id=id_sousetab)
    else:
        tpds = TypePayementDivers.objects.filter()

    for tpd in tpds:
        if isinstance(id_sousetab,int):
            setabs = tpd.sous_etabs.filter(id=id_sousetab)
        else:
            setabs = tpd.sous_etabs.filter()
        for se in setabs:
            res.append({"id":tpd.id,"libelle":tpd.libelle,
            "montant":tpd.montant,"entree_sortie_caisee":tpd.entree_sortie_caisee})

    return Response(res)

@api_view(['POST'])
def delete_type_payement_divers(request):
    id = int(request.data['id'])
    id_sousetab = request.data['id_sousetab']
    TypePayementDivers.objects.filter(id=id).delete()

    res = _list_type_payement_divers(id_sousetab)

    return Response({"status":1,"payements":res})

#################### CRUD TYPE ENSEIGNANT ####################

@api_view(['POST'])
def create_type_enseignant(request):

    id_sousetab = request.data['id_sousetab']
    libelle = request.data['libelle']
    description = request.data['description']
    est_paye_a_l_heure = True if request.data['est_paye_a_l_heure']== "oui" else False
    montant_quota_horaire = request.data['montant']

    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""

    tpe = TypeEnseignant()
    tpe.libelle = libelle
    tpe.description = description
    tpe.montant_quota_horaire = montant_quota_horaire if montant_quota_horaire != "" and montant_quota_horaire != None else 0
    tpe.est_paye_a_l_heure = est_paye_a_l_heure
    tpe.save()

    sousetabs = []
    if isinstance(id_sousetab,int):
        sousetabs = SousEtab.objects.filter(id=id_sousetab)
    else:
        sousetabs = SousEtab.objects.filter()

    for se in sousetabs:
        tpe.sous_etabs.add(se)
    res = _list_type_enseignants(id_sousetab)
    return Response({"status":1,"ens":res})

@api_view(['POST'])
def update_type_enseignant(request):

    id = request.data['id']
    id_sousetab = request.data['id_sousetab']
    libelle = request.data['libelle']
    est_paye_a_l_heure = True if request.data['est_paye_a_l_heure']== "oui" else False
    description = request.data['description']
    montant_quota_horaire = request.data['montant']

    montant_quota_horaire = float(montant_quota_horaire) if montant_quota_horaire != "" and montant_quota_horaire != None else 0

    TypeEnseignant.objects.filter(id=id).update(libelle=libelle,est_paye_a_l_heure=est_paye_a_l_heure,
            description=description, montant_quota_horaire=montant_quota_horaire)

    res = _list_type_enseignants(id_sousetab)
    return Response({"status":1,"ens":res})

@api_view(['POST'])
def list_type_enseignants(request):

    id_sousetab = request.data['id_sousetab']

    res = []
    tpds = []

    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""

    if isinstance(id_sousetab,int):
        tpds = TypeEnseignant.objects.filter(sous_etabs__id=id_sousetab)
    else:
        tpds = TypeEnseignant.objects.filter()

    for tpd in tpds:
        if isinstance(id_sousetab,int):
            setabs = tpd.sous_etabs.filter(id=id_sousetab)
        else:
            setabs = tpd.sous_etabs.filter()
        for se in setabs:
            res.append({"id":tpd.id,"libelle":tpd.libelle,
            "description":tpd.description,"montant_quota_horaire":tpd.montant_quota_horaire,
            "est_paye_a_l_heure":tpd.est_paye_a_l_heure})

    return Response(res)

@api_view(['POST'])
def delete_type_enseignant(request):
    id = int(request.data['id'])
    id_sousetab = request.data['id_sousetab']
    TypeEnseignant.objects.filter(id=id).delete()

    res = _list_type_enseignants(id_sousetab)
    return Response({"status":1,"ens":res})

#################### CRUD HIERARCHIE ####################

@api_view(['POST'])
def create_hierarchie(request):

    id_sousetab = request.data['id_sousetab']
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""

    libelle = request.data['libelle_hierarchie']
    is_adminstaff = True if request.data['is_adminstaff']== "1" else False
    rang = request.data['rang']
    rang = int(rang) if (rang != "_" and rang != None) else 0

    hi = HierarchieEtab()
    hi.libelle = libelle
    hi.rang = rang
    hi.is_adminstaff = is_adminstaff
    # hi.quota_cursus = quota_cursus if quota_cursus != "" and quota_cursus != None else 0
    hi.save()

    sousetabs = []
    if isinstance(id_sousetab,int):
        sousetabs = SousEtab.objects.filter(id=id_sousetab)
    else:
        sousetabs = SousEtab.objects.filter()

    for se in sousetabs:
        hi.sous_etabs.add(se)

    res = _list_hierarchies(id_sousetab)
    return Response({"status":1,"hierarchies":res})

@api_view(['POST'])
def update_hierarchie(request):
    id_sousetab = request.data['id_sousetab']
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    id = int(request.data['id'])
    libelle = request.data['libelle_hierarchie']
    is_adminstaff = True if request.data['is_adminstaff']== "1" else False
    rang = request.data['rang']
    print("rang: ",rang,libelle)
    rang = int(rang) if (rang != "_" and rang != None) else 0

    if id >0:
        # quota_cursus = quota_cursus if quota_cursus != "" and quota_cursus != None else 0

        HierarchieEtab.objects.filter(id=id).update(libelle=libelle,rang=rang,
                is_adminstaff=is_adminstaff)
    res = _list_hierarchies(id_sousetab)
    return Response({"status":1,"hierarchies":res})

@api_view(['POST'])
def list_hierarchies(request):

    id_sousetab = request.data['id_sousetab']

    res = []
    tpds = []

    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""

    if isinstance(id_sousetab,int):
        tpds = HierarchieEtab.objects.filter(sous_etabs__id=id_sousetab)
    else:
        tpds = HierarchieEtab.objects.filter()
    for tpd in tpds:
        if isinstance(id_sousetab,int):
            setabs = tpd.sous_etabs.filter(id=id_sousetab)
        else:
            setabs = tpd.sous_etabs.filter()
        for se in setabs:
            res.append({"id":tpd.id,"id_sousetab":se.id,"libelle_hierarchie":tpd.libelle,
            "rang":tpd.rang,"is_adminstaff":tpd.is_adminstaff,
            "quota_cursus":tpd.quota_cursus,"is_enseignant":"0"})

    s = SousEtab.objects.get(id=id_sousetab)
    config = s.configannee_set.all()[0]
    quota_enseignant = config.pourcentage_cursus_enseignant
    res.append({"id":0,"id_sousetab":s.id,"libelle_hierarchie":config.appellation_formateur,
        "rang":"_","is_adminstaff":"0", "quota_cursus":quota_enseignant,"is_enseignant":"1"})

    return Response(res)

@api_view(['POST'])
def delete_hierarchie(request):
    id = int(request.data['id'])
    if id != 0:
        HierarchieEtab.objects.filter(id=id).delete()
    id_sousetab = request.data['id_sousetab']

    res = _list_hierarchies(id_sousetab)
    return Response({"status":1,"hierarchies":res})

#################### CRUD TYPE PAYEMENT ENSEIGNANT ####################

@api_view(['POST'])
def create_type_payement_enseignant(request):

    id_sousetab = request.data['id_sousetab']
    id_type_enseignant = request.data['id_type_enseignant']
    libelle = request.data['libelle']
    montant = request.data['montant']
    entree_sortie_caisee = request.data['entree_sortie_caisee']

    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    type_enseignant = TypeEnseignant.objects.get(id=id_type_enseignant)
    tpd = TypePayementEnseignant()
    tpd.libelle = libelle
    tpd.montant = montant
    tpd.entree_sortie_caisee = entree_sortie_caisee
    tpd.save()
    tpd.type_enseignant.add(type_enseignant)

    sousetabs = []
    if isinstance(id_sousetab,int):
        sousetabs = SousEtab.objects.filter(id=id_sousetab)
    else:
        sousetabs = SousEtab.objects.filter()

    for se in sousetabs:
        tpd.sous_etabs.add(se)
    type_ens = _list_type_enseignants(id_sousetab)
    res = _list_type_payement_enseignants(id_sousetab,"")
    return Response({"status":1,"payements":res,"type_ens":type_ens})

@api_view(['POST'])
def update_type_payement_enseignant(request):

    id = request.data['id']
    id_sousetab = request.data['id_sousetab']
    id_type_enseignant = request.data['id_type_enseignant']
    libelle = request.data['libelle']
    montant = request.data['montant']
    entree_sortie_caisee = request.data['entree_sortie_caisee']

    te = TypeEnseignant.objects.get(id=id_type_enseignant)
    tpymt_ens = TypePayementEnseignant.objects.get(id=id)
    ens = tpymt_ens.type_enseignant.filter()

    for e in ens:
        tpymt_ens.type_enseignant.remove(e)

    tpymt_ens.type_enseignant.add(te)

    TypePayementEnseignant.objects.filter(id=id).update(libelle=libelle,montant=montant,entree_sortie_caisee=entree_sortie_caisee)

    type_ens = _list_type_enseignants(id_sousetab)
    res = _list_type_payement_enseignants(id_sousetab,"")
    return Response({"status":1,"payements":res,"type_ens":type_ens})

@api_view(['POST'])
def list_type_payement_enseignants(request):

    id_sousetab = request.data['id_sousetab']
    id_type_enseignant = request.data['id_type_enseignant']

    res = []
    tpds = []

    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    id_type_enseignant = int(id_type_enseignant) if (id_type_enseignant != "" and id_type_enseignant != None) else ""

    if isinstance(id_sousetab,int):
        if isinstance(id_type_enseignant,int):
            tpds = TypePayementEnseignant.objects.filter(sous_etabs__id=id_sousetab,type_enseignant__id=id_type_enseignant)
        else:
            tpds = TypePayementEnseignant.objects.filter(sous_etabs__id=id_sousetab)
    else:
        if isinstance(id_type_enseignant,int):
            tpds = TypePayementEnseignant.objects.filter(type_enseignant__id=id_type_enseignant)
        else:
            tpds = TypePayementEnseignant.objects.filter()

    for tpd in tpds:
        libelle_type_enseignants =""
        id_type_enseignant = 0
        if isinstance(id_sousetab,int):
            setabs = tpd.sous_etabs.filter(id=id_sousetab)
        else:
            setabs = tpd.sous_etabs.filter()
        if isinstance(id_type_enseignant,int):
            type_enseignants = tpd.type_enseignant.filter(id=id_type_enseignant)

        else:
            type_enseignants = tpd.type_enseignant.filter()
        # cpt = 1
        # for te in type_enseignants:
        #     if cpt < len(type_enseignants):
        #         libelle_type_enseignants+=te.libelle+","
        #     else:
        #         libelle_type_enseignants+=te.libelle

        type_enseignants = tpd.type_enseignant.filter()
        if len(type_enseignants)>0:
            id_type_enseignant = type_enseignants[0].id
            libelle_type_enseignants = type_enseignants[0].libelle
        # for se in setabs:
        res.append({"id":tpd.id,"libelle_payement":tpd.libelle,"id_type_enseignant":id_type_enseignant,"libelle_ens":libelle_type_enseignants,
            "montant":tpd.montant,"entree_sortie_caisee":tpd.entree_sortie_caisee})

    type_ens = _list_type_enseignants(id_sousetab)
    return Response({"payements":res,"type_ens":type_ens})

@api_view(['POST'])
def delete_type_payement_enseignant(request):
    id = int(request.data['id'])
    id_sousetab = int(request.data['id_sousetab'])
    TypePayementEnseignant.objects.filter(id=id).delete()

    type_ens = _list_type_enseignants(id_sousetab)
    res = _list_type_payement_enseignants(id_sousetab,"")
    return Response({"status":1,"payements":res,"type_ens":type_ens})

#################### CRUD TYPE PAYEMENT ADMINSTAFF ####################

@api_view(['POST'])
def create_type_payement_adminstaff(request):

    id_sousetab = request.data['id_sousetab']
    id_hierarchie = request.data['id_hierarchie']
    libelle = request.data['libelle']
    montant = request.data['montant']
    entree_sortie_caisee = request.data['entree_sortie_caisee']

    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    hierarchie = HierarchieEtab.objects.get(id=id_hierarchie)
    print(hierarchie)
    tpd = TypePayementAdminStaff()
    tpd.libelle = libelle
    tpd.montant = montant
    tpd.entree_sortie_caisee = entree_sortie_caisee
    tpd.save()
    tpd.hierarchies.add(hierarchie)

    sousetabs = []
    if isinstance(id_sousetab,int):
        sousetabs = SousEtab.objects.filter(id=id_sousetab)
    else:
        sousetabs = SousEtab.objects.filter()

    for se in sousetabs:
        tpd.sous_etabs.add(se)

    type_hierarchies = _list_hierarchies(id_sousetab)
    res = _list_type_payement_adminstaffs(id_sousetab,"")

    return Response({"status":1,"payements":res,"type_hierarchies":type_hierarchies})

@api_view(['POST'])
def update_type_payement_adminstaff(request):

    id = request.data['id']
    id_sousetab = request.data['id_sousetab']
    id_hierarchie = request.data['id_hierarchie']
    libelle = request.data['libelle']
    montant = request.data['montant']
    entree_sortie_caisee = request.data['entree_sortie_caisee']

    h = HierarchieEtab.objects.get(id=id_hierarchie)
    tpymt_admins = TypePayementAdminStaff.objects.get(id=id)
    hierarchies = tpymt_admins.hierarchies.filter()

    for hierarchie in hierarchies:
        tpymt_admins.hierarchies.remove(hierarchie)

    tpymt_admins.hierarchies.add(h)

    TypePayementAdminStaff.objects.filter(id=id).update(libelle=libelle,montant=montant,entree_sortie_caisee=entree_sortie_caisee)

    type_hierarchies = _list_hierarchies(id_sousetab)
    res = _list_type_payement_adminstaffs(id_sousetab,"")

    return Response({"status":1,"payements":res,"type_hierarchies":type_hierarchies})

@api_view(['POST'])
def list_type_payement_adminstaffs(request):

    id_sousetab = request.data['id_sousetab']
    id_hierarchie = request.data['id_hierarchie']

    res = []
    tpds = []
    hierarchies = []

    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    id_hierarchie = int(id_hierarchie) if (id_hierarchie != "" and id_hierarchie != None) else ""

    if isinstance(id_sousetab,int):
        if isinstance(id_hierarchie,int):
            tpds = TypePayementAdminStaff.objects.filter(sous_etabs__id=id_sousetab,hierarchies__id=id_hierarchie)
        else:
            tpds = TypePayementAdminStaff.objects.filter(sous_etabs__id=id_sousetab)
    else:
        if isinstance(id_hierarchie,int):
            tpds = TypePayementAdminStaff.objects.filter(hierarchies__id=id_hierarchie)
        else:
            tpds = TypePayementAdminStaff.objects.filter()

    for tpd in tpds:
        libelle_hierarchie =""
        id_h = 0
        if isinstance(id_sousetab,int):
            setabs = tpd.sous_etabs.filter(id=id_sousetab)
        else:
            setabs = tpd.sous_etabs.filter()

        if isinstance(id_hierarchie,int):
            hierarchies = tpd.hierarchies.filter(id=id_hierarchie)

        else:
            hierarchies = tpd.hierarchies.filter()
            print("ici")
        print(hierarchies)
        # cpt = 1
        # for te in hierarchies:
        #     if cpt < len(hierarchies):
        #         libelle_hierarchies+=te.libelle+", "
        #     else:
        #         libelle_hierarchies+=te.libelle
        if len(hierarchies)>0:
            libelle_hierarchie =hierarchies[0].libelle
            id_h =hierarchies[0].id
        for se in setabs:
            res.append({"id":tpd.id,"libelle_payement":tpd.libelle,"libelle_h":libelle_hierarchie,
                "id_h":id_h,"montant":tpd.montant,"entree_sortie_caisee":tpd.entree_sortie_caisee})

    type_hierarchies = _list_hierarchies(id_sousetab)

    return Response({"status":1,"payements":res,"type_hierarchies":type_hierarchies})

@api_view(['POST'])
def delete_type_payement_adminstaff(request):
    id = int(request.data['id'])
    id_sousetab = request.data['id_sousetab']
    TypePayementAdminStaff.objects.filter(id=id).delete()

    type_hierarchies = _list_hierarchies(id_sousetab)
    res = _list_type_payement_adminstaffs(id_sousetab,"")

    return Response({"status":1,"payements":res,"type_hierarchies":type_hierarchies})

#################### CRUD QUOTA CURSUS ####################

@api_view(['POST'])
def set_quota_cursus(request):

    id_sousetab = request.data['id_sousetab']
    quotas = request.data['quotas']
    id_hierarchies = request.data['id_hierarchies']

    id_hierarchies = id_hierarchies.split("_")
    id_hierarchies = id_hierarchies[1:-1]
    n = len(id_hierarchies)

    if n>0:
        quotas = quotas.split("_")
        quotas = quotas[1:-1]
        quotas = [float(quota) for quota in quotas]
        id_hierarchies = [int(id) for id in id_hierarchies]

        cpt_quota =0
        for id_h in id_hierarchies:
            if id_h >0:
                HierarchieEtab.objects.filter(id=id_h).update(quota_cursus=quotas[cpt_quota])
            else:
                ConfigAnnee.objects.filter(sous_etabs=id_sousetab).update(pourcentage_cursus_enseignant=float(quotas[cpt_quota]))
            cpt_quota += 1
    res = _list_quota_cursus(id_sousetab)
    return Response({"status":1,"quotas":res})

@api_view(['POST'])
def list_quota_cursus(request):

    id_sousetab = request.data['id_sousetab']
    hierarchies = HierarchieEtab.objects.filter(sous_etabs__id=id_sousetab).order_by('rang')
    res = []

    for h in hierarchies:
        res.append({"id":h.id,"rang":h.rang,"libelle":h.libelle,"quota_cursus":h.quota_cursus})
    config = ConfigAnnee.objects.get(sous_etabs=id_sousetab)
    res.append({"id":0,"rang":"_","libelle":config.appellation_formateur,"quota_cursus":config.pourcentage_cursus_enseignant})

    return Response(res)

#################### CRUD GROUPE D'UTILISATEURS ####################

@api_view(['POST'])
def set_groupe_users(request):

    id_sousetab = request.data['id_sousetab']

    sousetab = SousEtab.objects.get(id=id_sousetab)
    hierarchies = HierarchieEtab.objects.filter(sous_etabs=sousetab)

    for h in hierarchies:
        groupe = Group()
        groupe.name = h.libelle
        groupe.save()
        sousetab.groups.add(groupe)
        h.group.add(groupe)
        if (h.libelle).lower() == "proviseur":
            PredefinedRole.objects.get(libelle="principal").groupes.add(groupe)
        elif (h.libelle).lower() == "censeur":
            PredefinedRole.objects.get(libelle="censeur").groupes.add(groupe)
        elif (h.libelle).lower() == "surveillant":
            PredefinedRole.objects.get(libelle="surveillant").groupes.add(groupe)
        elif (h.libelle).lower() == "intendant":
            PredefinedRole.objects.get(libelle="intendant").groupes.add(groupe)
        elif (h.libelle).lower() == "directeur":
            PredefinedRole.objects.get(libelle="directeur").groupes.add(groupe)
    groupe = Group()
    groupe.name = "Enseignant"
    groupe.save()
    sousetab.groups.add(groupe)
    if (sousetab.type_sousetab).lower() == "secondaire":
        PredefinedRole.objects.get(type_role="secondaire",libelle="enseignant").groupes.add(groupe)
    else:
        PredefinedRole.objects.get(type_role="primaire",libelle="enseignant").groupes.add(groupe)



    return Response({"status":"Users Groups Settled !"})

@api_view(['POST'])
def delete_groupe_users(request):
    id = int(request.data['id'])
    Group.objects.filter(id=id).delete()

    return Response({"status":"Ok, Group deleted!"})

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @permission_classes([IsConnected])
# @permission_classes([IsCenseurAndClassesAllowed])
# @permission_classes([IsPrincipalAndClassesAllowed])
@permission_classes([IsIntendantAndClassesAllowed])
# @permission_classes([IsEnseignantAndClassesAllowed])
def list_groupe_users(request):

    id_sousetab = int(request.data['id_sousetab'])
    groups = SousEtab.objects.get(id=id_sousetab).groups.all()
    # groups = Group.objects.filter()
    print(groups)
    res = []

    for g in groups:
        res.append({"name":g.name})

    return Response(res)

# A annuler!
@api_view(['POST'])
def add_user_to_group(request):
    for i in [1,2,3,6]:
        group = Group.objects.get(id=i)
        user = User.objects.get(id=2)
        group.user_set.add(user)
    group = Group.objects.get(id=6)
    user = User.objects.get(id=1)
    group.user_set.add(user)

    return Response({"status":"User added to Group!"})

@api_view(['POST'])
def associer_user_roles(request):

    id_user = request.data['id_user']
    id_sousetab = request.data['id_sousetab']
    infos = request.data['infos']
    login= request.data['login']
    pwd= request.data['pwd']
    nom= request.data['nom']
    prenom= request.data['prenom']
    email= request.data['email']
    sexe= request.data['sexe']
    date_entree= request.data['date_entree']
    date_sortie= request.data['date_sortie']
    tel1= request.data['tel1']
    tel2= request.data['tel2']
    is_enseignant= request.data['is_enseignant']
    is_active= request.data['is_active']
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""

    # id_sousetab = request.data['id_sousetab']
    # is_enseignant = request.data['is_enseignant']
    # id_hierarchies = request.data['id_hierarchies']
    # id_classes = request.data['id_classes']
    # id_user = request.data['id_user']
    # id_matieres_specialite = request.data["id_matieres_specialite"]

    user = User.objects.get(id=id_user)
    sousetab = SousEtab.objects.get(id=int(id_sousetab))

    AdminStaff.objects.filter(users=user).delete()
    # Enseignant.objects.filter(users=user).delete()
    groupes = Group.objects.filter(user=user)
    print(groupes)
    for g in groupes:
        g.user_set.remove(user)

    # user.username = login
    # if pwd != "":
    #     user.password = make_password(pwd)
    # user.is_active = is_active
    # user.is_superuser = False
    # user.first_name = nom
    # user.last_name = prenom
    # user.is_staff = False
    # user.email = email
    # user.save()

    if pwd =="":
        User.objects.filter(id=id_user).update(is_active=is_active,first_name=nom,last_name=prenom,email=email)
    else:
        User.objects.filter(id=id_user).update(is_active=is_active,password=make_password(pwd),first_name=nom,last_name=prenom,email=email)

    profil = Profil.objects.get(user=user)

    profil.sexe = sexe
    profil.tel1 = tel1
    profil.tel2 = tel2
    if date_entree != "":
        profil.date_entree = date_entree
    if date_sortie != "":
        profil.date_sortie = date_sortie

    profil.save()
    print("is_enseignant: ",is_enseignant)
    ens = Enseignant.objects.filter(users=user)
    print("ENS: ",ens)
    if len(ens)<=0:
        ens = Enseignant()
        ens.is_active = is_enseignant
        ens.save()
        ens.users.add(user)
    else:
        ens = ens[0]
        ens.is_active = is_enseignant
        ens.save()
    # ACTIVER
    # if is_enseignant:
    #     ens.sous_etabs.add(sousetab)


    print(infos)
    if len(infos)>0:
        infos = infos.split("²²")
        print("ici: ",infos)
        for info in infos:
            if info != "":
                classes = []
                id_cls_list = []
                print(info)
                # print(len(info))
                info = info.split(":")
                id_hierarchie = info[0]
                hierarchie = HierarchieEtab.objects.get(id=id_hierarchie)
                print("hierarchie: ",id_hierarchie)
                if info[1] != "":
                    elts = info[1].split(",")
                    for id_c in elts:
                        if id_c!= "":
                            id_cls_list.append(int(id_c))
                    classes = Classe.objects.filter(id__in=id_cls_list)
                    print("classes: ",id_cls_list)
                    sousetab = SousEtab.objects.get(id=id_sousetab)
                    adminStaff = AdminStaff()
                    adminStaff.is_active = True
                    adminStaff.save()
                    adminStaff.users.add(user)
                    adminStaff.hierarchie_etab.add(hierarchie)
                    adminStaff.sous_etabs.add(sousetab)

                    for cl in classes:
                        adminStaff.handle_classes.add(cl)

    # id_hierarchies = id_hierarchies.split("_") if id_hierarchies!="" else []
    # id_classes = id_classes.split("_")
    # cpt_hierarchie = 0
    # print("id_hierarchies:",id_hierarchies)
    # for id_hierarchie in id_hierarchies:
    #     classes = []
    #     id_cls_list = []
    #     print(id_hierarchie)
    #     print(id_classes[cpt_hierarchie])
    #     hierarchie = HierarchieEtab.objects.get(id=id_hierarchie)
    #     if id_classes[cpt_hierarchie] =="all":
    #         classes = Classe.objects.filter(sous_etabs=sousetab)
    #     else:
    #         id_cls = id_classes[cpt_hierarchie].split(",")
    #         for id_c in id_cls:
    #             id_cls_list.append(int(id_c))
    #         classes = Classe.objects.filter(id__in=id_cls_list)
    #     print("Classes:",classes)
    #     adminStaff = AdminStaff()
    #     adminStaff.is_active = True
    #     adminStaff.save()
    #     adminStaff.users.add(user)
    #     adminStaff.hierarchie_etab.add(hierarchie)
    #     adminStaff.sous_etabs.add(sousetab)



    #     for cl in classes:
    #         adminStaff.handle_classes.add(cl)
    #     cpt_hierarchie += 1

    #     group = HierarchieEtab.objects.get(id=id_hierarchie).group.all()[0]
    #     # if user not in group.user_set.all():
    #     group.user_set.add(user)

    # id_matieres_spe = []
    # id_matieres_list = []
    # if is_enseignant == "1":
    #     id_matieres_specialite = id_matieres_specialite.split("_")
    #     for id_m in id_matieres_specialite:
    #         id_matieres_list.append(int(id_m))
    #     matieres = Matiere.objects.filter(id__in=id_matieres_list)
    #     print("matieres:",matieres)
    #     enseignants = Enseignant.objects.filter(users=user)
    #     print(enseignants)
    #     if len(enseignants)==0:
    #         ens = Enseignant()
    #         ens.users.add(user)
    #         ens.is_active = True
    #         ens.save()
    #     else:
    #         ens = enseignants[0]
    #     group = Group.objects.filter(name__iexact="enseignant")[0]
    #     group.user_set.add(user)
    #     print("ID ENSEIGNANT:",ens.id)
    #     for mat in matieres:
    #         ens.matiere_specialites.add(mat)

        print("It's a teacher")
    res,list_hierarchies = _list_user_roles(id_sousetab)
    return Response({"status":1,"res":res,"adminstaffs":list_hierarchies})

@api_view(['POST'])
def list_user_roles(request):

    id_sousetab = request.data['id_sousetab']
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    users,users_temps = [], []
    res = []


    if isinstance(id_sousetab, int):
        sous_etabs = SousEtab.objects.filter(id=id_sousetab)[0]
        users = sous_etabs.users.filter(is_active__in=[True])
    else:
        sous_etabs = SousEtab.objects.all()
        for s in sous_etabs:
            users_temps = s.users.filter(is_active__in=[True])
            for user in users_temps:
                if user not in users:
                    users.append(user)

    for user in users:
        liste_responsabilites = ""
        id_responsabilites = ""

        if isinstance(id_sousetab, int):
            adminStaffs = AdminStaff.objects.filter(sous_etabs__id=id_sousetab,users=user)
        else:
            adminStaffs = AdminStaff.objects.filter(users=user)

        if len(adminStaffs)>0:
            # adminStaff = adminStaff[0]
            for adminStaff in adminStaffs:
                hierarchie = adminStaff.hierarchie_etab.all()[0]
                classes = adminStaff.handle_classes.all()
                print(hierarchie)
                print(classes)
                liste_responsabilites+= hierarchie.libelle+":"
                id_responsabilites+= str(hierarchie.id)+":"
                cpt_c = 1
                for c in classes:
                    if cpt_c < len(classes):
                        liste_responsabilites += c.libelle+","
                        id_responsabilites += str(c.id)+","
                    else:
                        liste_responsabilites += c.libelle+"²²"
                        id_responsabilites += str(c.id)+"²²"
                    cpt_c +=1

        enseignant = Enseignant.objects.filter(users=user)
        liste_matieres_enseignees = ""
        is_enseignant = False
        if len(enseignant)>0:
            is_enseignant = enseignant[0].is_active

            # matieres_spe = enseignant[0].matiere_specialites.all()
            # cpt_m = 1
            # for m in matieres_spe:
            #     if cpt_m < len(matieres_spe):
            #         liste_matieres_enseignees+=m.libelle+","
            #     else:
            #         liste_matieres_enseignees+=m.libelle
            # print(matieres_spe)
        profil = Profil.objects.get(user=user)
        res.append({"id":user.id,"login":user.username,"pwd":user.password,
            "is_active":user.is_active,"sexe":profil.sexe,"tel1":profil.tel1,"tel2":profil.tel2,
            "date_entree":profil.date_entree,"date_sortie":profil.date_sortie,"email":user.email
            ,"nom":user.first_name,"prenom":user.last_name,"id_responsabilites":id_responsabilites,
            "liste_responsabilites":liste_responsabilites,"is_enseignant":is_enseignant})
        res = sorted(res, key=lambda k: k['nom'])


    list_hierarchies = []
    hierarchies = HierarchieEtab.objects.filter(sous_etabs__id=id_sousetab)
    cpt = 1
    for h in hierarchies:
        # if cpt < len(adminstaffs)
        list_hierarchies.append({"id":h.id,"libelle":h.libelle})


    return Response({"res":res,"adminstaffs":list_hierarchies})

#################### CRUD UTILISATEURS ####################

@api_view(['POST'])
def create_user(request):

    id_sousetab = request.data['id_sousetab']
    infos = request.data['infos']
    login= request.data['login']
    pwd= request.data['pwd']
    nom= request.data['nom']
    prenom= request.data['prenom']
    email= request.data['email']
    sexe= request.data['sexe']
    date_entree= request.data['date_entree']
    date_sortie= request.data['date_sortie']
    tel1= request.data['tel1']
    tel2= request.data['tel2']
    is_enseignant= request.data['is_enseignant']
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""

    status = 0

    if len(User.objects.filter(username__iexact=login))<=0:
        user = User()
        user.username = login
        user.password = make_password(pwd)
        user.is_active = True
        user.is_superuser = False
        user.first_name = nom
        user.last_name = prenom
        user.is_staff = False
        user.email = email

        profil = Profil()
        profil.sexe = request.data['sexe']
        profil.tel1 = request.data['tel1']
        profil.tel2 = request.data['tel2']
        # profil.is_active = True if request.data['is_active']=="1" else False
        if date_entree != "":
            profil.date_entree = date_entree
        if date_sortie != "":
            profil.date_sortie = date_sortie

        user.save()
        profil.user = user
        profil.save()

        if is_enseignant:
            ens = Enseignant()
            ens.users.add(user)
            ens.is_active = is_enseignant
            ens.save()
            # ACTIVER
            # ens.sous_etabs.add(sousetab)

            group = Group.objects.filter(name__iexact="enseignant")[0]
            group.user_set.add(user)

        if isinstance(id_sousetab, int):
            sous_etab = SousEtab.objects.get(id=id_sousetab)
            sous_etab.users.add(user)
        else:
            sous_etabs = SousEtab.objects.all()
            for sous_etab in sous_etabs:
                sous_etab.users.add(user)

        print(infos)
        if len(infos)>0:
            infos = infos.split("²²")
            print("ici: ",infos)
            for info in infos:
                if info != "":
                    classes = []
                    id_cls_list = []
                    print(info)
                    # print(len(info))
                    info = info.split(":")
                    id_hierarchie = info[0]
                    hierarchie = HierarchieEtab.objects.get(id=id_hierarchie)
                    print("hierarchie: ",id_hierarchie)
                    if info[1] != "":
                        elts = info[1].split(",")
                        for id_c in elts:
                            if id_c!= "":
                                id_cls_list.append(int(id_c))
                        classes = Classe.objects.filter(id__in=id_cls_list)
                        print("classes: ",id_cls_list)
                        sousetab = SousEtab.objects.get(id=id_sousetab)
                        adminStaff = AdminStaff()
                        adminStaff.is_active = True
                        adminStaff.save()
                        adminStaff.users.add(user)
                        adminStaff.hierarchie_etab.add(hierarchie)
                        adminStaff.sous_etabs.add(sousetab)

                        for cl in classes:
                            adminStaff.handle_classes.add(cl)
                    group = HierarchieEtab.objects.get(id=id_hierarchie).group.all()[0]
                    # if user not in group.user_set.all():
                    group.user_set.add(user)

        status = 1

    res,list_hierarchies = _list_user_roles(id_sousetab)
    return Response({"status":status,"res":res,"adminstaffs":list_hierarchies})

@api_view(['POST'])
def list_users(request):

    id_sousetab = request.data['id_sousetab']
    users = Profil.objects.filter(sous_etabs__id=id_sousetab).order_by('rang')
    res = []

    for h in hierarchies:
        res.append({"libelle":h.libelle,"quota_cursus":h.quota_cursus})
    config = ConfigAnnee.objects.get(sous_etabs=id_sousetab)
    res.append({"libelle":config.appellation_formateur,"quota_cursus":config.pourcentage_cursus_enseignant})

    return Response(res)

@api_view(['POST'])
def update_user(request):

    id = request.data['id']
    username = request.data['username']
    # password = request.data['password']
    is_superuser = True if request.data['is_superuser']=="1" else False
    first_name = request.data['first_name']
    last_name = request.data['last_name']
    email = request.data['email']
    is_staff = True if request.data['is_staff']=="1" else False
    is_active = True if request.data['is_active']=="1" else False

    User.objects.filter(id=id).update(username=username,
        is_superuser=is_superuser,
        first_name=first_name,
        last_name=last_name,
        email=email,
        is_staff=is_staff,
        is_active=is_active
        )

    return Response({"status":"User Updated !"})

@api_view(['POST'])
def delete_user(request):
    id = int(request.data['id'])
    id_sousetab = request.data['id_sousetab']
    User.objects.filter(id=id).update(is_active=False)

    return Response({"status":1})

#################### CRUD ENSEIGNANT MATIERE SPECIALITE ####################

@api_view(['POST'])
def list_enseignant_matieres_specialites(request):
    id_sousetab = request.data['id_sousetab']
    sousetab = SousEtab.objects.get(id=id_sousetab)
    users = sousetab.users.all()
    print("USERS: ",users)
    matieres = Matiere.objects.filter(sous_etabs__id=id_sousetab).order_by('libelle')
    # ACTIVER
    # enseignants = Enseignant.objects.filter(sous_etabs__id=id_sousetab,is_active__in=[True])
    # enseignants = Enseignant.objects.filter(is_active__in=[True])

    matieres = MatiereSerializer(matieres,many=True).data

    # enseignant = Enseignant.objects.filter(users=user)
    id_spe1=""
    id_spe2=""
    id_spe3=""

    res = []

    # for ens in enseignants:
    for user in users:
        # user = ens.users.all()[0]
        ens = Enseignant.objects.filter(users__id=user.id,is_active__in=[True])
        if ens:
            ens = ens[0]
            liste_matieres_enseignees = ""
            id_matieres_enseignees = ""

            matieres_spe = ens.matiere_specialites.all()
            cpt_m = 1
            id_spe1 = matieres_spe[0].id if matieres_spe else ""
            id_spe2 = matieres_spe[1].id if len(matieres_spe)>1 else ""
            id_spe3 = matieres_spe[2].id if len(matieres_spe)>2 else ""
            for m in matieres_spe:
                if cpt_m < len(matieres_spe):
                    liste_matieres_enseignees+=m.libelle+","
                    id_matieres_enseignees+=str(m.id)+","
                else:
                    id_matieres_enseignees+=str(m.id)
                    liste_matieres_enseignees+=m.libelle
                cpt_m+=1
            res.append({"id":ens.id,"nom":user.first_name,"prenom":user.last_name,"id_user":user.id
                ,"id_spe1":id_spe1,"id_spe2":id_spe2,"id_spe3":id_spe3,
                "id_matieres_enseignees":id_matieres_enseignees,"liste_matieres_enseignees":liste_matieres_enseignees})

    return Response({"res":res,"matieres":matieres})


@api_view(['POST'])
def update_enseignant_matieres_specialites(request):
    id_sousetab = request.data['id_sousetab']
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""
    id_matiere1 = request.data['id_matiere1']
    id_matiere2 = request.data['id_matiere2']
    id_matiere3 = request.data['id_matiere3']
    # id_user = request.data['id_user']
    id = request.data['id']
    print(id_matiere1,id_matiere2,id_matiere3)
    id_matieres_spe = []
    id_matieres_list = []

    if id_matiere1 != "-1" and id_matiere1 != "":
        id_matieres_list.append(int(id_matiere1))
    if id_matiere2 != "-1" and id_matiere2 != "":
        id_matieres_list.append(int(id_matiere2))
    if id_matiere3 != "-1" and id_matiere3 != "":
        id_matieres_list.append(int(id_matiere3))

    matieres = Matiere.objects.filter(id__in=id_matieres_list)
    ens = Enseignant.objects.get(id=id)

    old_matieres = ens.matiere_specialites.all()

    for om in old_matieres:
        m = Matiere.objects.get(id=om.id)
        ens.matiere_specialites.remove(m)

    for mat in matieres:
        ens.matiere_specialites.add(mat)

    res,matieres = _list_enseignant_matieres_specialites(id_sousetab)
    return Response({"res":res,"matieres":matieres})

#################### REACTIVATION DES USERS DESACTIVES ####################

@api_view(['POST'])
def list_users_desactives(request):

    id_sousetab = request.data['id_sousetab']
    users = SousEtab.objects.get(id=id_sousetab).users.filter(is_active__in=[False]).order_by('first_name')
    res = []

    for u in users:
        profil = Profil.objects.get(user=u)
        res.append({"id":u.id,"nom":u.first_name,"prenom":u.last_name,"login":u.username,"sexe":profil.sexe,
            "email":u.email,"is_active":False})
    return Response(res)

@api_view(['POST'])
def update_user_desactive(request):

    # id = request.data['id']
    id_sousetab = request.data['id_sousetab']
    # User.objects.filter(id=id).update(is_active=True)

    id_users = request.data['id_users'].split(",")
    n = len(id_users)
    print(n,id_users)

    if n>2:
        id_users = id_users[1:-1]
        print(id_users)
        id_users = [int(idc) for idc in id_users]
        User.objects.filter(id__in=id_users).update(is_active=True)

    res = _list_users_desactives(id_sousetab)
    return Response(res)
#################### MESSAGE CLOUD ####################

@api_view(['POST'])
def send_message_mongo_atlas(request):
    username = urllib.parse.quote_plus('ulrichguebayi2')
    password = urllib.parse.quote_plus('ABCDEF2019.')

    uri = "mongodb+srv://%s:%s@cluster0-g0upo.mongodb.net/test?retryWrites=true" % (username, password)
    client = MongoClient(uri)
    # print(client)
    db = client["paiementdb"]

    data = db["paiement"]
    # annuaire = data.find({"status_paiement":1})
    # for document in annuaire:
    #     print(document)

    # query = {"_id": {"$in": ids}}
    query = {"status_paiement": {"$eq": 1}}
    newvalues = {"$set": {"status_paiement":2}}
    data.update_many(query, newvalues)

    # error = "error"
    # try:
    #     uri = "mongodb+srv://%s:%s@cluster0-g0upo.mongodb.net/test?retryWrites=true" % (username, password)
    #     client = MongoClient(uri)
    #     db = client["college_les_batisseurs"]
    #     lst = [{"email_pere":"ulrichguebayi@gmail.com","email_mere":"christellemotomo@gmail.com","infos":[{"matricule":"MA0002","nom":"GUEBAYI","prenom":"Corinne","classe":"4eAll","file_id":"1xImfupH-7ltO6CrWbyVpSBe4JOovslup","infos":"*somethin*well*parsed7*","date":"2019-06-10","emetteur":{"fonction":"Prof Anglais","nom":"Bouba Diop"}},{"matricule":"MA0002","nom":"GUEBATI","prenom":"Corinne","classe":"4eAll","file_id":"1xImfupH-7ltO6CrWbyVpSBe4JOovslup","infos":"*something*well*parsed8*","date":"2021-04-26","emetteur":{"fonction":"Prof PCT","nom":"Evina Samson"}}],"refresh":"2019-06-29"}]
    #     # lsts = lst*1000
    #     db.temp_messages.insert_many(lst);
    #     # for i in range(1000):
    #     #     db.temp_messages.insert_one({"email_pere":"ulrichguebayi@gmail.com","email_mere":"christellemotomo@gmail.com","infos":[{"matricule":"MA0002","nom":"GUEBAYI","prenom":"Corinne","classe":"4eAll","file_id":"1xImfupH-7ltO6CrWbyVpSBe4JOovslup","infos":"*somethin*well*parsed7*","date":"2019-06-10","emetteur":{"fonction":"Prof Anglais","nom":"Bouba Diop"}},{"matricule":"MA0002","nom":"GUEBATI","prenom":"Corinne","classe":"4eAll","file_id":"1xImfupH-7ltO6CrWbyVpSBe4JOovslup","infos":"*something*well*parsed8*","date":"2019-06-28","emetteur":{"fonction":"Prof PCT","nom":"Evina Samson"}}],"refresh":"2019-06-29"});  
    #     error = ""
    #     #     print('*** {}/1000'.format(i+1))
    #         # bar.update(i)
    # finally:
    #     print("******At the end error is: {}".format(error))

    return Response({"status":"Cloud, founded"})

#################### PAYEMENTS DES ELEVES ####################

@api_view(['POST'])
def list_payement_eleve(request):
    id_sousetab = request.data["id_sousetab"]
    id_classe = request.data["id_classe"]
    res = []
    type_pyts = []
    montant_total_a_payer = 0

    classe = Classe.objects.get(id=id_classe)
    eleves = classe.eleves.all()

    tps = TypePayementEleve.objects.filter(classes=classe,entree_sortie_caisee="e").order_by('date_deb','date_fin')
    print(tps)
    for tp in tps:
        montant_total_a_payer+= tp.montant
        type_pyts.append({"id":tp.id,"libelle":tp.libelle,"date_deb":tp.date_deb,"date_fin":tp.date_fin,
            "montant":tp.montant})

    for el in eleves:
        montant_verse = 0
        payements = PayementEleve.objects.filter(eleves=el).order_by('date')
        montant_verse = sum([p.montant for p in payements])
        cpt =1
        date_payement=""
        montants = ""
        n = len(payements)
        for pay in payements:
            if cpt<n:
                date_payement+= str(pay.date).split('T')[0]+","
                montants += str(pay.montant)+";"
            else:
                date_payement+= str(pay.date).split('T')[0]
                montants += str(pay.montant)
            cpt+=1


        res.append({"id":el.id,"matricule":el.matricule,"nom":el.nom,"prenom":el.prenom,
            "montant":montant_verse,"dates_payements":date_payement,"montants":montants})

    return Response({"eleves":res,"type_payements":type_pyts,"montant_total_a_payer":montant_total_a_payer})

@api_view(['POST'])
def update_payement_eleve(request):
    id_classe = request.data["id_classe"]
    id_eleve = request.data["id"]
    montant = request.data["montant"]

    eleve= Eleve.objects.get(id=id_eleve)
    # payements = PayementEleve.objects.filter(eleves=eleve)
    # if len(payements)>0:
    #     payements = payements[0]
    #     payements.montant += float(montant)
    #     payements.save()
    # else:
    payement = PayementEleve()
    payement.montant = montant
    payement.save()
    payement.eleves.add(eleve)

    res,type_pyts,montant_total_a_payer = _list_payement_eleve(id_classe)

    return Response({"eleves":res,"type_payements":type_pyts,"montant_total_a_payer":montant_total_a_payer})

#################### EMPLOI DE TEMPS ####################

@api_view(['POST'])
def get_current_emploi_de_temps(request):
    # em = EmploiDuTemps()
    # em.libelle = "7h30_8h20"
    # em.save()
    # em.jours_id.append(1)
    # em.save()
    # em = EmploiDuTemps.objects.filter(jours__id=1)
    # em[0].jours.add(Jour.objects.get(id=2))


    id_sousetab = request.data['id_sousetab']
    sousetab = SousEtab.objects.get(id=id_sousetab)
    classes = sousetab.classe_set.all()
    classes = ClasseSerializer(classes,many=True).data
    # matieres = Matiere.objects.filter(sous_etabs__id=id_sousetab).order_by('libelle')

    ListMatieres = []
    first_class_id = -1

    for c in classes:
        matieres = Matiere.objects.filter(classes_id=c['id']).order_by('libelle')
        nbre = len(matieres)
        cpt = 1
        ligne = ""
        for m in matieres:
            if cpt<nbre:
                ligne += m.libelle+"*"+str(m.id)+"_"
            else:
                ligne += m.libelle+"*"+str(m.id)
            cpt +=1
        ListMatieres.append(ligne)

    listProfs, matieres = _list_enseignant_matieres_specialites(id_sousetab)

    jours = sousetab.jour_set.all()
    TAB_JOURS = []
    TAB_PERIODES = []
    TAB_CRENEAU_PAUSE = []
    TAB_VALEUR_HORAIRE = []
    nb_tranches = 0
    tranches = []

    for j in jours:
        # On suppose que le premier jour est le plus chargé et on récupère les tranches horaires et les pauses
        tranches_horaires = j.tranchehoraire_set.all().order_by("id")
        if j.numero_jour ==1:
            nb_tranches = len(tranches_horaires)
            tranches = [1]*nb_tranches
            for t in tranches_horaires:
                # C'est une tranche
                if t.type_tranche == "0":
                    TAB_PERIODES.append({"id":t.id,"type":"0","duree":t.heure_deb+"_"+t.heure_fin})
                    if t.heure_deb not in TAB_VALEUR_HORAIRE:
                        TAB_VALEUR_HORAIRE.append(t.heure_deb)
                    if t.heure_fin not in TAB_VALEUR_HORAIRE:
                        TAB_VALEUR_HORAIRE.append(t.heure_fin)
                    # C'est une pause
                else:
                    TAB_PERIODES.append({"id":t.id,"type":"1","duree":"B_"+t.heure_deb+"_"+t.heure_fin})
                    TAB_CRENEAU_PAUSE.append(t.heure_deb+"_"+t.heure_fin)
        else:
            cpteur=0
            tranches = [0]*nb_tranches
            for t in tranches_horaires:
                tranches[cpteur]=1
                cpteur+=1
        TAB_JOURS.append({"id":j.id,"libelle":j.libelle,"numero_jour":j.numero_jour,"tranches":tranches})

    emploiDeTemps = EmploiDuTemps.objects.filter(sous_etabs__id=id_sousetab)
    res_emp = []
    for emp in emploiDeTemps:
        id_jour = 0
        id_tranche = 0
        id_classe = 0
        id_matiere = 0
        id_enseignants = []
        value = ""
        libelle = ""
        # Il faudra ajouter genre dans la table user

        jour = emp.jours.all()
        if jour:
            id_jour = jour[0].id
            value +=str(id_jour)+":"
        tranche = emp.tranche_horaires.all()
        if tranche:
            id_tranche = tranche[0].id
            value += tranche[0].heure_deb+"_"+tranche[0].heure_fin+"*"
            libelle = tranche[0].heure_deb+"_"+tranche[0].heure_fin
        classe = emp.classes.all()
        if classe:
            id_classe = classe[0].id
        matiere = emp.matieres.all()
        if matiere:
            id_matiere = matiere[0].id
            value += str(id_matiere)
        ens = emp.enseignants.all()
        if ens:
            id_enseignants = [e.id for e in ens]
            # value +="*"
            cpt = 0
            for e in ens:
                user = e.users.all()[0]
                value += "*Mr."+user.first_name+" "+user.last_name+"%prof_"+str(e.id)
                # if cpt>0:
                #     value += "|"
                cpt +=1
        res_emp.append({"libelle":libelle,"id_jour":id_jour,"id_tranche":id_tranche,"id_classe":id_classe,
            "id_matiere":id_matiere,"id_enseignants":id_enseignants,"value":value,"modify":""})

    return Response({"emploiDeTemps":res_emp,"classes":classes,"matieres":matieres,"ListMatieres":ListMatieres,
        "listProfs":listProfs,"TAB_JOURS":TAB_JOURS,"TAB_PERIODES":TAB_PERIODES,"TAB_CRENEAU_PAUSE":TAB_CRENEAU_PAUSE,
        "TAB_VALEUR_HORAIRE":TAB_VALEUR_HORAIRE})

@api_view(['POST'])
def set_emploi_de_temps(request):
    id_sousetab = request.data["id_sousetab"]
    emploiDeTemps = request.data["emploiDeTemps"]
    print(emploiDeTemps)
    for e in emploiDeTemps:
        heure_deb,heure_fin = e['libelle'].split("_")
        libelle = heure_deb+"_"+heure_fin
        id_jour = e['id_jour']
        id_classe = e['id_classe']
        id_matiere = e['id_matiere']
        id_enseignants = e['id_enseignants']
        value = e['value']
        modify = e['modify']
        # print(id_jour,id_classe,id_matiere,id_enseignants,value,modify,heure_deb,heure_fin)
        tranche = TrancheHoraire.objects.filter(sous_etabs__id=id_sousetab,jours__id=id_jour,heure_deb=heure_deb,heure_fin=heure_fin )
        # print(tranche)
        cours = Cours.objects.filter(classes__id=id_classe,matieres__id=id_matiere)
        # print(cours)
        ens = Enseignant.objects.filter(id__in=id_enseignants)
        # print(ens)
        # On se rassure que la tranche existe, normalement ça existe toujours
        # if len(ens)>0 and len(tranche)>0:
        if len(tranche)>0:
            tranche = tranche[0]
            jour = Jour.objects.get(id=id_jour)
            classe = Classe.objects.get(id=id_classe)
            matiere = Matiere.objects.get(id=id_matiere)
            sousetab = SousEtab.objects.get(id=id_sousetab)
            # C'est un emploi de temps à supprimer
            if modify.find("s")>-1:
                # print(e['libelle']," Suppresion")
                EmploiDuTemps.objects.filter(jours__pk=id_jour,classes__pk=id_classe,matieres__pk=id_matiere,libelle=libelle).delete()
                for en in ens:
                    en.handle_classes.remove(classe)
            # C'est un element à ajouter dans l'emploi du temps
            elif modify.find("c")>-1:
                # On créé le cours s'il n'existe pas déja en bd
                if len(cours)==0:
                    cours = Cours()
                    cours.libelle = classe.libelle+" - "+matiere.libelle
                    cours.save()
                    cours.classes.add(classe)
                    cours.matieres.add(matiere)
                    for e in ens:
                        cours.enseignants.add(e)
                else:
                    cours = cours[0]
                emp = EmploiDuTemps()
                # emp.libelle = e['libelle']
                emp.save()
                emp.sous_etabs.add(sousetab)
                emp.cours.add(cours)
                emp.tranche_horaires.add(tranche)
                emp.jours.add(jour)
                emp.classes.add(classe)
                emp.matieres.add(matiere)
                for en in ens:
                    emp.enseignants.add(en)
                    en.handle_classes.add(classe)
                # print(e['libelle']," Création")
            # Un enseignant a été ajouté au cours
            elif modify.find("e")>-1:
                emp = EmploiDuTemps.objects.filter(jours__pk=id_jour,classes__pk=id_classe,matieres__pk=id_matiere,libelle=libelle)[0]
                for en in ens:
                    emp.enseignants.add(en)
                    en.handle_classes.add(classe)
                # print(e['libelle']," Ajout Enseignant")

    return Response({"emplois":"Success"})

@api_view(['POST'])
def get_current_emploi_de_temps_prof(request):
    id_ens = request.data['id_ens']
    enseignant = Enseignant.objects.get(id=id_ens)
    emploiDeTemps = EmploiDuTemps.objects.filter(enseignants__id=id_ens).order_by('jours__numero_jour','tranche_horaires_id')
    res_emp = []
    for emp in emploiDeTemps:
        jour = emp.jours.all()[0]
        classe = emp.classes.all()[0]
        matiere = emp.matieres.all()[0]
        res_emp.append({"jour":jour.libelle,"id_jour":jour.id,"numero_jour":jour.numero_jour,"heure":emp.libelle,
            "classe":classe.libelle,"id_classe":classe.id,
            "matiere":matiere.libelle,"id_matiere":matiere.id,})

    return Response({"emploiDeTemps":res_emp})

@api_view(['POST'])
def get_current_emploi_de_temps_classe(request):
    id_classe = request.data['id_classe']
    classe = Classe.objects.get(id=id_classe)
    emploiDeTemps = EmploiDuTemps.objects.filter(classes__id=id_classe).order_by('jours__numero_jour','tranche_horaires_id')
    res_emp = []
    for emp in emploiDeTemps:
        jour = emp.jours.all()[0]
        enseignants = emp.enseignants.all()
        profs = []
        for ens in enseignants:
            user = ens.users.all()[0]
            profs.append({"nom":user.first_name,"prenom":user.last_name,"id_ens":ens.id})
        matiere = emp.matieres.all()[0]
        res_emp.append({"jour":jour.libelle,"id_jour":jour.id,"numero_jour":jour.numero_jour,"heure":emp.libelle,
            "profs":profs,
            "matiere":matiere.libelle,"id_matiere":matiere.id,})
        # res_emp = sorted(res_emp, key=lambda k: k['numero_jour'])
    return Response({"emploiDeTemps":res_emp})


######################################## REQUETES LIEES A CURSUS PROF ########################################

@api_view(['GET'])
def tester_wifi(request):
    return Response({"known_wifi":"well_known"})



@api_view(['POST'])
def init_cursus_prof_etab(request):
    id_ens = request.data["id_ens"]
    sequences = []
    ens = Enseignant.objects.get(id=id_ens)
    # génération du code de l'enseignant
    code_ens = generate_random_string()
    # lecture de l'emploi du temps du prof
    emploiDeTemps = get_current_emploi_de_temps_prof(id_ens)
    # détermination de la liste des classes puis des cours et liste des élèves par classes
    classes = ens.handle_classes.all()
    print("classes du prof: ",classes)
    classes = [Classe.objects.get(id=1)]
    for cl in classes:
        sousetab = cl.sous_etabs.all()[0]
        print("sousetab de la classe: ",sousetab)
    # sélection des cahiers de texte
    # sélection des évaluations
    # sélection des notes déjà saisies
    return Response({"init":"ok"})

