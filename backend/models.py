from djongo import models

from django.contrib.auth.models import User, Group

# lets us explicitly set upload path and filename
def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class PredefinedRole(models.Model):
    # type_role peut être secondaire, primaire...
    type_role = models.CharField(max_length=20, default='secondaire')
    libelle = models.CharField(max_length=100)
    accreditation = models.IntegerField()

    groupes = models.ArrayReferenceField(
        to=Group,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class Etab(models.Model):

    libelle = models.CharField(max_length=100)
    date_creation = models.DateField(blank=True, null=True)
    nom_fondateur = models.CharField(max_length=200, blank=True)
    localisation = models.CharField(max_length=200, blank=True)
    bp = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    devise = models.CharField(max_length=100, blank=True)
    # logo = models.CharField(max_length=300)
    logo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    logo_url = models.TextField(blank=True, null=True)
    langue = models.CharField(max_length=100)
    site_web = models.CharField(max_length=200, blank=True)
    deja_configure = models.BooleanField(default=False)
    same_matricule_sousetab = models.BooleanField(default=False)

    format_matricule = models.CharField(max_length=3,default="")
    mat_fixed = models.CharField(max_length=10,default="", blank=True)
    mat_number_size = models.IntegerField(default=5)
    mat_number_last = models.IntegerField(default=0)
    mat_year = models.CharField(max_length=4,default="")
    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class SousEtab(models.Model):
    libelle = models.CharField(max_length=100)
    # type_sousetab peut etre primaire ou secondaire
    type_sousetab = models.CharField(max_length=100, default="secondaire")
    date_creation = models.DateField(blank=True, null=True)
    nom_fondateur = models.CharField(max_length=200, blank=True)
    localisation = models.CharField(max_length=200)
    bp = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    devise = models.CharField(max_length=100, blank=True)
    langue = models.CharField(max_length=100, blank=True)
    chemin_logo = models.TextField(blank=True, null=True)
    logo_url = models.TextField(blank=True, null=True)
    site_web = models.CharField(max_length=100, blank=True)

    deja_configure = models.BooleanField(default=False)
    emploi_du_temps_deja_configure = models.BooleanField(default=False)

    etabs = models.ArrayReferenceField(
        to=Etab,
        on_delete=models.PROTECT,
    )
    groups = models.ArrayReferenceField(
        to=Group,
        on_delete=models.CASCADE,
        default=[]
    )
    users = models.ArrayReferenceField(
        to=User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class AnneeScolaire(models.Model):
    libelle = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)

    etabs = models.ArrayReferenceField(
        to=Etab,
        on_delete=models.CASCADE,
    )
    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['-pk']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class Profil(models.Model):
    sexe = models.CharField(max_length=1, default='M')
    tel1 = models.CharField(max_length=20)
    tel2 = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    date_entree = models.CharField(max_length=10)
    date_sortie = models.CharField(max_length=10)

    user = models.OneToOneField(User,on_delete=models.CASCADE,)

    def __str__(self):
        return self.tel1

    objects = models.DjongoManager()

class Jour(models.Model):
    libelle = models.CharField(max_length=100)
    code = models.CharField(max_length=10, blank=True)
    heure_deb_cours = models.CharField(max_length=10, default="")
    heure_fin_cours = models.CharField(max_length=10, default="")
    numero_jour = models.IntegerField()

    annee_scolaires = models.ArrayReferenceField(
        to=AnneeScolaire,
        on_delete=models.CASCADE,
    )
    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['annee_scolaires__pk', 'numero_jour']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class Pause(models.Model):
    libelle = models.CharField(max_length=100)
    duree = models.IntegerField(default=0)

    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class TrancheHoraire(models.Model):
    libelle = models.CharField(max_length=100)
    heure_deb = models.CharField(max_length=10)
    heure_fin = models.CharField(max_length=10)
    # Pour ordnonner les tranches du matin au soir
    numero_tranche = models.IntegerField(default=0)
    # Permet de savoir si c'est une tranche (ie 0) ou une pause au quel cas il contient l'id de la pause
    type_tranche = models.CharField(default="0",max_length=10)
    # Contient éventuellement le nom de la pause, il faudra update atomiqmen type_tranche et nom_pause

    jours = models.ArrayReferenceField(
        to=Jour,
        on_delete=models.CASCADE,
    )
    annee_scolaires = models.ArrayReferenceField(
        to=AnneeScolaire,
        on_delete=models.CASCADE,
    )
    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE,
    )
    # class Meta:
    #   ordering = ['annee_scolaires__pk', 'jours__pk', 'numero_tranche']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class ConfigAnnee(models.Model):
    libelle = models.CharField(max_length=100)
    taux_cursus = models.FloatField(default=20000)
    pourcentage_cursus_enseignant = models.FloatField(default=50)
    heure_envoi_msg_cursus = models.CharField(max_length=10,default="15h35")
    date_deb = models.DateField()
    date_fin = models.DateField()
    langue = models.CharField(max_length=100)
    duree_periode = models.FloatField()
    nombre_trimestres = models.IntegerField()
    nombre_sequences = models.IntegerField()
    notation_sur = models.FloatField()
    format_bulletin = models.CharField(max_length=100, blank=True)
    bulletin_base_sur = models.CharField(max_length=100, blank=True)
    has_group_matiere = models.BooleanField(default=True)
    position = models.CharField(max_length=30, blank=True)
    appellation_bulletin = models.CharField(max_length=200, blank=True)
    options_arrondi_notes = models.TextField(default="0.25²²0.5²²0.75")
    appellation_coef = models.CharField(max_length=100)
    appellation_apprenant = models.CharField(max_length=100, blank=True)
    appellation_formateur = models.CharField(max_length=100, blank=True)
    appellation_sequence = models.CharField(max_length=100, blank=True)
    appellation_module = models.CharField(max_length=100, blank=True)
    appellation_chapitre = models.CharField(max_length=100, blank=True)
    appellation_lecon = models.CharField(max_length=100, blank=True)
    abbreviation_module = models.CharField(max_length=10, blank=True)
    abbreviation_chapitre = models.CharField(max_length=10, blank=True)
    abbreviation_lecon = models.CharField(max_length=10, blank=True)
    utilise_coef = models.CharField(max_length=50)
    matricule_auto_genere = models.BooleanField(default=True)

    # format_matricule peut être FNY: Fixed,Number,Year....NFY...
    format_matricule = models.CharField(max_length=3)
    mat_fixed = models.CharField(max_length=10, blank=True)
    mat_number_size = models.IntegerField(default=5)
    mat_number_last = models.IntegerField(default=0)
    mat_year = models.CharField(max_length=4)
    matricule_deja_attribues = models.BooleanField(default=False)

    annee_scolaires = models.ArrayReferenceField(
        to=AnneeScolaire,
        on_delete=models.CASCADE,
    )
    jours = models.ArrayReferenceField(
        to=Jour,
        on_delete=models.CASCADE,
    )
    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['-annee_scolaires__pk','sous_etabs__pk', '-pk']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class Cycle(models.Model):
    libelle = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    etabs = models.ArrayReferenceField(
        to=Etab,
        on_delete=models.CASCADE,
    )
    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['sous_etabs', 'libelle']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class Niveau(models.Model):
    libelle = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    is_niveau_classes_examen = models.BooleanField(default=False)

    etabs = models.ArrayReferenceField(
        to=Etab,
        on_delete=models.CASCADE,
    )
    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE,
    )
    cycles = models.ArrayReferenceField(
        to=Cycle,
        on_delete=models.CASCADE,
    )
    
    # class Meta:
    #   ordering = ['sous_etabs__pk', 'cycles__pk', 'libelle']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class Eleve(models.Model):
    matricule = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    prenom = models.CharField(max_length=150, blank=True)
    sexe = models.CharField(max_length=1, default='M')
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100)
    date_entree = models.CharField(max_length=100)
    nom_pere = models.CharField(max_length=100)
    prenom_pere = models.CharField(max_length=100, blank=True)
    nom_mere = models.CharField(max_length=100)
    prenom_mere = models.CharField(max_length=100, blank=True)
    tel_pere = models.CharField(max_length=20)
    tel_mere = models.CharField(max_length=20)
    email_pere = models.CharField(max_length=100)
    email_mere = models.CharField(max_length=100)
    photo_url = models.CharField(max_length=300, blank=True)
    redouble = models.BooleanField(default=False)
    age = models.IntegerField()
    
    # bourse = models.FloatField(default=0)
    # excedent : ce qui est en plus lorsque l'eleve a tout payé
    # excedent = models.FloatField(default=0)
    # compte = models.FloatField(default=0)
    # Pr savoir si l'élève a payé la pension pr l'année en cours
    est_en_regle = models.BooleanField(default=False)

    def __str__(self):
        return self.nom+" _ "+self.prenom

    objects = models.DjongoManager()

class TypeEnseignant(models.Model):
    libelle = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    est_paye_a_l_heure = models.BooleanField(default=False)
    montant_quota_horaire = models.FloatField(blank=True)
    rang = models.IntegerField(default=0)
    # Le poucentage de ce type enseignant dans les gains cursus
    quota_cursus = models.FloatField(default=0)
    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class Classe(models.Model):
    libelle = models.CharField(max_length=100)
    code = models.CharField(max_length=30)
    total_coefs = models.FloatField(default=0)
    nombre_eleves = models.IntegerField(default=0)
    is_classes_examen = models.BooleanField(default=False)
    matricule_deja_attribues = models.BooleanField(default=False)

    etabs = models.ArrayReferenceField(
        to=Etab,
        on_delete=models.CASCADE,
    )
    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE,
    )
    cycles = models.ArrayReferenceField(
        to=Cycle,
        on_delete=models.CASCADE,
    )
    niveaux = models.ArrayReferenceField(
        to=Niveau,
        on_delete=models.CASCADE,
    )
    eleves = models.ArrayReferenceField(
        to=Eleve,
        on_delete=models.CASCADE,
    )

    # # class Meta:
    # #   ordering = ['sous_etabs__pk', 'cycles__pk', 'niveaux__pk', 'nom_classe']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class Matiere(models.Model):
    libelle = models.CharField(max_length=150)
    code = models.CharField(max_length=100,)

    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE,
    )
    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class Enseignant(models.Model):
    # prenom = models.CharField(max_length=100, blank=True)
    # sexe = models.CharField(max_length=20, default='masculin')
    # tel1 = models.CharField(max_length=20)
    # tel2 = models.CharField(max_length=20, blank=True)
    # email = models.CharField(max_length=150)
    # matiere_specialisation1 = models.CharField(max_length=100)
    # matiere_specialisation2= models.CharField(max_length=100, blank=True)
    # matiere_specialisation3= models.CharField(max_length=100, blank=True)
    # date_entree = models.DateField()
    # date_sortie = models.DateField()
    code_ens = models.CharField(max_length=25,default='')
    is_active = models.BooleanField()

    # user = models.OneToOneField(User, on_delete=models.CASCADE,)
    users = models.ArrayReferenceField(
        to=User,
        on_delete=models.CASCADE,
    )
    type_enseignant = models.ArrayReferenceField(
        to=TypeEnseignant,
        on_delete=models.CASCADE,
    )
    matiere_specialites = models.ArrayReferenceField(
        to=Matiere,
        on_delete=models.CASCADE,
    )
    handle_classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE,
    )
    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE,
        default=[1]
    )


    def __str__(self):
        return str(self.id)

    objects = models.DjongoManager()

class SpecialiteClasse(models.Model):
    # specialite correspond à Scientifique,...
    libelle = models.CharField(max_length=200)
    code = models.CharField(max_length=20)

    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE,
    )
    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class Trimestre(models.Model):
    libelle = models.CharField(max_length=200)
    numero = models.IntegerField(default=0)
    date_deb = models.DateField()
    date_fin = models.DateField()
    is_active = models.BooleanField(default=False)

    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE, 
    )

    # class Meta:
    #   ordering = ['numero']
    
    def __str__(self):
        return self.libelle
    objects = models.DjongoManager()

class Cours(models.Model):
    libelle = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    code = models.IntegerField(default=1)
    coef = models.FloatField()
    volume_horaire_hebdo = models.CharField(max_length=10)
    volume_horaire_annuel = models.CharField(max_length=10)

    matieres = models.ArrayReferenceField(
        to=Matiere,
        on_delete=models.CASCADE, 
    )
    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE, 
    )
    enseignants = models.ArrayReferenceField(
        to=Enseignant,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['classes__pk', 'matieres__pk']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class GroupeMatiere(models.Model):
    libelle = models.CharField(max_length=200)
    code = models.CharField(max_length=15)
    groupe_matiere_de_specialite = models.BooleanField(default=False)
    total_coefs = models.FloatField(default=0)
    
    matieres = models.ArrayReferenceField(
        to=Matiere,
        on_delete=models.CASCADE,
    )
    cours = models.ArrayReferenceField(
        to=Cours,
        on_delete=models.CASCADE,
    )
    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['-id','libelle']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class Sequence(models.Model):
    libelle = models.CharField(max_length=200)
    numero = models.IntegerField()
    date_deb = models.DateField()
    date_fin = models.DateField()
    is_active = models.BooleanField(default=False)
    trimestres = models.ArrayReferenceField(
        to=Trimestre,
        on_delete=models.CASCADE,
    )
    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['numero']
    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class FicheDeProgression(models.Model):
    module = models.TextField()
    chapitre = models.TextField()
    lecon = models.TextField()
    date_deb = models.CharField(max_length=10)
    date_fin = models.CharField(max_length=10)
    # status peut être 0:non commencé 1:commencée 2 achevée
    status = models.IntegerField(default=0)

    cours = models.ArrayReferenceField(
        to=Cours,
        on_delete=models.CASCADE,
    )

    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['annee_scolaires__pk','cours__pk']

    def __str__(self):
        return self.module

    objects = models.DjongoManager()

class CahierDeTexte(models.Model):
    date = models.CharField(max_length=10)
    jour = models.CharField(max_length=100)
    heure_deb = models.CharField(max_length=10)
    heure_fin = models.CharField(max_length=10)
    # module,chapitre,lecon sont prévues au cas ou la fiche de progression n'est pas upload
    module = models.TextField()
    chapitre = models.TextField()
    lecon = models.TextField()
    contenu = models.TextField()
    mot_cles = models.TextField()
    taux_progression = models.IntegerField(default=0)

    cours = models.ArrayReferenceField(
        to=Cours,
        on_delete=models.CASCADE,
    )

    fiche_progression = models.ArrayReferenceField(
        to=FicheDeProgression,
        on_delete=models.CASCADE,
    )
    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE,
    )

    def __str__(self):
            return self.module+" "+self.chapitre+" "+self.lecon
    objects = models.DjongoManager()

class ManuelScolaire(models.Model):
    libelle = models.CharField(max_length=300)
    description = models.TextField()
    prix = models.FloatField()

    cours = models.ArrayReferenceField(
        to=Cours,
        on_delete=models.CASCADE,
    )
    annee_scolaires = models.ArrayReferenceField(
        to=AnneeScolaire,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['annee_scolaires__pk','cours__pk']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class AbsenceEleve(models.Model):
    libelle = models.CharField(max_length=100)
    jour = models.CharField(max_length=100) # Lundi, Mardi, ...    
    date = models.DateField() # 2019-12-02    

    tranche_horaires = models.ArrayReferenceField(
        to=TrancheHoraire,
        on_delete=models.CASCADE,
    )
    cours = models.ArrayReferenceField(
        to=Cours,
        on_delete=models.CASCADE,
    )
    # Concerne un eleve
    eleves = models.ArrayReferenceField(
        to=Eleve,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['date']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class AppreciationNote(models.Model):
    libelle = models.CharField(max_length=100)

    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return str(self.libelle)

# Utilisé dans le cas ou il y a +sieurs notes pour une séquence
class SousNote(models.Model):
    score = models.FloatField(blank = True)
    numero = models.IntegerField(default=1)

    def __str__(self):
        return str(self.score)

    objects = models.DjongoManager()

class Note(models.Model):
    score = models.FloatField()
    scorexcoef= models.FloatField(blank = True)
    # note_min = models.FloatField(default=0)
    # note_max = models.FloatField(default=0)
    appreciation_notes = models.CharField(max_length=100)
    # Le rang de l'élève dans la matiere pour l'évaluation considéée
    rang = models.IntegerField(default=0)
    # Pour savoir si l'élève a une note et qu'elle est prise en compte pr les stats de la classe
    est_pris_en_compte = models.BooleanField(default=True)

    # Une note correspond a un eleve
    eleves = models.ArrayReferenceField(
        to=Eleve,
        on_delete=models.CASCADE,
    )
    sequences = models.ArrayReferenceField(
        to=Sequence,
        on_delete=models.CASCADE,
    )
    # trimestre est défini si c'est une note trimestrielle
    trimestres = models.ArrayReferenceField(
        to=Trimestre,
        on_delete=models.CASCADE,
    )
    cours = models.ArrayReferenceField(
        to=Cours,
        on_delete=models.CASCADE,
    )
    # appreciation_notes = models.ArrayReferenceField(
    #     to=AppreciationNote,
    #     on_delete=models.CASCADE,
    # )
    groupes = models.ArrayReferenceField(
        to=GroupeMatiere,
        on_delete=models.CASCADE,
    )
    # Lié au fait que dans une séquence on peut avoir plusieurs sous notes
    sous_notes = models.ArrayReferenceField(
        to=SousNote,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['sequences__pk', 'cours__pk', 'eleves__pk']

    def __str__(self):
        return str(self.score)

    objects = models.DjongoManager()

# Contient les infos relatives a une sequence dans un cours donné
class InfoNoteClasseMatiereSequence(models.Model):
    # quota_notes est sous la forme "70%²²30%²²" ou "13²²7"
    quota_notes = models.CharField(max_length=200)
    competence_visee = models.CharField(max_length=400)
    total_coef = models.FloatField(default=0)
    moy = models.FloatField()
    note_min = models.FloatField(default=0)
    note_max = models.FloatField(default=0)
    appreciation_notes = models.CharField(max_length=100)
    nb_eleves = models.IntegerField()

    sequences = models.ArrayReferenceField(
        to=Sequence,
        on_delete=models.CASCADE, 
    )
    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE, 
    )
    cours = models.ArrayReferenceField(
        to=Cours,
        on_delete=models.CASCADE, 
    )


    def __str__(self):
        return "["+self.moy+" - "+self.note_min+"] "

    objects = models.DjongoManager()

class NoteClasseMatiereTrimestre(models.Model):
    competence_visee = models.CharField(max_length=400)
    total_coef = models.FloatField(default=0)
    moy = models.FloatField()
    note_min = models.FloatField(default=0)
    note_max = models.FloatField(default=0)
    appreciation_notes = models.CharField(max_length=100)
    nb_eleves = models.IntegerField()

    trimestres = models.ArrayReferenceField(
        to=Trimestre,
        on_delete=models.CASCADE, 
    )
    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE, 
    )
    cours = models.ArrayReferenceField(
        to=Cours,
        on_delete=models.CASCADE, 
    )

    def __str__(self):
        return "["+self.moy+" - "+self.note_min+"] "

    objects = models.DjongoManager()

class RecapitulatifGroupeMatiereSequenceEleve(models.Model):
    # cours_note_min = models.FloatField()
    # cours_note_max = models.FloatField()
    total_coef = models.FloatField(default=0)
    moy = models.FloatField()
    score = models.FloatField(default=0)
    nxc = models.FloatField()
    rang = models.IntegerField(default=0)
    appreciation_notes = models.CharField(max_length=100)
    est_classe = models.BooleanField(default=True)


    eleves = models.ArrayReferenceField(
        to=Eleve,
        on_delete=models.CASCADE, 
    )
    groupes = models.ArrayReferenceField(
        to=GroupeMatiere,
        on_delete=models.CASCADE, 
    )
    sequences = models.ArrayReferenceField(
        to=Sequence,
        on_delete=models.CASCADE, 
    )
    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE, 
    )

    def __str__(self):
        return "["+self.moy+" - "+self.rang+"] "

    objects = models.DjongoManager()

class RecapitulatifGroupeMatiereTrimestreEleve(models.Model):
    total_coef = models.FloatField(default=0)
    moy = models.FloatField()
    score = models.FloatField(default=0)
    nxc = models.FloatField()
    rang = models.IntegerField(default=0)
    appreciation_notes = models.CharField(max_length=100)
    est_classe = models.BooleanField(default=True)

    eleves = models.ArrayReferenceField(
        to=Eleve,
        on_delete=models.CASCADE, 
    )
    groupes = models.ArrayReferenceField(
        to=GroupeMatiere,
        on_delete=models.CASCADE, 
    )
    trimestres = models.ArrayReferenceField(
        to=Trimestre,
        on_delete=models.CASCADE, 
    )
    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE, 
    )

    def __str__(self):
        return "["+self.moy+" - "+self.rang+"] "

class RecapitulatifGroupeMatiereSequence(models.Model):
    note_min = models.FloatField()
    note_max = models.FloatField()
    total_coef = models.FloatField(default=0)
    moy = models.FloatField()
    nxc = models.FloatField()
    appreciation_notes = models.CharField(max_length=100)
    est_classe = models.BooleanField(default=True)


    # appreciation_notes = models.ArrayReferenceField(
    #     to=AppreciationNote,
    #     on_delete=models.CASCADE, 
    # )
    groupes = models.ArrayReferenceField(
        to=GroupeMatiere,
        on_delete=models.CASCADE, 
    )
    sequences = models.ArrayReferenceField(
        to=Sequence,
        on_delete=models.CASCADE, 
    )
    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE, 
    )

    def __str__(self):
        return "["+self.moy+" - "+self.rang+"] "

    objects = models.DjongoManager()

class RecapitulatifTotalSequence(models.Model):
    note_max = models.FloatField()
    note_min = models.FloatField()
    taux_reussite_classe = models.FloatField()
    moyenne = models.FloatField()
    nombre_moyenne = models.IntegerField()
    nombre_eleves = models.IntegerField()

    sequences = models.ArrayReferenceField(
        to=Sequence,
        on_delete=models.CASCADE, 
    )
    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE, 
    )

    def __str__(self):
        return str(self.nombre_moyenne)

    objects = models.DjongoManager()

class RecapitulatifTotalTrimestre(models.Model):
    note_max = models.FloatField()
    note_min = models.FloatField()
    taux_reussite_classe = models.FloatField()
    moyenne = models.FloatField()
    nombre_moyenne = models.IntegerField()
    nombre_eleves = models.IntegerField()

    trimestres = models.ArrayReferenceField(
        to=Trimestre,
        on_delete=models.CASCADE, 
    )
    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE, 
    )

    def __str__(self):
        return str(self.nombre_moyenne)

    objects = models.DjongoManager()

class ResultatEleveSequence(models.Model):
    total_points = models.FloatField()
    total_coefs = models.FloatField()
    moyenne = models.FloatField()
    nxc = models.FloatField(default=0)
    est_classe = models.BooleanField(default=True)
    rang = models.IntegerField(default=True)
    appreciation = models.CharField(max_length=200)

    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE,
    )
    eleves = models.ArrayReferenceField(
        to=Eleve,
        on_delete=models.CASCADE,
    )
    sequences = models.ArrayReferenceField(
        to=Sequence,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return "["+str(self.moyenne)+" - "+str(self.total_points)+"] "

    objects = models.DjongoManager()

class ResultatEleveTrimestre(models.Model):
    total_points = models.FloatField()
    total_coefs = models.FloatField()
    moyenne = models.FloatField()
    est_classe = models.BooleanField(default=True)
    moyenne = models.FloatField()
    rang = models.IntegerField(default=True)

    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE,
    )
    eleves = models.ArrayReferenceField(
        to=Eleve,
        on_delete=models.CASCADE,
    )
    trimestres = models.ArrayReferenceField(
        to=Trimestre,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return "["+str(self.moyenne)+" - "+str(self.total_points)+"] "

    objects = models.DjongoManager()

# Contient les infos calculées propres aux eleves pr produire les bulletins des séquences et trimestre facilement
class BulletinSeqTrimEleve(models.Model):
    # si une note est modifiée pr la classe et l'évaluation considérée on positionne to_update à True
    to_update = models.BooleanField(default=True)
    resultat = models.TextField()
    rang = models.IntegerField(default=0)

    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE,
    )
    eleves = models.ArrayReferenceField(
        to=Eleve,
        on_delete=models.CASCADE,
    )
    sequences = models.ArrayReferenceField(
        to=Sequence,
        on_delete=models.CASCADE,
    )
    trimestres = models.ArrayReferenceField(
        to=Trimestre,
        on_delete=models.CASCADE,
    )
    ordering = ['rang']
    def __str__(self):
        return self.resultat

    objects = models.DjongoManager()

# Contient les infos recap note calculées pr produire les bulletins des séquences et trimestre facilement
# note_recap += "~~"+str(coefs[cpt_cours])+"²²"+str(min_note_matiere)+"²²"+str(max_note_matiere)+"²²"+str(moy_note_matiere)
class BulletinSeqTrimNoteRecap(models.Model):
    # si une note est modifiée pr la classe et l'évaluation considérée on positionne to_update à True
    to_update = models.BooleanField(default=True)
    resultat = models.TextField()

    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE,
    )
    sequences = models.ArrayReferenceField(
        to=Sequence,
        on_delete=models.CASCADE,
    )
    trimestres = models.ArrayReferenceField(
        to=Trimestre,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.resultat

    objects = models.DjongoManager()

# Contient les infos recap note sur les groupes calculées pr produire les bulletins des séquences et trimestre facilement
# groupe_recap += "~~"+str(min_note_groupe)+"²²"+str(max_note_groupe)+"²²"+str(moy_note_groupe)
class BulletinSeqTrimGroupeNoteRecap(models.Model):
    # si une note est modifiée pr la classe et l'évaluation considérée on positionne to_update à True
    resultat = models.TextField()

    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE,
    )
    sequences = models.ArrayReferenceField(
        to=Sequence,
        on_delete=models.CASCADE,
    )
    trimestres = models.ArrayReferenceField(
        to=Trimestre,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.resultat

    objects = models.DjongoManager()

# Contient les infos recap seq  ou trim calculées pr produire les bulletins des séquences et trimestre facilement
    # seq_recap += "~~"+str(min_note_seq)+"²²"+str(max_note_seq)+"²²"+str(moy_note_seq)+"²²"+str(nombre_moyenne)+"²²"+str(taux_reussite_classe)+"²²"+str(nb_eleves)
class BulletinSeqTrimRecapTotal(models.Model):
    # si une note est modifiée pr la classe et l'évaluation considérée on positionne to_update à True
    resultat = models.TextField()

    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE,
    )
    sequences = models.ArrayReferenceField(
        to=Sequence,
        on_delete=models.CASCADE,
    )
    trimestres = models.ArrayReferenceField(
        to=Trimestre,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.resultat

    objects = models.DjongoManager()

# # Contient les infos calculées pr produire les bulletins des trimestres facilement
# class BulletinTrimestre(models.Model):
#     # si une note est modifiée pr la classe et l'évaluation considérée on positionne to_update à True
#     to_update = models.BooleanField(default=True)
#     resultat = models.TextField()

#     classes = models.ArrayReferenceField(
#         to=Classe,
#         on_delete=models.CASCADE,
#     )
#     eleves = models.ArrayReferenceField(
#         to=Eleve,
#         on_delete=models.CASCADE,
#     )
#     trimestres = models.ArrayReferenceField(
#         to=Trimestre,
#         on_delete=models.CASCADE,
#     )
#     def __str__(self):
#         return self.resultat

#     objects = models.DjongoManager()

class EmploiDuTemps(models.Model):
    # libelle contiendra le nom de la tranche ex: 7h30_8h20
    libelle = models.CharField(max_length=150, default="")

    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete = models.CASCADE,
    )

    cours = models.ArrayReferenceField(
        to=Cours,
        on_delete = models.CASCADE,
    )
    tranche_horaires = models.ArrayReferenceField(
        to=TrancheHoraire,
        on_delete = models.CASCADE,
    )
    jours = models.ArrayReferenceField(
        to=Jour,
        on_delete = models.CASCADE,
    )
    enseignants = models.ArrayReferenceField(
        to=Enseignant,
        on_delete = models.CASCADE,
    )
    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete = models.CASCADE,
    )
    matieres = models.ArrayReferenceField(
        to=Matiere,
        on_delete = models.CASCADE,
    )
    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class TypePayementEleve(models.Model):
    libelle = models.CharField(max_length=100)
    date_deb = models.DateField()
    date_fin = models.DateField()
    entree_sortie_caisee = models.CharField(max_length=1,default="e")
    montant = models.FloatField()

    # Permet de connaitre l'ordre de payement pour les classes concernées
    ordre_paiement = models.IntegerField()

    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete = models.CASCADE,
    )
    
    # class Meta:
    #   ordering = ['ordre_paiement']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class PayementEleve(models.Model):
    libelle = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True, blank=True)
    montant = models.FloatField()

    type_payement_eleves = models.ArrayReferenceField(
        to=TypePayementEleve,
        on_delete=models.CASCADE,
    )
    eleves = models.ArrayReferenceField(
        to=Eleve,
        on_delete=models.CASCADE,
    )
    # class Meta:
    #   ordering = ['date', 'eleves__pk']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class TypePayementEnseignant(models.Model):
    libelle = models.CharField(max_length=100)
    entree_sortie_caisee = models.CharField(max_length=1,default="s")
    montant = models.FloatField()

    type_enseignant = models.ArrayReferenceField(
        to=TypeEnseignant,
        on_delete=models.CASCADE,
    )

    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete = models.CASCADE,
    )

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class PayementEnseignant(models.Model):
    libelle = models.CharField(max_length=100)
    date = models.DateField()
    montant = models.FloatField()

    enseignants = models.ArrayReferenceField(
        to=Enseignant,
        on_delete=models.CASCADE,
    )
    type_payement_enseignants = models.ArrayReferenceField(
        to=TypePayementEnseignant,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['date']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class HierarchieEtab(models.Model):
    libelle = models.CharField(max_length=100)
    rang = models.IntegerField(default=0)
    is_adminstaff = models.IntegerField(default=1)
    # Le poucentage de cette hierarchie dans les gains cursus
    quota_cursus = models.FloatField(default=0.0)
    # Il y a une hierarchie "Enseignant" qui sera creee par defaut
    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE,
    )
    group = models.ArrayReferenceField(
        to=Group,
        on_delete=models.CASCADE,
        default=[]
    )

    # class Meta:
    #   ordering = ['rang']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class AdminStaff(models.Model):
    # tel1 = models.CharField(max_length=20)
    # tel2 = models.CharField(max_length=20, blank=True)
    # email = models.CharField(max_length=200)
    # date_entree = models.DateField()
    # date_sortie = models.DateField()
    is_active = models.BooleanField()

    # user = models.OneToOneField(User, on_delete=models.CASCADE,)

    users = models.ArrayReferenceField(
        to=User,
        on_delete=models.CASCADE,
    )
    hierarchie_etab = models.ArrayReferenceField(
        to=HierarchieEtab,
        on_delete=models.CASCADE,
    )
    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE,
    )
    # groups = models.ArrayReferenceField(
    #     to=Group,
    #     on_delete=models.CASCADE,
    #     default=[]
    # )
    handle_classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.is_active

    objects = models.DjongoManager()

class TypePayementAdminStaff(models.Model):
    libelle = models.CharField(max_length=100)
    entree_sortie_caisee = models.CharField(max_length=1,default="s")
    montant = models.FloatField()

    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete = models.CASCADE,
    )
    hierarchies = models.ArrayReferenceField(
        to=HierarchieEtab,
        on_delete = models.CASCADE,
    )
    admin_staffs = models.ArrayReferenceField(
        to=AdminStaff,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class PayementAdminStaff(models.Model):
    libelle = models.CharField(max_length=100)
    date = models.DateField()
    montant = models.FloatField()

    admin_staffs = models.ArrayReferenceField(
        to=AdminStaff,
        on_delete=models.CASCADE,
    )

    type_payement_admin_staffs = models.ArrayReferenceField(
        to=TypePayementAdminStaff,
        on_delete=models.CASCADE,
    )
    # class Meta:
    #   ordering = ['date']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class TypePayementDivers(models.Model):
    libelle = models.CharField(max_length=100)
    entree_sortie_caisee = models.CharField(max_length=1,default="e")
    montant = models.FloatField()
    # class Meta:
    #   ordering = ['libelle']
    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete = models.CASCADE,
    )
    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class PayementDivers(models.Model):
    libelle = models.CharField(max_length=100)
    date = models.DateField()
    montant = models.FloatField()

    sous_etabs = models.ArrayReferenceField(
        to=SousEtab,
        on_delete=models.CASCADE,
    )
    type_payement_divers = models.ArrayReferenceField(
        to=TypePayementDivers,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['date']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class Message(models.Model):
    infos = models.TextField()
    delivered = models.BooleanField(default=False)
    date = models.DateField()
    
    eleves = models.ArrayReferenceField(
        to=Eleve,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['eleves__pk']

    def __str__(self):
        return self.infos

    objects = models.DjongoManager()

class DocumentClasse(models.Model):
    libelle = models.CharField(max_length=200)
    chemin_fichier = models.CharField(max_length=300)
    date_upload = models.DateField()

    cours = models.ArrayReferenceField(
        to=Cours,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['cours__pk']

    def __str__(self):
        return self.libelle
    
    objects = models.DjongoManager()

class Chambre(models.Model):
    libelle = models.CharField(max_length=200)
    code = models.CharField(max_length=100)
    is_active = models.BooleanField()
    # Permet de savoir si la chambre est libre ou occupée
    status = models.BooleanField()
    nb_occupants_max = models.IntegerField(default=1)

    eleves = models.ArrayReferenceField(
        to=Eleve,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.libelle
    
    objects = models.DjongoManager()

class Bus(models.Model):
    libelle = models.CharField(max_length=200)
    code = models.CharField(max_length=100)
    is_active = models.BooleanField()

    def __str__(self):
        return self.libelle
    
    objects = models.DjongoManager()  

class Chauffeur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, blank=True)
    tel1 = models.CharField(max_length=20)
    tel2 = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=100)
    date_entree = models.DateField()
    date_sortie = models.DateField()
    is_active = models.BooleanField()

    bus = models.ArrayReferenceField(
        to=Bus,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.nom+" "+self.prenom

    objects = models.DjongoManager()

class Dortoir(models.Model):
    libelle = models.CharField(max_length=200)
    code = models.CharField(max_length=100)
    is_active = models.BooleanField()
    chambres = models.ArrayReferenceField(
        to=Chambre,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class TypeSanction(models.Model):
    libelle = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    sanction_sur_heure = models.BooleanField(default=False)
    sanction_sur_jours = models.BooleanField(default=False)
    sanction_sur_autre = models.BooleanField(default=True)
    nb_heures_min = models.DateTimeField(blank=True)
    nb_heures_max = models.DateTimeField(blank=True)
    nb_jours_min = models.FloatField(blank=True)
    nb_jours_max = models.FloatField(blank=True)

    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class Sanction(models.Model):
    description = models.TextField()
    date = models.DateField()

    type_sanctions = models.ArrayReferenceField(
        to=TypeSanction,
        on_delete=models.CASCADE,
    )
    eleves = models.ArrayReferenceField(
        to=Eleve,
        on_delete=models.CASCADE,
    )
    annee_scolaires = models.ArrayReferenceField(
        to=AnneeScolaire,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['annee_scolaires__pk', 'eleves__pk', 'type_sanctions__pk']

    def __str__(self):
        return self.description

    objects = models.DjongoManager()

class BilletSortie(models.Model):
    libelle = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    heure_deb = models.DateTimeField()
    heure_fin = models.DateTimeField()
    date_deb = models.DateField()
    date_fin = models.DateField()
    # Status passe a True s'il a ete utilise pour justifier des absences
    status = models.BooleanField(default=False)

    eleves = models.ArrayReferenceField(
        to=Eleve,
        on_delete=models.CASCADE,
    )
    annee_scolaires = models.ArrayReferenceField(
        to=AnneeScolaire,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['annee_scolaires__pk', 'eleves__pk']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class ResultatExamenOfficiel(models.Model):
    libelle = models.CharField(max_length=300)
    chemin_fichier = models.CharField(max_length=300)
    taux_reussite = models.FloatField()
    taux_reussite_garcons = models.FloatField()
    taux_reussite_filles = models.FloatField()

    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE,
    )
    annee_scolaires = models.ArrayReferenceField(
        to=AnneeScolaire,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['annee_scolaires__pk', 'classes__pk']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class ProfPrincipal(models.Model):
    libelle = models.CharField(max_length=300)

    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE,
    )
    enseignants = models.ArrayReferenceField(
        to=Enseignant,
        on_delete=models.CASCADE,
    )
    annee_scolaires = models.ArrayReferenceField(
        to=AnneeScolaire,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['annee_scolaires__pk', 'classes__pk']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class DecisionConseilClasse(models.Model):
    libelle = models.CharField(max_length=300)
    admis_en_classe_superieur = models.BooleanField(default=False)
    est_renvoye = models.BooleanField(default=False)
    motif_renvoi = models.TextField(blank=True)

    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE,
    )
    eleves = models.ArrayReferenceField(
        to=Eleve,
        on_delete=models.CASCADE,
    )
    annee_scolaires = models.ArrayReferenceField(
        to=AnneeScolaire,
        on_delete=models.CASCADE,
    )

    # class Meta:
    #   ordering = ['annee_scolaires__pk', 'classes__pk', 'eleves__pk']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class ConditionRenvoi(models.Model):
    libelle = models.CharField(max_length=200)
    nb_heures_max = models.FloatField(default=0)
    age = models.FloatField(default=0)
    moyenne = models.FloatField(default=0)
    nb_jours = models.FloatField(default=0)

    annee_scolaires = models.ArrayReferenceField(
        to=AnneeScolaire,
        on_delete=models.CASCADE,
    )
    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class ConditionSucces(models.Model):
    libelle = models.CharField(max_length=200)
    moyenne = models.FloatField(default=0)
    
    annee_scolaires = models.ArrayReferenceField(
        to=AnneeScolaire,
        on_delete=models.CASCADE,
    )
    classes = models.ArrayReferenceField(
        to=Classe,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class CommuniqueAdministratif(models.Model):
    libelle = models.CharField(max_length=300)
    Description = models.TextField()
    date = models.DateField()
    date_debut_validite = models.DateField()
    date_fin_validite = models.DateField()
    emetteur = models.ArrayReferenceField(
        to=AdminStaff,
        on_delete=models.CASCADE,
    )
    # portee peut etre Etab, sousEtab,...,Classe, Enseignant
    portee = models.CharField(max_length=300)
    
    annee_scolaires = models.ArrayReferenceField(
        to=AnneeScolaire,
        on_delete=models.CASCADE,
    )
    # class Meta:
    #   ordering = ['date']

    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class SanteEleve(models.Model):
    libelle = models.CharField(max_length=300)
    Description = models.TextField()
    apte = models.BooleanField(default=True)
    # Etat sante peut etre excellent, Très bon, bon, moyen, problématique, 
    etat_sante = models.CharField(max_length=100)
    
    eleves = models.ArrayReferenceField(
        to=Eleve,
        on_delete=models.CASCADE,
    )
    annee_scolaires = models.ArrayReferenceField(
        to=AnneeScolaire,
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class Club(models.Model):
    libelle = models.CharField(max_length=300)
    Description = models.TextField()
    
    eleves = models.ArrayReferenceField(
        to=Eleve,
        on_delete=models.CASCADE,
    )
    annee_scolaires = models.ArrayReferenceField(
        to=AnneeScolaire,
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class Livre(models.Model):
    libelle = models.CharField(max_length=300)
    Description = models.TextField()
    date_entree = models.DateField()
    
    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class Bibliotheque(models.Model):
    libelle = models.CharField(max_length=200)
    livres = models.ArrayReferenceField(
        to=Livre,
        on_delete=models.CASCADE,
    )
    annee_scolaires = models.ArrayReferenceField(
        to=AnneeScolaire,
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class AssembleeGenerale(models.Model):
    libelle = models.CharField(max_length=300)
    date = models.DateField()
    rapport = models.TextField()

    enseignants = models.ArrayReferenceField(
        to=Enseignant,
        on_delete=models.CASCADE,
    )
    admin_staffs = models.ArrayReferenceField(
        to=AdminStaff,
        on_delete=models.CASCADE,
    )
    annee_scolaires = models.ArrayReferenceField(
        to=AnneeScolaire,
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return self.libelle

    objects = models.DjongoManager()

class File(models.Model):
  file = models.FileField(blank=False, null=False)
  description = models.CharField(max_length=300,blank=True)
  file_type = models.CharField(max_length=200, blank=True)
  timestamp = models.DateTimeField(auto_now_add=True)