from rest_framework import serializers
# from .models import File, Eleve, Cycle, BulletinSeqTrimEleve, BulletinSeqTrimNoteRecap, BulletinSeqTrimGroupeNoteRecap, BulletinSeqTrimRecapTotal, Etab
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self,attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

class FileSerializer(serializers.ModelSerializer):
  class Meta():
    model = File
    fields = ('file', 'description', 'file_type', 'timestamp')

class EleveSerializer(serializers.ModelSerializer):
  class Meta():
    model = Eleve
    fields = '__all__'

class CycleSerializer(serializers.ModelSerializer):
  class Meta():
    model = Cycle
    fields = ["id","libelle","code"]
    # fields = '__all__'

class BulletinSeqTrimEleveSerializer(serializers.ModelSerializer):
  class Meta():
    model = BulletinSeqTrimEleve
    fields = ('id','resultat', 'rang')

class BulletinSeqTrimNoteRecapSerializer(serializers.ModelSerializer):
  class Meta():
    model = BulletinSeqTrimNoteRecap
    fields = ('id','resultat','rang')

class BulletinSeqTrimGroupeNoteRecapSerializer(serializers.ModelSerializer):
  class Meta():
    model = BulletinSeqTrimGroupeNoteRecap
    fields = ('id','resultat')

class BulletinSeqTrimRecapTotalSerializer(serializers.ModelSerializer):
  class Meta():
    model = BulletinSeqTrimRecapTotal
    fields = ('id','resultat')

class EtabSerializer(serializers.ModelSerializer):
  class Meta():
    model = Etab
    # fields = '__all__'
    fields = ('id','libelle','date_creation','nom_fondateur','devise','localisation','bp','email','tel','langue','site_web','logo','logo_url')

class SousEtabSerializer(serializers.ModelSerializer):
  class Meta():
    model = SousEtab
    # fields = '__all__'
    fields = ('id','libelle','type_sousetab','date_creation','nom_fondateur','devise','localisation','bp','email','tel','langue','site_web','logo_url')
    # exclude = ["type_sousetab","users","groups","emploi_du_temps_deja_configure","deja_configure","etabs"]

class NiveauSerializer(serializers.ModelSerializer):
  class Meta():
    model = Niveau
    fields = ["id","libelle","code"]
    # fields = '__all__'

class ClasseSerializer(serializers.ModelSerializer):
  class Meta():
    model = Classe
    fields = ["id","libelle","code"]
    # fields = '__all__'

class SpecialiteClasseSerializer(serializers.ModelSerializer):
  class Meta():
    model = SpecialiteClasse
    fields = ["id","libelle","code"]
    # fields = '__all__'

class MatiereSerializer(serializers.ModelSerializer):
  class Meta():
    model = Matiere
    fields = ["id","libelle","code"]
    # fields = '__all__'

class ConfigAnneeSerializer(serializers.ModelSerializer):
  class Meta():
    model = ConfigAnnee
    # fields = ["id","libelle","is_active"]
    fields = '__all__'

# class CoursSerializer(serializers.ModelSerializer):
#   class Meta():
#     model = Cours
#     fields = ["id","libelle","description","coef","volume_horaire_hebdo","volume_horaire_annuel"]
