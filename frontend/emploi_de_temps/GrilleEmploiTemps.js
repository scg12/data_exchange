import React from 'react';
import classes from './EmploiT.module.css';
import LigneMatieres from './LigneMatieres';
import LigneProfs from './LigneProfs'
import LigneValeur from './LigneValeur';
import CustomButton from '../customButton/CustomButton';
import Palette from './palette/Palette';
import DroppableDiv from '../droppableDiv/DroppableDiv';
import Jour from './Jour';
import MatiereDiv from './matiereDiv/MatiereDiv';

import { useContext, useState, useEffect} from "react";
import UiContext from '../../../store/UiContext';
import AppContext from "../../../store/AppContext";

import { useTranslation } from "react-i18next";
import '../../../translation/i18n';
import {DndProvider} from 'react-dnd';
import {HTML5Backend} from 'react-dnd-html5-backend';
import axiosInstance from '../../../axios';
import {useNavigate} from 'react-router-dom';
// import {clearGrille, initProfList, clearMatiereList, initMatiereList, Evaluate, getJourIndex, CURRENT_DROPPED_MATIERE_LIST, CURRENT_DROPPED_PROFS_LIST} from './ET_Module';
// *desactiver
// import {TAB_JOURS, LONGUEUR_PERIODE, TAB_PERIODES} from './ET_Module';
// import { createPauses } from "../../../store/SharedData/DndFuncts";
import classesP from '../emploi_de_temps/palette/Palette.module.css';




var currentClasseId =undefined;
function GrilleEmploiTemps(props) {
  
    const currentUiContext = useContext(UiContext);
    const currentAppContext = useContext(AppContext);
    const navigate = useNavigate();

    // *activer
    // let TAB_JOURS = [], LONGUEUR_PERIODE =[], TAB_PERIODES=[];
    // *activer
    let indexClasse = -1;
    let nb_refresh = 0;
    let decallage_pause =0;
    let OLD_DROPPED_MATIERE = [];
    // *activer
    // let ET_data = []

     //Cette constante sera lu lors de la configuration de l'utilisateur.
    const selectedTheme = currentUiContext.theme;
    const [isValid, setIsValid] = useState(false);
    // *activer
    const [optClasse, setOptClasse] = useState();
    const [pausecreated, setPauseCreated] = useState(false);
    const { t, i18n } = useTranslation();
    
    
    const changeLanguage = (event) => {
        i18n.changeLanguage(event.target.id);
    };
    let SELECTED_MATIERE_ID;
    let COUNT_SELECTED_MATIERES;

    let SELECTED_MATIERE_TAB;
    let CURRENT_MATIERE_LIST;
    let CURRENT_DROPPED_MATIERE_LIST;
    let COUNT_SELECTED_PROFS;
    let SELECTED_PROF_ID;
    
    let SELECTED_PROF_TAB;
    let CURRENT_PROFS_LIST;
    let CURRENT_DROPPED_PROFS_LIST;

    var PROF_DATA ={
        idProf:'',
        NomProf:'',
        idJour:'',
        heureDeb:'',
        heureFin:'',
        idMatiere:'',
        isSelected:false
    }
    function updateSelectedProfId(valeur){
        SELECTED_PROF_ID = valeur;
    }
    
    function updateCountSelectedProfs(valeur){
        COUNT_SELECTED_PROFS = valeur;
    }
    
    //---SELECTED_PROF_TAB
    function AddValueToSelectedProfTab(position, valeur){
        if(position!=-1) SELECTED_PROF_TAB.splice(position,0,valeur);
        else SELECTED_PROF_TAB.push(valeur);
    }
    
    function removeValueToSelectedProfTab(position){
        SELECTED_PROF_TAB.splice(position,1);    
    }
    
    
    //---CURRENT_PROF_LIST
    function AddValueToCurrentProfList(position, valeur){
        if(position!=-1) CURRENT_PROFS_LIST.splice(position,0,valeur);
        else CURRENT_PROFS_LIST.push(valeur);
    }
    
    function removeValueToCurrentProfList(position){
        CURRENT_PROFS_LIST.splice(position,1);    
    }
    
    
    //---CURRENT_DROPPED_PROFS_LIST
    function AddValueToDroppedProfList(position, valeur){
        if(position!=-1) CURRENT_DROPPED_PROFS_LIST.splice(position,0,valeur);
        else CURRENT_DROPPED_PROFS_LIST.push(valeur);
    }
    
    function removeValueToDroppedProfList(position){
        CURRENT_MATIERE_LIST.splice(position,1);    
    }

    function updateSelectedMatiereId(valeur){
        SELECTED_MATIERE_ID = valeur;
    }
    
    function updateCountSelectedMatieres(valeur){
        COUNT_SELECTED_MATIERES = valeur;
    }
    
    //---SELECTED_MATIERE_TAB
    function AddValueToSelectedMatiereTab(position, valeur){
        if(valeur='') SELECTED_MATIERE_TAB=[];
        else{
            if(position!=-1) SELECTED_MATIERE_TAB.splice(position,0,valeur);
            else SELECTED_MATIERE_TAB.push(valeur);
        }   
    }
    
    function removeValueToSelectedMatiereTab(position){
        SELECTED_MATIERE_TAB.splice(position,1);    
    }
    
    //---CURRENT_MATIERE_LIST
    function AddValueToCurrentMatiereList(position, valeur){
        if(position!=-1) CURRENT_MATIERE_LIST.splice(position,0,valeur);
        else CURRENT_MATIERE_LIST.push(valeur);
    }
    
    function removeValueToCurrentMatiereList(position){
        CURRENT_MATIERE_LIST.splice(position,1);    
    }
    
    //---CURRENT_DROPPED_MATIERE_LIST
    function AddValueToValueDroppedMatiereList(position, valeur){
        if(position!=-1) CURRENT_DROPPED_MATIERE_LIST.splice(position,0,valeur);
        else CURRENT_DROPPED_MATIERE_LIST.push(valeur);
    }
    
    function removeValueToDroppedMatiereList(position){
        CURRENT_DROPPED_MATIERE_LIST.splice(position,1);    
    }
    // *desactiver
    // const listMatieres = [
    //     "Francais*001_Anglais*002_Histoire*003_ECM*004_SVT*005_PCT*006_Maths*007_Sport*008_TM*009_ESF*003_hdhhd*0011_vdvdvd*0012_vdvddd*0013_dcdcdc*0014_dgdggd*0015_dvvdvd*0016_dvvdd*0017",
    //     "Allemand*0018_Francais*001_Anglais*002_Histoire*003_ECM*004_SVT*005_PCT*006_Maths*007_Sport*008_TM*009_ESF*003",
    //     "Espagnol*001_Francais*002_Anglais*003_Histoire*003_ECM*002_SVT*002_PCT*001_Maths*001_Sport*002_TM*001_ESF*003_Espagnol*002_Francais*001_Anglais*002_Histoire*003_ECM*001_SVT*003_PCT*001_Maths*005_Sport*001_TM*004_ESF*003_Espagnol*004_Francais*008_Anglais*003",
    //     "Espagnol*0019_Philo*0020_Francais*001_Anglais*002_Histoire*003_ECM*004_SVT*005_PCT*006_Maths*007_Sport*008_TM*009_ESF*0010"
    // ]
   
    // *desactiver
    // const optClasse=[
    //     {value: '0',     label:'Choisir une classe'},
    //     {value: '6em1',  label:'6ieme 1'           },
    //     {value: '5em2',  label:'5ieme 2'           },
    //     {value: '4A2',   label:'4ieme A2'          },
    //     {value: '3E',    label:'3ieme Esp'         },
    //     {value: '2c1',   label:'2nd C1'            },
    //     {value: '1L',    label:'1ere L'            },
    //     {value: 'TD',    label:'Tle D'             }
    // ]

    const selectNiveauStyles = {
        control: base => ({
            ...base,
            height: '3.3vh',
            minHeight: '3.3vh',
            width:'17vw',
            minwidth:'17vw',
            paddingBottom : 30,
            fontSize:'1vw',         
          }),  
          placeholder:base => ({
              ...base,
              marginTop:'-3.3vh',
              fontSize: '1vw'
          }),  
          indicatorsContainer:(base,state) => ({
              ...base,
              height: state.isSelected ?'5vh': '5vh',
              marginTop: state.isSelected ? '-1.3vh' :'-1.3vh',
              alignSelf: state.isSelected ? 'center' : 'center',
          }),  
          indicatorSeparator:(base,state) => ({
              ...base,
              height: state.isSelected ? '5vh': '5vh',
              marginTop: state.isSelected ? '-1.4vh' : '-1.4vh'
          }),          
          dropdownIndicator:(base,state) => ({
              ...base,
              marginTop: state.isSelected ? '-2.7vh' : '-2.7vh',
              fontSize: state.isSelected ? '1vw' : '1vw'
          }),          
          singleValue: (base,state) => ({
            ...base,
            marginTop: state.isSelected ? '-3.7vh' : '-3.7vh',
            fontSize:  state.isSelected ? '0.9vw' : '0.9vw',
            fontWeight: state.isSelected ? '670' : '670'
        })
    };

    function createOption2(libellesOption){
        var newTab=[];
        for(var i=0; i< libellesOption.length; i++){
            var obj={
                value: libellesOption[i].id,
                label: libellesOption[i].libelle
            }
            newTab.push(obj);
        }
        return newTab;
    }
    

    useEffect(()=> {
        if(currentUiContext.TAB_CRENEAU_PAUSE.length>0)
        {
        console.log("00000 ",currentUiContext)
        setOptClasse(createOption2(currentUiContext.classeEmploiTemps));
        console.log("init TAB_VALEUR_HORAIRE",currentUiContext.TAB_VALEUR_HORAIRE)

    //     // Affichage initial des matières pr la première classe selectionnée
         if(currentUiContext.classeEmploiTemps.length>0){
            // currentUiContext.setNbRefreshEmpoiTemps();
            currentUiContext.addMatiereToDroppedMatiereList([],-2);
            console.log("nb_refresh: ",currentUiContext.nbRefreshEmpoiTemps);
            console.log("=currentUiContext.CURRENT_DROPPED_MATIERE_LIST: ",currentUiContext.CURRENT_DROPPED_MATIERE_LIST)
            currentClasseId = currentUiContext.classeEmploiTemps[0].id;
            console.log("currentClasseId: ",currentClasseId,currentUiContext.classeEmploiTemps)
            indexClasse = currentUiContext.classeEmploiTemps.findIndex(c=>c.id==currentClasseId);
            console.log("INDEX: ",indexClasse);

            clearGrille(currentUiContext.TAB_PERIODES, currentUiContext.TAB_JOURS.length);
            initProfList(currentUiContext.listProfs);
            // currentUiContext.addProfToDroppedProfList(CURRENT_DROPPED_PROFS_LIST,-1);
            clearMatiereList(currentUiContext.matiereSousEtab); 
            var tabMatieres=[]
            // var listMat = getMatieres();
            // var listMat = listMatieres[indexClasse];
            var listMat = currentUiContext.listMatieres[indexClasse];

            tabMatieres = listMat.split('_');
            initMatiereList(tabMatieres);

            var ET_data = getSaveEmploiTempsData(currentClasseId);
            // if(ET_data.length > 0)  
            initGrille(ET_data,currentUiContext.matiereSousEtab,currentUiContext.listProfs,currentClasseId,currentUiContext.emploiDeTemps,"");
            currentUiContext.setCurrentIdClasseEmploiTemps(currentClasseId);
            currentUiContext.setIndexClasse(indexClasse);
            let liste_dropped_matiere = currentUiContext.CURRENT_DROPPED_MATIERE_LIST.filter(ce=>ce.idClasse==currentClasseId).concat(OLD_DROPPED_MATIERE)
            console.log("+++ liste_dropped_matiere: ",liste_dropped_matiere);
            CURRENT_DROPPED_MATIERE_LIST = liste_dropped_matiere;
            currentUiContext.addMatiereToDroppedMatiereList(liste_dropped_matiere,-2);
            
            console.log("currentUiContext.CURRENT_DROPPED_MATIERE_LIST: ",currentUiContext.CURRENT_DROPPED_MATIERE_LIST)
        }
        }  

    },[currentUiContext.TAB_CRENEAU_PAUSE]);

    // useEffect(()=> {
    //     console.log("-------- currentUiContext.TAB_JOURS: ",currentUiContext.TAB_JOURS.length);
    //     if(currentUiContext.TAB_JOURS.length>0){
    //         // createPauses();

    //         clearGrille(currentUiContext.TAB_PERIODES.length);
    //         // initProfList();
    //         // currentUiContext.addProfToDroppedProfList(CURRENT_DROPPED_PROFS_LIST,-1);
    //         // clearMatiereList(); 
    //         var tabMatieres=[]
    //         // var listMat = getMatieres();
    //         var listMat = currentUiContext.listMatieres[currentUiContext.indexClasse];

    //         tabMatieres = listMat.split('_');
    //         // initMatiereList(tabMatieres);

    //         // setPauseCreated(true);
    //     }        
    // },[currentUiContext.TAB_JOURS]);

     /*************************** <Managing Theme> ****************************/

    function getCurrentTheme()
    {  // Choix du theme courant
       switch(selectedTheme){
            case 'Theme1': return classes.Theme1_footer;
            case 'Theme2': return classes.Theme2_footer;
            case 'Theme3': return classes.Theme3_footer;
            default: return classes.Theme1_footer;
        }
    }

      
    function getButtonStyle()
    { // Choix du theme courant
      switch(selectedTheme){
        case 'Theme1': return classes.Theme1_Btnstyle ;
        case 'Theme2': return classes.Theme2_Btnstyle ;
        case 'Theme3': return classes.Theme3_Btnstyle ;
        default: return classes.Theme1_Btnstyle ;
      }
    }
    // *activer
    function getMatieres(indexClasse){
      let ligne = "";
    //   indexClasse = currentUiContext.classeEmploiTemps.findIndex(c=>c.id==currentClasseId);
      ligne = currentUiContext.listMatieres[indexClasse];
      console.log("LIGNE: ",ligne)
      return ligne;
    }
    // *desactiver
    // function getMatieres(classe){
      
    //     switch(classe){
    //         case '6em1': return listMatieres[0] ;
    //         case '5em2': return listMatieres[0] ;
    //         case '4A2':  return listMatieres[1] ;
    //         case '3E':   return listMatieres[2] ;
    //         case '2c1':  return listMatieres[0] ;
    //         case '1L':   return listMatieres[3] ;
    //         case 'TD':   return listMatieres[0] ;
    //     }
      
    // }
    // *activer
    function getEmploiDeTempsString(classeId){
        return '';
    }

    // *desactiver
    // function getEmploiDeTempsString(classeId){
    //     switch(classeId){
    //         case '6em1': return '0:8h_9h*001*Mr. MBARGA P.%prof_1|2:10h10_11h*002*Mr. TEMGHOUA%prof_2' ;
    //         case '5em2': return '0:8h_9h*003*Mme. BOMBA%prof_1|1:13h10_14h*004' ;
    //         case '4A2':  return '0:8h_9h*005*Mr. ELimbi%prof_2*Mme. MENGUE%prof_3|3:14h_15h*002*Mme. SANGA%prof_4' ;
    //         case '3E':   return '' ;
    //         case '2c1':  return '' ;
    //         case '1L':   return '0:8h_9h*001|4:9h_10h*002' ;
    //         case 'TD':   return '' ;
    //     }

    // }

    /*************************** <Managing Handlers> ****************************/
    function saveEmploiDeTemps(classeId){
        //Ici on ecrit le code du save.
    }
    // *activer
    function dropDownHandler(e){       
        var tabMatieres=[];
        currentClasseId = e.target.value;
        currentUiContext.setNbRefreshEmpoiTemps(1);

            clearGrille(currentUiContext.TAB_PERIODES,currentUiContext.TAB_JOURS);

            //Initialisation de la liste des profs 
            initProfList(currentUiContext.listProfs);
            // currentUiContext.addProfToDroppedProfList(CURRENT_DROPPED_PROFS_LIST,-1);

            //Initialisation de la liste des  matieres 
            clearMatiereList(currentUiContext.matiereSousEtab); 
            let indexClasse = currentUiContext.classeEmploiTemps.findIndex(c=>c.id==currentClasseId);
            var listMat = getMatieres(indexClasse);
            console.log("ICI listMat: ",listMat);
            tabMatieres = listMat.split('_');
            initMatiereList(tabMatieres);
            
            //Pre-remplissage de la grille avec les creneau deja configures 
            var ET_data = getSaveEmploiTempsData(currentClasseId);
            console.log("ET_data.length: ",ET_data.length);
            // if(ET_data.length > 0)  
            console.log("currentClasseId: ",currentClasseId);
            console.log("init currentUiContext.emploiDeTemps: ",currentUiContext.emploiDeTemps);
            initGrille(ET_data,currentUiContext.matiereSousEtab,currentUiContext.listProfs,currentClasseId,currentUiContext.emploiDeTemps,"dropDownHandler");
            // currentUiContext.addMatiereToDroppedMatiereList(CURRENT_DROPPED_MATIERE_LIST,-1); 
            currentUiContext.setIndexClasse(indexClasse); 
            currentUiContext.setCurrentIdClasseEmploiTemps(currentClasseId);
            console.log("OLD_MATIERES: ",OLD_DROPPED_MATIERE);
            console.log("**CURRENT_DROPPED_MATIERE_LIST: ",currentUiContext.CURRENT_DROPPED_MATIERE_LIST.filter(ce=>ce.idClasse==currentClasseId));
            let liste_dropped_matiere = currentUiContext.CURRENT_DROPPED_MATIERE_LIST.filter(ce=>ce.idClasse==currentClasseId).concat(OLD_DROPPED_MATIERE)
            console.log("+++ liste_dropped_matiere: ",liste_dropped_matiere);
            CURRENT_DROPPED_MATIERE_LIST = liste_dropped_matiere;
            currentUiContext.addMatiereToDroppedMatiereList(liste_dropped_matiere,-2);
            // currentUiContext.addMatiereToDroppedMatiereList(currentUiContext.CURRENT_DROPPED_MATIERE_LIST.filter(ce=>ce.idClasse==currentClasseId),-2);
            console.log("currentUiContext.CURRENT_DROPPED_MATIERE_LIST: ",currentUiContext.CURRENT_DROPPED_MATIERE_LIST)
            // let droppedMatieres = currentUiContext.CURRENT_DROPPED_MATIERE_LIST;
            // for (let i = 0; i < droppedMatieres.length; i++) {
            //     droppedMatieres[i].isSelected = false;
            // }
            // // on rafraichit la liste
            // currentUiContext.addMatiereToDroppedMatiereList(droppedMatieres,-2);
    }

    
    function cancelHandler(){
        var tabMatieres=[];

        if(currentClasseId!= undefined){
            
            //Initialisation de la Grille d'emploi de temps 
            clearGrille(currentUiContext.TAB_PERIODES,currentUiContext.TAB_JOURS);

            //Initialisation de la liste des profs 
            initProfList();
            currentUiContext.addProfToDroppedProfList(CURRENT_DROPPED_PROFS_LIST,-1);
            
            //Initialisation de la liste des  matieres 
            var listMat = getMatieres(currentClasseId);
            tabMatieres = listMat.split('_');
            initMatiereList(tabMatieres);
            currentUiContext.addMatiereToDroppedMatiereList(CURRENT_DROPPED_MATIERE_LIST,-1);
       
        }
    }

// *desactiver
    function getSaveEmploiTempsData(classeId){
        var ET_data='';
        //Requete axios pour rechercher les donnees d'emploi de temps existantes pour cette classe.
        /*axiosInstance.post(`get-emploiTemps/`, {
            code_classe: classeId,
        }).then((res)=>{
            console.log(res.data);
            ET_data = res.data ///bref on retourne la chaine 
        })*/
        var ET_data = getEmploiDeTempsString(classeId);

        return ET_data;
    }

    function UpdateEmploiDeTemps(){
        axiosInstance
        .post(`set-emploi-de-temps/`,{id_sousetab: currentAppContext.currentEtab,
        emploiDeTemps:currentUiContext.emploiDeTemps }).then((res)=>{
            // res.data.map((cycle)=>{cycles.push(cycle)});
            console.log(res.data);
            // navigate('/login');
            // window.location.href = '/scolarite';
        })  
    }

    function PrintEmploiDeTemps(){
        
    }
    
   /*************************** <Utility Functions> ****************************/
    
    function calculDureePause(creneau){
        var tabHeure, tabHeureDeb,tabHeureFin;
        var dureePause=[];
        tabHeure = creneau.split('_');
        tabHeureDeb = tabHeure[0].split('h');
        tabHeureFin = tabHeure[1].split('h');
        // console.log("calculDureePause: ",tabHeureDeb, tabHeureFin);
        tabHeureDeb[0] =Evaluate(tabHeureDeb[0]);
        tabHeureDeb[1] =Evaluate(tabHeureDeb[1]);
        tabHeureFin[0] =Evaluate(tabHeureFin[0]);
        tabHeureFin[1] =Evaluate(tabHeureFin[1]);
        if( tabHeureDeb[0]==tabHeureFin[0]){
            dureePause.push(0);
            dureePause.push(tabHeureFin[1] - tabHeureDeb[1]);
        }else{
            if(tabHeureDeb[1]==tabHeureFin[1]){
                dureePause.push((tabHeureFin[0] -  tabHeureDeb[0]))
                dureePause.push(0); 
            } else{
                dureePause.push(tabHeureFin[0] -  (tabHeureDeb[0]+1));
                dureePause.push((60-tabHeureDeb[1])+tabHeureFin[1]);
            }           

        }
        
        return ((dureePause[0]*60)+ dureePause[1]);
    }

    function computePauseDivSize(dureePauseEnMinutes){
        let minutes = calculDureePause(currentUiContext.intervalleMaxTranche)
        return Math.floor(dureePauseEnMinutes*65/minutes);
        // return Math.floor(dureePauseEnMinutes*60/(currentUiContext.TAB_PERIODES.length))/60;
    }

    function calculMarge(creneau){
        var heure,marge, tabHeureDeb;
        let minutes = calculDureePause(currentUiContext.intervalleMaxTranche)
        tabHeureDeb = creneau.split('_');
        heure = tabHeureDeb[0].split('h');
        // marge = (Evaluate(heure[1])*60/(currentUiContext.TAB_PERIODES.length))/60;
        marge = (Evaluate(heure[1])*65/minutes);
        return Math.floor(marge);
    }
/*************************** <Profs Functions> ****************************/
    // function getProfs(codeMatiere){
    //     switch(codeMatiere){
    //         case '001': return listProfs[1] ;
    //         case '002': return listProfs[2] ;
    //         case '003': return listProfs[3]
    //         default: return listProfs[0];
    //         //case 'matiere_4':   return listProfs[2] ;           
    //     }
      
    // }
    // function initProfListWithProfs(listeProf){
    //     var parent = document.getElementById('profList');
    //     var draggableSon, draggableSonText, draggableSonImg;
    
    //     clearProflist();
    //     //alert(listeProf);
      
    //     for (var i = 0; i < listeProf.length; i++) {
    //         PROF_DATA = {};
    //         draggableSon =  document.getElementById('prof_' + (i+1));
    //         draggableSonText = document.getElementById('prof_' + (i+1)+'_sub');
            
    //         draggableSon.className = classesP.profDivStyle;  
    //         draggableSon.title = listeProf[i];       
            
    //         draggableSonText.textContent = listeProf[i];
    //         draggableSonText.className = classesP.profTextSyle;            
    
    //         draggableSonImg =  document.getElementById('prof_' + (i+1) + '_img');
    //         draggableSonImg.className = classesP.profImgStyle;
    
    //         draggableSonImg = document.querySelector('#prof_' + (i+1) + '_img > img')
    //         if(listeProf[i].includes('Mr.')) {
    //             draggableSonImg.setAttribute('src',"images/maleTeacher.png");
    //         }else{
    //             draggableSonImg.setAttribute('src',"images/femaleTeacher.png");
    //         }
            
            
    //         PROF_DATA.idProf = 'prof_' + (i+1);
    //         PROF_DATA.NomProf = listeProf[i];
            
    //         CURRENT_PROFS_LIST.push(PROF_DATA);
    //         PROF_DATA = {};                                     
    //     }
     
    // }
    // function getProfsList(codeMatiere, periode){
    //     var tabProfs,profList;
    //     var codeMatiere;
    
    //     profList = getProfs(codeMatiere)
    //     tabProfs = profList.split('_');
    //     initProfListWithProfs(tabProfs);
    // }
/****************************Copié depuis ET_Module**************************** */
function initGrille(ET_data,matiereSousEtab,listProfs,id_classe,emploiDeTemps,functionAppellante) {
    var i, j, jour, periode, codeMatiere, profId,id_tranche;
    // on doit aussi ajouter l'id de la classe en parametre
    // on cherche dans emploiDeTemps l'attribut value et on travaille avec
    // var tabMatiere = ET_data.split('|');
    var controleur;
    if (functionAppellante=="dropDownHandler"){
        controleur = 0;
        // currentUiContext.setNbRefreshEmpoiTemps(0);
    }
    else controleur = currentUiContext.nbRefreshEmpoiTemps;

    if(controleur==0 ){
    var tabMatiere = [];
    console.log("ET_data: ",ET_data," id_classe: ",id_classe);
    i = 0;
    let emploiTemps = emploiDeTemps.filter(em=>!em.modify.includes("s")&&em.id_classe==id_classe)
    console.log("emploiTemps: ",emploiTemps);
    // console.log("initGrille :",matiereSousEtab);
    let cpte_emploiTemps = emploiTemps.length;
    while(i < cpte_emploiTemps) {
        console.log("emploiTemps:[i] ",i,emploiTemps[i]);
        // jour = tabMatiere[i].split(':')[0];
        jour = emploiTemps[i].id_jour;
        // periode = tabMatiere[i].split(':')[1].split('*')[0];
        periode = emploiTemps[i].libelle;
        id_tranche = emploiTemps[i].id_tranche;
        // codeMatiere = tabMatiere[i].split(':')[1].split('*')[1];
        codeMatiere = emploiTemps[i].id_matiere;
        
        var idMatiereToDrop = 'DM_'+jour +'_' +  periode;
        var matiereIndex = CURRENT_MATIERE_LIST.findIndex((matiere)=> matiere.codeMatiere == codeMatiere);
        
        if(matiereIndex >= 0){
            var droppedMatiere = {...CURRENT_MATIERE_LIST[matiereIndex]};
            
            droppedMatiere.idMatiere = idMatiereToDrop;
            droppedMatiere.idJour = jour;
            droppedMatiere.isSelected = false;
            droppedMatiere.isOld = true;
            droppedMatiere.idClasse = id_classe;
            droppedMatiere.heureDeb = periode.split('_')[0];
            droppedMatiere.heureFin = periode.split('_')[1];
            droppedMatiere.tabProfsID =[];
            //droppedMatiere.tabProfsID.push(tabMatiere[i].split(':')[1].split('*')[2]);

           
            
            //POSITIONNEMENT DE L'ELEMENT SUR LA GRILLE
            var parentDiv = document.createElement('div');
            parentDiv.id = droppedMatiere.idMatiere;
            parentDiv.className = classes.droppedMatiereStyle;
           

            var enfanDiv = document.createElement('div');
            enfanDiv.id = droppedMatiere.idMatiere + '_sub';
            enfanDiv.className = classes.matiereTitleStyle;
            enfanDiv.textContent = droppedMatiere.libelleMatiere;

            parentDiv.appendChild(enfanDiv);
            // console.log("enfanDiv: ",enfanDiv);
            // console.log("parentDiv: ",parentDiv);

            var idDropZone = jour +'_'+ periode;
            console.log('zone de drop :', idDropZone)
            var containerDiv = document.getElementById(idDropZone);
            containerDiv.appendChild(parentDiv);
            parentDiv.addEventListener('click', (e) => {matiereClickHandler(e)})
            
            //S'IL YA UN OU DES PROFS, ON LES GERE
            if(emploiTemps[i].value!="" && emploiTemps[i].value.split('*').length>2&& emploiTemps[i].value.split('*')[2].length>2)
            {
            //    var countProf =  tabMatiere[i].split(':')[1].split('*').length-2;
               var countProf =  emploiTemps[i].id_enseignants.length;
                j = 0;
                while(j<countProf){
                    console.log("emploiTemps[i].id_enseignants[j]: ",emploiTemps[i].id_enseignants[j])
                    // var droppedProfId = 'DP_'+ tabMatiere[i].split(':')[1].split('*')[j+2].split('%')[1] + '_' + jour +'_' +  periode;
                    var droppedProfId = 'DP_prof_'+ emploiTemps[i].id_enseignants[j]+"_"+emploiTemps[i].id_jour+"_"+emploiTemps[i].libelle
                    
                    var droppedprofImgDiv = document.createElement('div');
                    droppedprofImgDiv.id = droppedProfId +'_img';
                    droppedprofImgDiv.className = classes.profImgStyle;


                    var droppedprofImg = document.createElement('img');
                    droppedprofImg.className = classes.imgStyle +' '+ classes.profImgStyle;
                    droppedprofImg.id = droppedProfId +'_img';
                    // droppedprofImg.setAttribute('src',(tabMatiere[i].split(':')[1].split('*')[j+2].split('%')[0].includes('Mr.'))? "images/maleTeacher.png":"images/femaleTeacher.png");
                    droppedprofImg.setAttribute('src', "images/maleTeacher.png");
                    droppedprofImg.addEventListener('click', (e) => {droppedProfClickHandler(e)})

                    
                    var droppedprofText = document.createElement('div');
                    droppedprofText.id = droppedProfId +'_sub';
                    droppedprofText.className = classes.profTextSyle;
                    // droppedprofText.textContent = tabMatiere[i].split(':')[1].split('*')[j+2].split('%')[0];
                    droppedprofText.textContent = emploiTemps[i].value.split("*")[2+j].split("%")[0].split("Mr."[1]);
                    droppedprofText.addEventListener('click', (e) => {droppedProfClickHandler(e)})


                   
                    droppedprofImgDiv.appendChild(droppedprofImg)
                    droppedprofImgDiv.appendChild(droppedprofText)
                    //droppedprofImgDiv.addEventListener('click', (e) => {droppedProfClickHandler(e)})


                    var droppedprofDiv = document.createElement('div');
                    droppedprofDiv.id = droppedProfId;
                    droppedprofDiv.className = classes.profDivStyle;
                    droppedprofDiv.appendChild(droppedprofImgDiv);
                    //droppedprofDiv.addEventListener('click', () => {droppedProfClickHandler(droppedProfId)})
                    
                    var container = document.getElementById('P_'+ jour + '_' +  periode);
                    container.appendChild(droppedprofDiv)
                    //container.addEventListener('click', () => {droppedProfClickHandler(droppedProfId)})

                    droppedMatiere.tabProfsID.push(droppedProfId);
                    
                    PROF_DATA = {};
                    PROF_DATA.idProf     = droppedProfId;
                    // PROF_DATA.NomProf    = tabMatiere[i].split(':')[1].split('*')[j+2].split('%')[0];
                    PROF_DATA.NomProf    = emploiTemps[i].value.split("*")[2].split("%")[0].split("Mr."[1]);
                    PROF_DATA.idJour     = jour;
                    PROF_DATA.idMatiere  = idMatiereToDrop;
                    PROF_DATA.heureDeb   = periode.split('_')[0];
                    PROF_DATA.heureFin   = periode.split('_')[1];
                    PROF_DATA.isSelected = false
                    
                    CURRENT_DROPPED_PROFS_LIST.push(PROF_DATA);
                    j++;

                    console.log(PROF_DATA, CURRENT_DROPPED_PROFS_LIST)
                }
            }
            
            OLD_DROPPED_MATIERE.push(droppedMatiere);
             //MISE A JOUR DES DONNEES GLOBALES
            //  AddValueToValueDroppedMatiereList(-1,droppedMatiere);
           
           
        }  
        i++;         
    }
    // console.log("OLD_DROPPED_MATIERE: ",OLD_DROPPED_MATIERE);
    }
    currentUiContext.setNbRefreshEmpoiTemps(0);

}
function matiereClickHandler(e){
    var indexMatiere, codeMatiere, matiereId;
    console.log('event',e);
    // console.log('matiereClickHandler listProfs',listProfs);
    matiereId = e.target.id;
    matiereId = e.target.id;
    if (matiereId.includes('_sub'))  matiereId = matiereId.substring(0,matiereId.length-4)
    if(e.ctrlKey || e.metaKey){
        if(!isCellSelected(matiereId)) {
            //clearCellSelection();
            selectCell(matiereId);                
        } else {
            //clearCellSelection();
            disSelectCell(matiereId);             
        }
    } else {
        if(!isCellSelected(matiereId)) {
            clearCellSelection();
            selectCell(matiereId);                
        } else {
            clearCellSelection();
            disSelectCell(matiereId);                
        }

    }
    
    var countSelected = getCountSelectedDroppedMatieres()

    if(countSelected==1){
        var periode ; //ici il faudra initialiser la periode de la matiere selectionnee.
        let liste_prof = [],tab_prof_id;
        indexMatiere = CURRENT_DROPPED_MATIERE_LIST.findIndex((matiere)=>(matiere.isSelected == true));
        codeMatiere = CURRENT_DROPPED_MATIERE_LIST[indexMatiere].codeMatiere;
        // getProfsList(codeMatiere, periode);
        periode = CURRENT_DROPPED_MATIERE_LIST[indexMatiere].idMatiere;
        tab_prof_id = CURRENT_DROPPED_MATIERE_LIST[indexMatiere].tabProfsID;
        console.log("tab_prof_id: ",tab_prof_id);
        tab_prof_id.forEach(prof => {console.log("$$ prof: ",prof,prof.split("DP_prof_")[1].split("_")[0]);
            liste_prof.push(parseInt(prof.split("DP_prof_")[1].split("_")[0]))
        });
        console.log("liste_prof: ",liste_prof)
        // console.log("1indexMatiere: ",CURRENT_DROPPED_MATIERE_LIST[indexMatiere]);             
        getProfsList2(codeMatiere,periode,liste_prof);                      

    } else {
        if(countSelected >1){
            
            if(selectedDroppedMatiereHaveSameCode()){
                let liste_prof = [],tab_prof_id;
                var listePeriode; //ici il faudra initialiser avec la liste des periodes des matieres selectionnees
                indexMatiere = CURRENT_DROPPED_MATIERE_LIST.findIndex((matiere)=>(matiere.isSelected == true));
                codeMatiere = CURRENT_DROPPED_MATIERE_LIST[indexMatiere].codeMatiere;
                // getProfsList(codeMatiere, listePeriode);     
                periode = CURRENT_DROPPED_MATIERE_LIST[indexMatiere].idMatiere;
                tab_prof_id = CURRENT_DROPPED_MATIERE_LIST[indexMatiere].tabProfsID;
                tab_prof_id.forEach(prof => {
                    liste_prof.push(parseInt(prof.split("DP_Prof_")[1].split("_")[0]))
                });
                console.log("liste_prof: ",liste_prof)
                // console.log("2indexMatiere: ",CURRENT_DROPPED_MATIERE_LIST[indexMatiere]);             
                getProfsList2(codeMatiere,periode,liste_prof);                    
                    }
        }
    }
}
function initProfList(listProfs){
    clearProflist();
    COUNT_SELECTED_PROFS=0;
    SELECTED_PROF_ID='';
    SELECTED_PROF_TAB=[];
    CURRENT_DROPPED_PROFS_LIST=[];
   
}
function clearProflist(){
    let listProfs = currentUiContext.listProfs;
    var draggableSon, draggableSonText, draggableSonImg;
    var PROFLIST_MAXSIZE =listProfs.length;
    for (var i = 0; i < PROFLIST_MAXSIZE; i++) {
        draggableSon =  document.getElementById('prof_' + listProfs[i].id);
        draggableSonText = document.getElementById('prof_' + listProfs[i].id+'_sub');
       
        draggableSon.className = null;
        draggableSon.title = '';
        draggableSonText.textContent ='';
        draggableSonText.className = null;

        draggableSonImg =  document.getElementById('prof_' + listProfs[i].id + '_img');
        draggableSonImg.className = null;

        draggableSonImg = document.querySelector('#prof_' + listProfs[i].id + '_img > img');
        if (draggableSonImg.hasAttribute('src')) draggableSonImg.removeAttribute('src');
        //draggableSonImg.setAttribute('src',null);  
          
    } 
    CURRENT_PROFS_LIST = [];
}
function clearGrille(TAB_PERIODES,TAB_JOURS) {
    var DropZoneId;
    var childDivs;
    var parentDivs;
    var NB_PERIODE = TAB_PERIODES.length;
    var DAYS_COUNT = TAB_JOURS.length;
   
    for (var dayId = 0; dayId < DAYS_COUNT; dayId++) {
        for (var periode = 0; periode < NB_PERIODE; periode++)
         {
            //La DropZone de la Matiere
            DropZoneId = TAB_JOURS[dayId].id+"_"+TAB_PERIODES[periode].duree;
            childDivs = document.getElementById(DropZoneId);
            console.log("DropZoneId: ",DropZoneId)
            if (childDivs!=null){
                childDivs = childDivs.childNodes;
                for(var i = 0; i < childDivs.length; i++){
                    console.log("son: ",childDivs[i])
                    childDivs[i].remove();
                }
            }                
            //La DroZone du Prof
            DropZoneId = 'P_'+TAB_JOURS[dayId].id+'_'+TAB_PERIODES[periode].duree;
            parentDivs = document.getElementById(DropZoneId);
            console.log("DropZoneId2: ",DropZoneId)
            if (parentDivs!=null)
                while(parentDivs.firstChild) parentDivs.removeChild(parentDivs.firstChild);

            // if (parentDivs!=null){
            //     if (parentDivs.style.borderColor=='red'){
            //         parentDivs.style.borderStyle = null;
            //         parentDivs.style.borderWidth = null;
            //         parentDivs.style.borderColor = null;
            //         parentDivs.className = classes.ProfDroppableDivstyle;
            //     }
            //     childDivs = parentDivs.childNodes;
            //     console.log("childDivs ",childDivs)
            //     console.log("childDivs.childNodes: ",childDivs.length)
            //     for(var i = 0; i < childDivs.length; i++){
            //         console.log("son: ",childDivs[i])
            //         childDivs[i].remove();
            //     }
            // }                
            
        }
    }

}
function clearMatiereList(matieres){
    var parent, enfants, draggableSon;
    //On initialise tout ce aui concerne la matiere.
    COUNT_SELECTED_MATIERES=0;
    SELECTED_MATIERE_ID='';
    SELECTED_MATIERE_TAB=[]
    CURRENT_DROPPED_MATIERE_LIST=[];
    CURRENT_MATIERE_LIST=[];
    let MATIERE_MAXSIZE = matieres.length;
    
    parent = document.getElementById('matieres');
    enfants = parent.childNodes;
    
    for (var i = 0; i < MATIERE_MAXSIZE; i++) {
        parent =  document.getElementById('matiere_' + matieres[i].id);
        draggableSon = document.getElementById('matiere_' + matieres[i].id+'_sub');
        parent.className = null;
        parent.title = '';
        draggableSon.textContent ='';
        draggableSon.className = null; 
    }  
    currentUiContext.setCURRENT_MATIERE_LIST([])  
}
function initMatiereList(listeMatieres){
    console.log("listeMatieres: ",listeMatieres)
    var MATIERE_DATA ={
        idMatiere:'',
        codeMatiere:'',
        libelleMatiere:'',
        idClasse:-1,
        idJour:'',
        heureDeb:'',
        heureFin:'',
        tabProfsID:[]
    };
    var parent, draggableSon;
    var tabMatiere =[];
    
    for (var i = 0; i < listeMatieres.length; i++) {
        
        tabMatiere = listeMatieres[i].split('*');
        parent =  document.getElementById('matiere_' + tabMatiere[1]);
        draggableSon = document.getElementById('matiere_' + tabMatiere[1]+'_sub');
        parent.className = classes.matiereStyle;  
        parent.title = tabMatiere[0];
        
        MATIERE_DATA = {};
        MATIERE_DATA.idMatiere = 'matiere_' + tabMatiere[1];
        MATIERE_DATA.libelleMatiere = tabMatiere[0];
        MATIERE_DATA.codeMatiere = tabMatiere[1];
        CURRENT_MATIERE_LIST[i] = MATIERE_DATA;
        
        draggableSon.textContent = tabMatiere[0];
        draggableSon.className = classes.matiereTitleStyle;                     
              
    }
    MATIERE_DATA = {};
    console.log(CURRENT_MATIERE_LIST);
    currentUiContext.setCURRENT_MATIERE_LIST(CURRENT_MATIERE_LIST);
}
function Evaluate(val){
    if(val==''||val==' '|| isNaN(val)) return 0;
    else return eval(val);

}
function droppedProfClickHandler(e){
    var droppedProfDiv = e.target.id;
    //On enleve l'extension _sub ou _img
    droppedProfDiv = droppedProfDiv.substring(0,droppedProfDiv.length-4)
    profZoneClickedHandler(droppedProfDiv);  
    console.log(droppedProfDiv) 
}
function  isCellSelected (cellId) {
    console.log("isCellSelected-CURRENT_DROPPED_MATIERE_LIST: ",CURRENT_DROPPED_MATIERE_LIST);
    var index = CURRENT_DROPPED_MATIERE_LIST.findIndex((matiere)=>matiere.idMatiere == cellId)
    console.log(CURRENT_DROPPED_MATIERE_LIST[index])
    return (CURRENT_DROPPED_MATIERE_LIST[index].isSelected == true);
}
function getCountSelectedDroppedMatieres(){
    var count = 0;
    for(var i=0 ; i<CURRENT_DROPPED_MATIERE_LIST.length; i++){
        if(CURRENT_DROPPED_MATIERE_LIST[i].isSelected==true) count++;
    }
    return count;
}
function getCountSelectedDroppedProfs(){
    var count = 0;
    for(var i=0 ; i<CURRENT_DROPPED_PROFS_LIST.length; i++){
        if(CURRENT_DROPPED_PROFS_LIST[i].isSelected==true) count++;
    }
    return count;
}
function selectedDroppedMatiereHaveSameCode(){
    var areSame = true;
    var i = 1;
    var firstSelectedIndex = CURRENT_DROPPED_MATIERE_LIST.findIndex((matiere)=>matiere.isSelected==true);
    var codeMatiere = CURRENT_DROPPED_MATIERE_LIST[firstSelectedIndex].codeMatiere;

    while(i < CURRENT_DROPPED_MATIERE_LIST.length && areSame==true) {
        if(CURRENT_DROPPED_MATIERE_LIST[i].isSelected == true && CURRENT_DROPPED_MATIERE_LIST[i].codeMatiere != codeMatiere) areSame = false;
        i++;       
    }
    return areSame;
}
function clearCellSelection(){
    var countSelected = getCountSelectedDroppedMatieres()
    if (countSelected >0) {
        for(var i=0; i<CURRENT_DROPPED_MATIERE_LIST.length; i++){ 
            if(CURRENT_DROPPED_MATIERE_LIST[i].isSelected){
                // disSelectCell(CURRENT_DROPPED_MATIERE_LIST[i].idMatiere);
                disSelectCell(CURRENT_DROPPED_MATIERE_LIST[i].idMatiere);
            }         
           
        }
        //SELECTED_MATIERE_ID='';
    }  
}
function selectCell(cellId){
   
    if(!isCellSelected(cellId)) {
        var matiereIndex = CURRENT_DROPPED_MATIERE_LIST.findIndex((matiere)=>matiere.idMatiere == cellId);
        CURRENT_DROPPED_MATIERE_LIST[matiereIndex].isSelected = true;      
        document.getElementById(cellId).style.borderColor ='red';
        clearProflist();

        //COUNT_SELECTED_MATIERES ++;
        //SELECTED_MATIERE_TAB.push(cellId);
        
        //if (COUNT_SELECTED_MATIERES==1) SELECTED_MATIERE_ID = cellId;
        //else SELECTED_MATIERE_ID = '';
        // Vider la liste des profs
         
    }
}
function disSelectCell(cellId) {
    if(isCellSelected(cellId)) {
        var matiereIndex = CURRENT_DROPPED_MATIERE_LIST.findIndex((matiere)=> matiere.idMatiere == cellId);
        CURRENT_DROPPED_MATIERE_LIST[matiereIndex].isSelected = false;
        if(document.getElementById(cellId).style.backgroundColor.length==0){
            document.getElementById(cellId).style.borderColor = 'rgb(6, 83, 134)';
        }else{
            document.getElementById(cellId).style.borderColor = document.getElementById(cellId).style.backgroundColor;
        }
       //console.log(document.getElementById(cellId).style.backgroundColor);
        clearProflist();

       /* var index = SELECTED_MATIERE_TAB.findIndex((droppedMatierId)=>cellId == droppedMatierId);        
        if(index>=0) {
            
            
            SELECTED_MATIERE_TAB.splice(index,1);
            COUNT_SELECTED_MATIERES --;

            if(COUNT_SELECTED_MATIERES==1) SELECTED_MATIERE_ID = SELECTED_MATIERE_TAB[0];
            else SELECTED_MATIERE_ID ='';

            // Vider la liste des profs si elle ne l'est pas
            clearProflist();
        }*/
      
    }

}
function getProfsList(codeMatiere, periode){


    var tabProfs,profList;
    var codeMatiere;

    profList = getProfs(codeMatiere)
    tabProfs = profList.split('_');
    initProfListWithProfs(tabProfs);

    /*countMatieres = getCountSelectedDroppedMatieres();
    if(countMatieres == 0) {
        alert('Vous devez selectionner une matiere!');
    } else {
        if(countMatieres > 1) {
            alert('Vous devez selectionner une seule matiere!');
        } else {
            profList = getProfs(codeMatiere)
            tabProfs = profList.split('_');
            initProfListWithProfs(tabProfs);
        } 
    }*/
}
function initProfListWithProfs2(listeProf){
    var parent = document.getElementById('profList');
    var draggableSon, draggableSonText, draggableSonImg;

    clearProflist();
    console.log(listeProf);
  
    for (var i = 0; i < listeProf.length; i++) {
        PROF_DATA = {};
        draggableSon =  document.getElementById('prof_' + listeProf[i].id);
        draggableSonText = document.getElementById('prof_' + listeProf[i].id+'_sub');
        
        draggableSon.className = classesP.profDivStyle;  
        draggableSon.title = listeProf[i].nom+" "+listeProf[i].prenom;       
        
        draggableSonText.textContent = listeProf[i].nom;
        draggableSonText.className = classesP.profTextSyle;            

        draggableSonImg =  document.getElementById('prof_' + listeProf[i].id + '_img');
        draggableSonImg.className = classesP.profImgStyle;

        draggableSonImg = document.querySelector('#prof_' + listeProf[i].id + '_img > img')

        draggableSonImg.setAttribute('src',"images/maleTeacher.png");

        // if(listeProf[i].includes('Mr.')) {
        //     draggableSonImg.setAttribute('src',"images/maleTeacher.png");
        // }else{
        //     draggableSonImg.setAttribute('src',"images/femaleTeacher.png");
        // }
        
        
        PROF_DATA.idProf = 'prof_' +listeProf[i].id;
        PROF_DATA.NomProf = listeProf[i].nom;
        
        CURRENT_PROFS_LIST.push(PROF_DATA);
        currentUiContext.setCurrentProfList(CURRENT_PROFS_LIST);
        PROF_DATA = {};                                     
    }
 
}
// *desactiver
function initProfListWithProfs(listeProf){
    var parent = document.getElementById('profList');
    var draggableSon, draggableSonText, draggableSonImg;

    clearProflist();
    //alert(listeProf);
  
    for (var i = 0; i < listeProf.length; i++) {
        PROF_DATA = {};
        draggableSon =  document.getElementById('prof_' + (i+1));
        draggableSonText = document.getElementById('prof_' + (i+1)+'_sub');
        
        draggableSon.className = classesP.profDivStyle;  
        draggableSon.title = listeProf[i];       
        
        draggableSonText.textContent = listeProf[i];
        draggableSonText.className = classesP.profTextSyle;            

        draggableSonImg =  document.getElementById('prof_' + (i+1) + '_img');
        draggableSonImg.className = classesP.profImgStyle;

        draggableSonImg = document.querySelector('#prof_' + (i+1) + '_img > img')
        if(listeProf[i].includes('Mr.')) {
            draggableSonImg.setAttribute('src',"images/maleTeacher.png");
        }else{
            draggableSonImg.setAttribute('src',"images/femaleTeacher.png");
        }
        
        
        PROF_DATA.idProf = 'prof_' + (i+1);
        PROF_DATA.NomProf = listeProf[i];
        
        CURRENT_PROFS_LIST.push(PROF_DATA);
        PROF_DATA = {};                                     
    }
 
}
function profZoneClickedHandler(id){
    SELECTED_PROF_ID = id;
    var idTab = SELECTED_PROF_ID.split('_');
    var ProfDroppableZone = 'P_'+idTab[3]+'_'+idTab[4]+'_'+idTab[5];
    var index;
       
    if (idTab[0]=='DP') {
        
        index = CURRENT_DROPPED_PROFS_LIST.findIndex((prof)=>prof.idProf == id)
       
        if(index >=0) {
            if(CURRENT_DROPPED_PROFS_LIST[index].isSelected == false){
                CURRENT_DROPPED_PROFS_LIST[index].isSelected = true;
                document.getElementById(SELECTED_PROF_ID).style.borderStyle ='solid';
                document.getElementById(SELECTED_PROF_ID).style.borderWidth ='1px';  
                document.getElementById(SELECTED_PROF_ID).style.borderColor ='red';

            } else {
                CURRENT_DROPPED_PROFS_LIST[index].isSelected = false;
                document.getElementById(SELECTED_PROF_ID).style.borderStyle = null;
                document.getElementById(SELECTED_PROF_ID).style.borderWidth = null;
                document.getElementById(SELECTED_PROF_ID).style.borderColor = null;
            }
 
        } else{
            alert('Le prof selectionne ne figure pas dans la lista des profs')
        }        
    }      
}
function getProfs(codeMatiere){
    
    // switch(codeMatiere){
    //     case '001': return listProfs[1] ;
    //     case '002': return listProfs[2] ;
    //     case '003': return listProfs[3]
    //     default: return listProfs[0];
    //     //case 'matiere_4':   return listProfs[2] ;           
    // }
  
}
function getProfsList2(codeMatiere,periode,liste_prof_current_tranche){
    let idjour = periode.split("DM_")[1].split("_")[0];
    let tranche = periode.split("DM_")[1].split("_")[1]+"_";
    tranche += periode.split("DM_")[1].split("_")[2];
    console.log("tranche: ",tranche)
    console.log("y Periode: ",periode);
    let listProfs = currentUiContext.listProfs;
    let emploiDeTemps = currentUiContext.emploiDeTemps;
    var libre=true;
    let profLibres = [],profOccupes = [];
    let profsMatieres = listProfs.filter((prof)=>prof.id_spe1==codeMatiere||prof.id_spe2==codeMatiere||prof.id_spe3==codeMatiere);
    console.log("*** profsMatieres: ",profsMatieres)
    console.log("*** emploiDeTemps: ",emploiDeTemps)
    let emploi_selected = emploiDeTemps.filter(e=>!e.modify.includes("s")&&e.id_matiere==codeMatiere&&e.id_jour==idjour&&e.libelle==tranche);
    console.log("emploi_selected: ",emploi_selected)
    let emp;
    let idProfs =[];
    for(let j=0;j<emploi_selected.length;j++){
        emploi_selected[j].id_enseignants.forEach(prof => {
            profOccupes.push( prof)
        });
    }
    profOccupes.forEach(p => {
        if (!liste_prof_current_tranche.includes(p.id_enseignants))
        profLibres.push(p)
    });
    liste_prof_current_tranche.forEach(p => {
       if(!profOccupes.includes(p))
            profOccupes.push(p)
    });
    profLibres = profsMatieres.filter(p=>!profOccupes.includes(p.id))


    console.log("*** profLibres: ",profLibres);
    console.log("*** profOccupes: ",profOccupes);
    console.log("*** liste_prof_cureent_tranche: ",liste_prof_current_tranche);
    initProfListWithProfs2(profLibres);

}

/*************************** <JSX Code> ****************************/
   return (              
       <DndProvider backend={HTML5Backend}>
            <div className={classes.formET}>
                <div className={classes.formTitle +' '+classes.margBottom3}>
                    CREATION DES EMPLOIS DE TEMPS PAR CLASSES
                </div>                
 
                <div className={classes.inputRow}>
                    <div className={classes.bold+ ' '+classes.fontSize1} style={{alignSelf:'center'}}>
                        CLASSE  :                       
                    </div>
                    <div>
                        <select id='selectClasse' onChange={dropDownHandler} className={classes.comboBoxStyle} style={{width:'11.3vw', marginBottom:1}}>
                            {(optClasse||[]).map((option)=> {
                                return(
                                    <option  value={option.value}>{option.label}</option>
                                );
                            })}
                        </select>
                    </div>              
                </div>                
                
                <div className={classes.fullSchedule}>

                    <div className={classes.PalettePosition}>
                        <Palette/>
                    </div>

                    <div className={classes.matiereTitle}>Matieres</div>

                    <div className={classes.grilleEtMatiere}> 
                    <div className={classes.grille}>

                            <LigneValeur/>

                            {(currentUiContext.TAB_JOURS).map((jour,indjour) => {
                                return (
                                    
                                    <div id={jour.id} className={jour.numero_jour==1 ? classes.ligneDebut :jour.numero_jour==6? classes.ligneFin : classes.ligne}> 
                                        <Jour jourName={jour.libelle}/>
                                         {currentUiContext.TAB_PERIODES.map((periode,index) => {
                                                return (
                                                    (periode.duree.includes('B_'))?
                                                   <div className={classes.DroppableZone} style={{width:computePauseDivSize(calculDureePause(periode.duree.substring(2)))+'vw'}}>
                                                        <div className={classes.pauseZone}/>
                                                    </div>
                                                    :
                                                    currentUiContext.TAB_JOURS[indjour].tranches[index]==1?
                                                    <div className={classes.DroppableZone} style={{width:computePauseDivSize(calculDureePause(periode.duree))+'vw'}}>
                                                        <DroppableDiv
                                                            id={jour.id+'_'+periode.duree}
                                                            acceptType='matiere'
                                                            CurrentMatiereList = {props.CurrentMatiereList}
                                                            // listProfs = {currentUiContext.listProfs}
                                                            className={classes.droppableDivstyle}
                                                            style={{marginLeft:calculMarge(periode.duree.substring(2))+'vw', }}
                                                        />                                                                                                           
                                                       
                                                        <DroppableDiv
                                                            id={'P_'+jour.id+'_'+periode.duree}
                                                            acceptType='profImage'
                                                            CurrentMatiereList = {props.CurrentMatiereList}
                                                            className={classes.ProfDroppableDivstyle}
                                                        />
                                                    </div>
                                                    :<div className={classes.DroppableZone} style={{width:computePauseDivSize(calculDureePause(periode.duree))+'vw'}}>
                                                    <div className={classes.pauseZone}/>
                                                </div>
                                                    
                                                );
                                            })
                                        } 
                                    </div>
                                );
                            })}                         
                           
                        </div>  
                        <LigneMatieres/>
                    </div>

                    <div className={classes.profSelect}>
                        <div className={classes.profListTitle}> Enseignants</div>
                        <LigneProfs/>
                    </div>                    
                </div>

                <div className={classes.buttonRow}>

                   <CustomButton
                        btnText='Annuler' 
                        buttonStyle={getButtonStyle()}
                        btnTextStyle = {classes.btnTextStyle}
                        btnClickHandler={cancelHandler}
                    />
                    
                    <CustomButton
                        btnText='Enregistrer' 
                        buttonStyle={getButtonStyle()}
                        btnTextStyle = {classes.btnTextStyle}
                        btnClickHandler={UpdateEmploiDeTemps}
                        //disable={(isValid==false)}
                        // disable={(currentUiContext.CURRENT_DROPPED_MATIERE_LIST.length == 0)}
                    />

                    <CustomButton
                        btnText='Imprimer'
                        buttonStyle={getButtonStyle()}
                        btnTextStyle = {classes.btnTextStyle}
                        btnClickHandler={(isValid) ? PrintEmploiDeTemps: null}
                        disable={(isValid==false)}
                    />
                    
                </div>
            </div>
        </DndProvider>
    
    );
}

export default GrilleEmploiTemps;