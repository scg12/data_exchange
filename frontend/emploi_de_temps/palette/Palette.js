import React, { useState } from 'react';

import classes from './Palette.module.css';

import { useContext } from "react";
import UiContext from '../../../../store/UiContext';

import { useTranslation } from "react-i18next";
import '../../../../translation/i18n';
import CustomButton from '../../customButton/CustomButton';
import classesP from './Palette.module.css';

// import {SELECTED_MATIERE_ID, CURRENT_PROFS_LIST, SELECTED_MATIERE_TAB, COUNT_SELECTED_MATIERES, CURRENT_DROPPED_MATIERE_LIST, SELECTED_PROF_ID, SELECTED_PROF_TAB, COUNT_SELECTED_PROFS, CURRENT_DROPPED_PROFS_LIST} from '../ET_Module'
// import {PROFLIST_MAXSIZE, TAB_COLORS} from '../ET_Module';
// import {getProfsList,getProfs, initProfList, setMatiereColor, getCountSelectedDroppedMatieres, updateCountSelectedMatieres, AddValueToSelectedMatiereTab, deleteMatiere, deleteProf, clearProflist} from '../ET_Module';

var PROF_DATA ={
    idProf:'',
    NomProf:'',
    idJour:'',
    heureDeb:'',
    heureFin:'',
    IdMatiere:''
}
let COUNT_SELECTED_PROFS;
let SELECTED_PROF_ID;

let SELECTED_PROF_TAB;
let CURRENT_PROFS_LIST;
let PROFLIST_MAXSIZE;
var TAB_COLORS = {};
TAB_COLORS["GreenDark"] ='rgb(22, 122, 22)';
TAB_COLORS["Green"] ='rgb(60, 170, 60)';
TAB_COLORS["Yellow"] ='rgb(180, 219, 38)';
TAB_COLORS["YellowGold"] ='rgb(228, 224, 7)';
TAB_COLORS["BleuDark"] ='rgb(6, 29, 92)';
TAB_COLORS["Bleu"] ='rgb(43, 86, 206)';
TAB_COLORS["VioletDark"] ='rgb(117, 25, 121)';
TAB_COLORS["Violet"] ='rgb(206, 16, 212)';
TAB_COLORS["Orange"] ='rgb(219, 90, 15)';
TAB_COLORS["Red"] ='rgb(201, 10, 10)';
TAB_COLORS["PinkDark"] ='rgb(95, 22, 65)';
TAB_COLORS["Pink"] ='rgb(212, 16, 92)';
TAB_COLORS["Grey"] ='grey';
TAB_COLORS["Black"] ='rgb(26, 25, 25)';
let CURRENT_DROPPED_MATIERE_LIST;
let CURRENT_DROPPED_PROFS_LIST;

 
function Palette(props) {

    const currentUiContext = useContext(UiContext);
    const [isValid,setIsValid]=useState(false);

    //Cette constante sera lu lors de la configuration de l'utilisateur.
    const selectedTheme = currentUiContext.theme;
    const { t, i18n } = useTranslation();
    
    const changeLanguage = (event) => {
        i18n.changeLanguage(event.target.id);
    };


/*    const listProfs = [
        "Mr. ONDOUA p._Mme. MENGUE A._Mr. ABENA T._Mr. HOMBA S._Mr. Talla J._Mlle. ELIMBI_Mr. ETOA_Mr. BASSOGOG",
        "Mme. Ngo Milend_Mme. Ngo Nouki_Mme. Mendoua_Mme. Mouliom_Mme. Kamga_Mr. Belingua_Mr. Mpenza",
        "Mr. Evina_Mr. Bassagal_Mr. Tindo_Mr. Ateba_Mr. Kembo Ekoko_Mr. Telep_Mme. Ebana_MrMbazoa_Mr. Elimbi"        
    ]*/


    
    function getCurrentButtonTheme()
    {  // Choix du theme courant
       switch(selectedTheme){
            case 'Theme1': return classes.Theme1_buttonStyle;
            case 'Theme2': return classes.Theme2_buttonStyle;
            case 'Theme3': return classes.Theme3_buttonStyle;
            default: return classes.Theme1_buttonStyle;
        }
    }

    function getCurrentFooterTheme()
    {  // Choix du theme courant
       switch(selectedTheme){
            case 'Theme1': return classes.Theme1_footer;
            case 'Theme2': return classes.Theme2_footer;
            case 'Theme3': return classes.Theme3_footer;
            default: return classes.Theme1_footer;
        }
    }

    /*function setMatiereColor(colorString){
        alert('ici couleeur')
        var countSelectedMatieres = getCountSelectedDroppedMatieres();
        for (var i= 0; i< countSelectedMatieres; i++){
            if(CURRENT_DROPPED_MATIERE_LIST[i].isSelected==true){
                //console.log('pepa',CURRENT_DROPPED_MATIERE_LIST[i])
                document.getElementById(CURRENT_DROPPED_MATIERE_LIST[i].idMatiere).style.backgroundColor = TAB_COLORS[colorString];
                document.getElementById(CURRENT_DROPPED_MATIERE_LIST[i].idMatiere).style.borderColor = TAB_COLORS[colorString];
                
                if (colorString=='Yellow'|| colorString=='YellowGold'){
                    document.getElementById(CURRENT_DROPPED_MATIERE_LIST[i].idMatiere).style.color = 'black';
                }

            }
           
        }

        updateCountSelectedMatieres(0);
        AddValueToSelectedMatiereTab('',-1);
        
    }*/

    function deleteElements(){
        CURRENT_DROPPED_MATIERE_LIST = currentUiContext.CURRENT_DROPPED_MATIERE_LIST;
        CURRENT_DROPPED_PROFS_LIST = currentUiContext.CURRENT_DROPPED_PROFS_LIST;
        console.log("CURRENT_DROPPED_MATIERE_LIST: ",CURRENT_DROPPED_MATIERE_LIST);
        deleteMatiere();
        deleteProf();
        currentUiContext.addMatiereToDroppedMatiereList(CURRENT_DROPPED_MATIERE_LIST,-1);
        currentUiContext.addProfToDroppedProfList(CURRENT_DROPPED_PROFS_LIST,-1);
    }
    function getCountSelectedDroppedMatieres(){
        var count = 0;
        for(var i=0 ; i<CURRENT_DROPPED_MATIERE_LIST.length; i++){
            if(CURRENT_DROPPED_MATIERE_LIST[i].isSelected==true) count++;
        }
        return count;
    }
    function deleteMatiere () {
        var DropZoneId,toDeleIndex, droppedProfId, droppedProfZone,idTab;
        var countMatiere, tabPos, profDropZone, AssociatedProfCount;
        countMatiere = getCountSelectedDroppedMatieres();
        // var tabSelectedDroppedMatieres = getSelectedDroppedMatieres();
       
        tabPos = 0;
        console.log('ggdgdgd',countMatiere, CURRENT_DROPPED_MATIERE_LIST);
        while(tabPos<countMatiere){
            console.log(tabPos+'fois')
            var toDeleIndex = CURRENT_DROPPED_MATIERE_LIST.findIndex((matiere)=>matiere.isSelected == true)
            DropZoneId = CURRENT_DROPPED_MATIERE_LIST[toDeleIndex].idMatiere;
            idTab = DropZoneId.split('_');
            //'DM_'+jour +'_'+ PeriodDeb +'_'+ PeriodFin;
            droppedProfZone ='P_'+idTab[1]+'_'+idTab[2]+'_'+idTab[3];
                        
            //toDeleIndex = CURRENT_DROPPED_MATIERE_LIST.findIndex((matiere)=>matiere.idMatiere == DropZoneId);             
            console.log(CURRENT_DROPPED_MATIERE_LIST[toDeleIndex]);
            if(toDeleIndex >= 0){
                console.log('matiere a supprimer',CURRENT_DROPPED_MATIERE_LIST[toDeleIndex]);
                var matiereToDeleteProf = {...CURRENT_DROPPED_MATIERE_LIST[toDeleIndex]};
                if (CURRENT_DROPPED_MATIERE_LIST[toDeleIndex].tabProfsID.length > 0) {
                    AssociatedProfCount = CURRENT_DROPPED_MATIERE_LIST[toDeleIndex].tabProfsID.length;
                    
                    while(AssociatedProfCount > 0){
                        droppedProfId = CURRENT_DROPPED_MATIERE_LIST[toDeleIndex].tabProfsID.shift();
                        profDropZone =  document.getElementById(droppedProfId);  
                        var children = profDropZone.childNodes;   
                        for(var i = 0; i < children.length; i++){
                            children[i].remove();
                        } 
                        profDropZone.remove();
                
                        if (profDropZone.style.borderColor=='red'){
                            profDropZone.style.borderStyle = null;
                            profDropZone.style.borderWidth = null;
                            profDropZone.style.borderColor = null;
                        }                   
                        AssociatedProfCount--;
                    }  
                }
                CURRENT_DROPPED_MATIERE_LIST.splice(toDeleIndex,1);
                document.getElementById(DropZoneId).remove();
            }
            tabPos++;

            let emploiDeTemps = currentUiContext.emploiDeTemps;
            let emp = emploiDeTemps.filter(e=>e.id_classe==currentUiContext.currentIdClasseEmploiTemps&&
                e.id_jour==idTab[1]&&e.libelle==idTab[2]+"_"+idTab[3]&&e.id_matiere==matiereToDeleteProf.codeMatiere);
            let empIndex = emploiDeTemps.findIndex(e=>e.id_classe==currentUiContext.currentIdClasseEmploiTemps&&
                e.id_jour==idTab[1]&&e.libelle==idTab[2]+"_"+idTab[3]&&e.id_matiere==matiereToDeleteProf.codeMatiere);
                console.log("empIndex: ",empIndex);

            if (emp.length>0){
                let empToUpdate = emp[0];
                // C'est un cours qui a été créé pendant la session courante on peut simplement le supprimer
                if(empToUpdate.modify.includes("c"))
                      emploiDeTemps.splice(empIndex,1)
                // Ca vient de la bd donc la suppression doit se faire en bd
                else{
                    empToUpdate.modify +="s";
                    emploiDeTemps.splice(empIndex,1,empToUpdate)
                    console.log("emploiDeTemps: ",emploiDeTemps);
                }

                    
                    currentUiContext.setEmploiDeTemps(emploiDeTemps);
                

            }
        }
        currentUiContext.addMatiereToDroppedMatiereList(CURRENT_DROPPED_MATIERE_LIST,-2);
        clearProflist();
    }
    function deleteProf (){
        var DropProfId, children, profDropZone;
        var associatedMatiere, idTab, matiereIndex,profIndex, indexProf, profId;
        var countProfs = getCountSelectedDroppedProfs();
        
        if (countProfs >0) {
           
            for(var i=0; i < countProfs; i++){
               
                profIndex = CURRENT_DROPPED_PROFS_LIST.findIndex((prof)=>prof.isSelected == true)
                if(profIndex>=0){
                    DropProfId = CURRENT_DROPPED_PROFS_LIST[profIndex].idProf;
                    associatedMatiere = CURRENT_DROPPED_PROFS_LIST[profIndex].idMatiere;
                    matiereIndex = CURRENT_DROPPED_MATIERE_LIST.findIndex((matiere)=>matiere.idMatiere == associatedMatiere)
                    
                    if (matiereIndex>=0){
                        indexProf = CURRENT_DROPPED_MATIERE_LIST[matiereIndex].tabProfsID.findIndex((prof)=> prof == DropProfId);
                        if (profIndex>=0) CURRENT_DROPPED_MATIERE_LIST[matiereIndex].tabProfsID.splice(indexProf,1);
                        else{alert("Erreur, le prof n'est pas enregistre pour une matiere")}
                       
    
                        profDropZone =  document.getElementById(DropProfId);  
                        children = profDropZone.childNodes;   
                        for(var i = 0; i < children.length; i++){
                            children[i].remove();
                        } 
                        profDropZone.remove();
                
                        if (profDropZone.style.borderColor=='red'){
                            profDropZone.style.borderStyle = null;
                            profDropZone.style.borderWidth = null;
                            profDropZone.style.borderColor = null;
                            profDropZone.className = null;
                        }
                    }                
                    CURRENT_DROPPED_PROFS_LIST.splice(profIndex,1);
                }                      
            }
            currentUiContext.addProfToDroppedProfList(CURRENT_DROPPED_PROFS_LIST,-1);
            SELECTED_PROF_TAB =[];
            COUNT_SELECTED_PROFS = 0;
            SELECTED_PROF_ID='';        
        } 
    }
    function setMatiereColor(colorString){
    
        var countSelectedMatieres = getCountSelectedDroppedMatieres();
       if(countSelectedMatieres){
            for (var i= 0; i< CURRENT_DROPPED_MATIERE_LIST.length; i++){
                
                if(CURRENT_DROPPED_MATIERE_LIST[i].isSelected==true){
                    
                    //CURRENT_DROPPED_MATIERE_LIST[i].isSelected = false;
                    document.getElementById(CURRENT_DROPPED_MATIERE_LIST[i].idMatiere).style.backgroundColor = TAB_COLORS[colorString];
                    //document.getElementById(CURRENT_DROPPED_MATIERE_LIST[i].idMatiere).style.borderColor = TAB_COLORS[colorString];
                    
                    if (colorString=='Yellow'|| colorString=='YellowGold'){
                        document.getElementById(CURRENT_DROPPED_MATIERE_LIST[i].idMatiere).style.color = 'black';
                    }
    
                }
                
            }
    
        }
    }
    function clearProflist(){
        var draggableSon, draggableSonText, draggableSonImg;
        var listProfs =currentUiContext.listProfs;
        PROFLIST_MAXSIZE =listProfs.length;
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
    function getCountSelectedDroppedProfs(){
        var count = 0;
        for(var i=0 ; i<CURRENT_DROPPED_PROFS_LIST.length; i++){
            if(CURRENT_DROPPED_PROFS_LIST[i].isSelected==true) count++;
        }
        return count;
    }
    // function getProfsList2(codeMatiere, listProfs,emploiDeTemps,idjour,h_deb,h_fin)
    function getProfsList2(codeMatiere)
    {   console.log("codeMatiere: ",codeMatiere);
        var libre=true;
        let listProfs = currentUiContext.listProfs;
        let emploiDeTemps = currentUiContext.emploiDeTemps
        let profLibres = [];
        let profsMatieres = listProfs.filter((prof)=>prof.id_spe1==codeMatiere||prof.id_spe2==codeMatiere||prof.id_spe3==codeMatiere);
        console.log("*** listProfs: ",listProfs)
        for(let i=0;i<profsMatieres.length;i++){
            libre = true;
            for(let j=0;j<emploiDeTemps.length;j++){
                if(emploiDeTemps[j].id_enseignants.includes(profsMatieres[i].id)){
                    // console.log("==EGALITE  emploiDeTemps[j]: ",emploiDeTemps[j],"profsMatieres[i]: ",profsMatieres[i],emploiDeTemps[j].id_enseignants.includes(profsMatieres[i].id))
                    libre=false;
                    break;
                }
            }
            if (libre) profLibres.push(profsMatieres[i])
        }
        console.log("*** profLibres: ",profLibres)
        // profList = getProfs(codeMatiere)
        // tabProfs = profList.split('_');
        // initProfListWithProfs2(profsMatieres);
        initProfListWithProfs2(profLibres);
    
    }
    function initProfListWithProfs2(){
        var parent = document.getElementById('profList');
        var draggableSon, draggableSonText, draggableSonImg;
        let listeProf = currentUiContext.listeProf;
        clearProflist();
        //alert(listeProf);
      
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
            PROF_DATA = {};                                     
        }
     
    }

    /*function initProfList(listeProf){
        var parent = document.getElementById('profList');
        var draggableSon, draggableSonText, draggableSonImg;

        clearProflist();
        //alert(listeProf);
      
        for (var i = 0; i < listeProf.length; i++) {
            PROF_DATA = {};
            draggableSon =  document.getElementById('prof_' + (i+1));
            draggableSonText = document.getElementById('prof_' + (i+1)+'_sub');
            
            draggableSon.className = classes.profDivStyle;  
            draggableSon.title = listeProf[i];       
            
            draggableSonText.textContent = listeProf[i];
            draggableSonText.className = classes.profTextSyle;            

            draggableSonImg =  document.getElementById('prof_' + (i+1) + '_img');
            draggableSonImg.className = classes.profImgStyle;

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

    function getProfs(codeMatiere){
        
        switch(codeMatiere){
            case '001': return listProfs[1] ;
            case '002': return listProfs[2] ;
            default: return listProfs[0];
            //case 'matiere_4':   return listProfs[2] ;           
        }
      
    }

    function getProfsList(periode){
        var tabProfs,profList;
        var codeMatiere, countMatieres, indexMatiere;
        countMatieres = getCountSelectedDroppedMatieres();
        if(countMatieres == 0) {
            alert('Vous devez selectionner une matiere!');
        } else {
            if(countMatieres > 1) {
                alert('Vous devez selectionner une seule matiere!');
            } else {
                indexMatiere = CURRENT_DROPPED_MATIERE_LIST.findIndex((matiere)=>matiere.isSelected==true);
                codeMatiere = CURRENT_DROPPED_MATIERE_LIST[indexMatiere]
                profList = getProfs(codeMatiere)
                tabProfs = profList.split('_');
                initProfList(tabProfs);
            } 
        }
    }*/
   
    return (       
        <div className={classes.paletteContainer}> 
            <div className={classes.buttonContainer}>
                <CustomButton
                    btnText=''
                    buttonStyle={classes.buttonStyle}
                    //btnTextStyle = {classes.btnTextStyleX}
                    
                    hasIconImg= {true}
                    imgSrc='images/delete.png'
                    imgStyle = {classes.imgStyle}
                    btnClickHandler={deleteElements}
                />

                <CustomButton
                    btnText='' 
                    buttonStyle={classes.buttonStyle}
                    /*btnTextStyle = {classes.btnTextStyle}*/
                    hasIconImg= {true}
                    imgSrc='images/teacher.png'
                    imgStyle = {classes.imgStyleTeacher}
                    btnClickHandler={getProfsList2}
                    //disable={(isValid==true)}
                />
                
               {/* <CustomButton
                    btnText='+' 
                    buttonStyle={getCurrentButtonTheme()}
                    btnTextStyle = {classes.btnTextStyle}
                    btnClickHandler={setMatiereColor('Yellow')}
                    disable={(isValid==true)}
                />

                <CustomButton
                    btnText='-' 
                    buttonStyle={getCurrentButtonTheme()}
                    btnTextStyle = {classes.btnTextStyle}
                    btnClickHandler={setMatiereColor('Yellow')}
                    disable={(isValid==true)}
                /> */}
            </div>
                        
            <div className={classes.colorContainer}>
                <div className={classes.colorRow}>
                    <CustomButton
                        btnText=''
                        buttonStyle={classes.buttonStyleGreenDark}
                        /*btnTextStyle = {classes.btnTextStyle}*/
                        btnClickHandler={()=>setMatiereColor('GreenDark')}
                        /*disable={(isValid==false)}*/
                    />

                    <CustomButton
                        btnText=''
                        buttonStyle={classes.buttonStyleGreen}
                        /*btnTextStyle = {classes.btnTextStyle}*/
                        btnClickHandler={()=>setMatiereColor('Green')}
                        /*disable={(isValid==false)}*/
                    />
                </div>
                <div className={classes.colorRow}>
                    <CustomButton
                        btnText=''
                        buttonStyle={classes.buttonStyleYellow}
                        /*btnTextStyle = {classes.btnTextStyle}*/
                        btnClickHandler={()=>setMatiereColor('Yellow')}
                        /*disable={(isValid==false)}*/
                    />

                    <CustomButton
                        btnText=''
                        buttonStyle={classes.buttonStyleYellowGold}
                        /*btnTextStyle = {classes.btnTextStyle}*/
                        btnClickHandler={()=>setMatiereColor('YellowGold')}
                        /*disable={(isValid==false)}*/
                    />
                </div>
                <div className={classes.colorRow}>
                    <CustomButton
                        btnText=''
                        buttonStyle={classes.buttonStyleBleuDark}
                        /*btnTextStyle = {classes.btnTextStyle}*/
                        btnClickHandler={()=>setMatiereColor('BleuDark')}
                        /*disable={(isValid==false)}*/
                    />

                    <CustomButton
                        btnText=''
                        buttonStyle={classes.buttonStyleBleu}
                        /*btnTextStyle = {classes.btnTextStyle}*/
                        btnClickHandler={()=>setMatiereColor('Bleu')}
                        /*disable={(isValid==false)}*/
                    />
                </div>
                <div className={classes.colorRow}>
                    <CustomButton
                        btnText=''
                        buttonStyle={classes.buttonStylePinkDark}
                        /*btnTextStyle = {classes.btnTextStyle}*/
                        btnClickHandler={()=>setMatiereColor('PinkDark')}
                        /*disable={(isValid==false)}*/
                    />

                    <CustomButton
                        btnText=''
                        buttonStyle={classes.buttonStylePink}
                        /*btnTextStyle = {classes.btnTextStyle}*/
                        btnClickHandler={()=>setMatiereColor('Pink')}
                        /*disable={(isValid==false)}*/
                    />
                </div>

                <div className={classes.colorRow}>
                    <CustomButton
                         btnText=''
                        buttonStyle={classes.buttonStyleViolet}
                        /*btnTextStyle = {classes.btnTextStyle}*/
                        btnClickHandler={()=>setMatiereColor('Violet')}
                         /*disable={(isValid==false)}*/
                    />

                    <CustomButton
                        btnText=''
                        buttonStyle={classes.buttonStyleVioletDark}
                       /*btnTextStyle = {classes.btnTextStyle}*/
                        btnClickHandler={()=>setMatiereColor('VioletDark')}
                        /*disable={(isValid==false)}*/
                    />
                </div>

                <div className={classes.colorRow}>
                    <CustomButton
                        btnText=''
                        buttonStyle={classes.buttonStyleOrange}
                       /*btnTextStyle = {classes.btnTextStyle}*/
                        btnClickHandler={()=>setMatiereColor('Orange')}
                         /*disable={(isValid==false)}*/
                    />

                    <CustomButton
                        btnText=''
                        buttonStyle={classes.buttonStyleRed}
                        /*btnTextStyle = {classes.btnTextStyle}*/
                        btnClickHandler={()=>setMatiereColor('Red')}
                         /*disable={(isValid==false)}*/
                    />
                </div>

                <div className={classes.colorRow}>
                    <CustomButton
                        btnText='' 
                        buttonStyle={classes.buttonStyleGrey}
                        /*btnTextStyle = {classes.btnTextStyle}*/
                        btnClickHandler={()=>setMatiereColor('Grey')}
                         /*disable={(isValid==false)}*/
                    />

                    <CustomButton
                        btnText=''
                        buttonStyle={classes.buttonStyleBlack}
                        /*btnTextStyle = {classes.btnTextStyle}*/
                        btnClickHandler={()=>setMatiereColor('Black')}
                         /*disable={(isValid==false)}*/
                    />
                </div>
              
            </div>
            
        </div>
       
    );
}

export default Palette;