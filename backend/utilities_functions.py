import string
import random
from .models import *
from .serializers import MatiereSerializer
# from rest_framework.response import Response


def _list_etabs():
    etabs = Etab.objects.all()
    return etabs
def _list_sousetabs(id_annee):
    annee = AnneeScolaire.objects.get(id=id_annee)
    sous_etabs = annee.sous_etabs.all()
    return sous_etabs
def _list_cycles(id_sousetab):
    if isinstance(id_sousetab, int)==True:
        cycles = Cycle.objects.filter(sous_etabs__id=id_sousetab)
    else:
        cycles = []
    return cycles
def _list_annee_scolaire():
    return AnneeScolaire.objects.all()
def _list_niveaux(cycles):
    res = []
    for c in cycles:
        niveaux = c.niveau_set.all()
        for n in niveaux:
            res.append({"id":n.id,"libelle":n.libelle,"code":n.code,"id_cycle":c.id,"libelle_cycle":c.libelle})
    return res
def _list_classes(cycles):
    res = []
    for c in cycles:
        niveaux = c.niveau_set.all()
        for n in niveaux:
            classes = n.classe_set.all()
            for cl in classes:
                res.append({"id":cl.id,"libelle":cl.libelle,"code":cl.code,
                "id_cycle":c.id,"libelle_cycle":c.libelle,"id_niveau":n.id,"libelle_niveau":n.libelle})
    return res
def _list_matieres(id_sousetab):
    matieres = Matiere.objects.filter(sous_etabs__id=id_sousetab)
    return matieres
def _list_matieres_classe(matieres,classes):
    res = []
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
    return res
def _list_cours(id_sousetab):
    crs = []

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
            # print("len(cr): ",len(cr),cl.libelle,c.libelle)


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

    return crs
def _list_matricules(sousetabs):
    res = []
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
    return res
def _list_hierarchies(id_sousetab):
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

    return res
def _list_classes_examens(id_sousetab):
    classes = Classe.objects.filter(sous_etabs__id=id_sousetab)
    res = []
    for c in classes:
        res.append({"id":c.id,"libelle":c.libelle,"is_classe_examen":c.is_classes_examen})
    return res
def _list_quota_cursus(id_sousetab):
    hierarchies = HierarchieEtab.objects.filter(sous_etabs__id=id_sousetab).order_by('rang')
    res = []

    for h in hierarchies:
        res.append({"id":h.id,"rang":h.rang,"libelle":h.libelle,"quota_cursus":h.quota_cursus})
    config = ConfigAnnee.objects.get(sous_etabs=id_sousetab)
    res.append({"id":0,"rang":"_","libelle":config.appellation_formateur,"quota_cursus":config.pourcentage_cursus_enseignant})

    return res
def _list_type_payement_eleve(id_sousetab,id_cycle,id_niveau,id_classes):

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
        print("tpe: ",tpe)
        for t in tpe:
            print("tranche: ",t)
            if cpt < len(tpe):
                info_tranches += str(t.id)+","+t.libelle+","+str(t.montant)+","+str(t.ordre_paiement)+","+str(t.date_deb)+","+str(t.date_fin)+"²²"
            else:
                info_tranches += str(t.id)+","+t.libelle+","+str(t.montant)+","+str(t.ordre_paiement)+","+str(t.date_deb)+","+str(t.date_fin)
            total += t.montant
            cpt += 1
        res.append({"id":cl.id,"classe":cl.libelle,"info_tranches":info_tranches,"total":total})

    return res
def _list_type_payement_divers(id_sousetab):
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

    return res
def _list_type_enseignants(id_sousetab):


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

    return res
def _list_type_payement_enseignants(id_sousetab,id_type_enseignant):

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

        type_enseignants = tpd.type_enseignant.filter()

        if len(type_enseignants)>0:
            id_type_enseignant = type_enseignants[0].id
            libelle_type_enseignants = type_enseignants[0].libelle

        # for se in setabs:
        res.append({"id":tpd.id,"libelle_payement":tpd.libelle,"id_type_enseignant":id_type_enseignant,"libelle_ens":libelle_type_enseignants,
            "montant":tpd.montant,"entree_sortie_caisee":tpd.entree_sortie_caisee})

    return res
def _list_type_payement_adminstaffs(id_sousetab,id_hierarchie):

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
        print(hierarchies)
        if len(hierarchies)>0:
            libelle_hierarchie =hierarchies[0].libelle
            id_h =hierarchies[0].id
        for se in setabs:
            res.append({"id":tpd.id,"libelle_payement":tpd.libelle,"libelle_h":libelle_hierarchie,
                "id_h":id_h,"montant":tpd.montant,"entree_sortie_caisee":tpd.entree_sortie_caisee})

    return res
def _list_trimestres(id_sousetab):

    res = []
    trimestres = []
    if isinstance(id_sousetab,int):
        trimestres = Trimestre.objects.filter(sous_etabs__id=id_sousetab).order_by('date_deb')
    else:
        trimestres = Trimestre.objects.all().order_by('date_deb')

    for trimestre in trimestres:
        liste_sous_etabs_libelle = ""
        sousetabs = trimestre.sous_etabs.all()
        res.append({"id":trimestre.id,"libelle":trimestre.libelle,
            "date_deb":trimestre.date_deb,"date_fin":trimestre.date_fin,"is_active":trimestre.is_active,
            "numero":trimestre.numero})

    return res
def _list_sequences(id_sousetab,id_trimestre):
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
        libelle_trimestre = seq.trimestres.all()[0].libelle
        id_trimestre = seq.trimestres.all()[0].id
        res.append({"id":seq.id,"libelle":seq.libelle,"id_trimestre":id_trimestre,"libelle_trimestre":libelle_trimestre,
            "date_deb":seq.date_deb,"date_fin":seq.date_fin,"is_active":seq.is_active,
            "numero":seq.numero})
    return res
def _list_specialites(id_sousetab):

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



    return res
def _list_jours(id_sousetab):
    res = []
    if isinstance(id_sousetab, int)==False:
        jours = Jour.objects.filter().order_by('numero_jour')
    else:
        jours = Jour.objects.filter(sous_etabs__id=id_sousetab).order_by('numero_jour')

    for jour in jours:
        res.append({"id":jour.id,"libelle":jour.libelle,"numero":jour.numero_jour,"h_deb":jour.heure_deb_cours,
            "h_fin":jour.heure_fin_cours})
    return res
def _list_pauses(id_sousetab):
    res = []
    id_sousetab = int(id_sousetab) if (id_sousetab != "" and id_sousetab != None) else ""

    pauses = Pause.objects.filter(sous_etabs__id=id_sousetab)

    for pause in pauses:
        res.append({"id":pause.id,"libelle":pause.libelle,"duree":pause.duree})
    return res
def _list_tranche_horaires(id_sousetab):

    res = []
    jours = Jour.objects.filter(sous_etabs__id=id_sousetab).order_by('numero_jour')
    for jour in jours:
        tranches = TrancheHoraire.objects.filter(jours=jour).order_by('heure_deb')
        cpt = 0
        libelle_tranches = ""
        id_tranches = ""
        type_tranches = ""
        heure_deb_tranches = ""
        heure_fin_tranches = ""
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

    return res,duree_periode
def _list_user_roles(id_sousetab):

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


    return res,list_hierarchies
def _list_enseignant_matieres_specialites(id_sousetab):

    matieres = Matiere.objects.filter(sous_etabs__id=id_sousetab).order_by('libelle')
    enseignants = Enseignant.objects.filter(is_active__in=[True])
    sousetab = SousEtab.objects.get(id=id_sousetab)
    users = sousetab.users.all()
    matieres = MatiereSerializer(matieres,many=True).data

    # enseignant = Enseignant.objects.filter(users=user)
    liste_matieres_enseignees = ""
    id_matieres_enseignees = ""
    res = []

    for user in users:
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

    return res,matieres
def _list_users_desactives(id_sousetab):

    users = SousEtab.objects.get(id=id_sousetab).users.filter(is_active__in=[False]).order_by('first_name')
    res = []

    for u in users:
        profil = Profil.objects.get(user=u)
        res.append({"id":u.id,"nom":u.first_name,"prenom":u.last_name,"login":u.username,"sexe":profil.sexe,
            "email":u.email,"is_active":False})

    return res
def _list_payement_eleve(id_classe):
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

    return res,type_pyts,montant_total_a_payer

def formater_heure(heure):
    heure = heure.split("h")
    minute = ""
    h = ""
    h= heure[0]
    if len(heure) ==2:
        minute = heure[1]
    if minute!= "" and int(minute) == 0:
        minute = ""
    if int(h) ==0:
        h = "0"
    h = h[1] if len(h)==2 and h[0]=="0" else h
    minute = minute[1] if len(minute)==2 and minute[0]=="0" else minute
    return h+"h"+minute
def generate_random_string():
    # initializing size of string
    N = 10
    # using random.choices()
    # generating random strings
    res = ''.join(random.choices(string.ascii_letters, k=N))
    # print result
    print("The generated random string : " + str(res))
    return str(res)