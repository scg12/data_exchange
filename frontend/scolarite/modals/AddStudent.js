import React from 'react';
import { useFilePicker } from 'use-file-picker';
import classes from "../subPages/SubPages.module.css";
import CustomButton from "../../../customButton/CustomButton";
import UiContext from "../../../../../store/UiContext";
import { useContext, useState, useEffect } from "react";
import FormPuce from '../../../formPuce/FormPuce';
import axiosInstance from '../../../../../axios';
import Select from 'react-select';

var CURRENT_ELEVE = {
    //---Infos Perso 
    matricule : '',
    nom : '',
    prenom : '',
    date_naissance : '',
    lieu_naissance : '',
    adresse : '',
    sexe : 'M',
    photo_url : '',           
    //---Infos Scolaires
    date_entree : '',
    etab_origine:'',
    classe:'',
    filiere:'',
    redouble : false,
    //---Infos des parents
    nom_pere : '',
    email_pere : '',
    tel_pere : '',
    prenom_pere :'',

    nom_mere : '',
    email_mere : '',
    tel_mere : '',
    prenom_mere : '',      
             
};

function AddStudent(props) {
    const currentUiContext = useContext(UiContext);
    const [isValid, setIsValid] = useState(false);
    const [modalOpen, setModalOpen] = useState(0); //0 = close, 1=creation, 2=modif
    const selectedTheme = currentUiContext.theme;
    const[etape,setEtape] = useState(1);
    const [etape1InActiv, setEtape1Activ] = useState(setButtonDisable(1));
    const [etape2InActiv, setEtape2Activ] = useState(setButtonDisable(2));
    const [etape3InActiv, setEtape3Activ] = useState(setButtonDisable(3));

    useEffect(()=> {
        if(currentUiContext.formInputs.length > 0){
            CURRENT_ELEVE = {
                //---Infos Perso 
                matricule : putToEmptyStringIfUndefined(currentUiContext.formInputs[11]),
                nom : putToEmptyStringIfUndefined(currentUiContext.formInputs[0]),
                prenom : putToEmptyStringIfUndefined(currentUiContext.formInputs[1]),
                date_naissance : putToEmptyStringIfUndefined(currentUiContext.formInputs[2]),
                lieu_naissance : putToEmptyStringIfUndefined(currentUiContext.formInputs[3]),
                adresse : '',
                sexe : 'M',
                photo_url : '',           
                //---Infos Scolaires
                date_entree : '',
                etab_origine:putToEmptyStringIfUndefined(currentUiContext.formInputs[4]),
                classe:'',
                filiere:'',
                redouble : false,
                //---Infos des parents
                nom_pere : putToEmptyStringIfUndefined(currentUiContext.formInputs[5]),
                email_pere : putToEmptyStringIfUndefined(currentUiContext.formInputs[6]),
                tel_pere : putToEmptyStringIfUndefined(currentUiContext.formInputs[7]),
                prenom_pere :'',
        
                nom_mere : putToEmptyStringIfUndefined(currentUiContext.formInputs[8]),
                email_mere : putToEmptyStringIfUndefined(currentUiContext.formInputs[9]),
                tel_mere : putToEmptyStringIfUndefined(currentUiContext.formInputs[10]),
                prenom_mere : '',      
                         
            };       
        }
    },[]);

    const [openFileSelector, { filesContent, loading, errors }] = useFilePicker({
        readAs: 'DataURL',
        accept: 'image/*',
        multiple: false,
        limitFilesConfig: { max: 1 },
        // minFileSize: 0.1, // in megabytes
        maxFileSize: 50,
        imageSizeRestrictions: {
          maxHeight: 500, // in pixels
          maxWidth: 500,
          minHeight: 32,
          minWidth: 32,
        },
    });
    
    if (loading) {
        return <div>Loading...</div>;
    }

    if (errors.length) {
        getUploadError();
        console.log(errors);
    }

    

    function setButtonDisable(etape){
        switch(props.formMode){  
            case 'creation':                     
                switch(etape){
                    case 1: return false;
                    case 2: return true;
                    case 3: return true;                    
                }
            case 'modif':
                switch(etape){
                    case '1': return false;
                    case '2': return false;
                    case '3': return false;                    
                }
            default : 
                switch(etape){
                    case '1': return false;
                    case '2': return false;
                    case '3': return false;                    
                }
        }         
  
    }

    function getGridButtonStyle()
    { // Choix du theme courant
        switch(selectedTheme){
            case 'Theme1': return classes.Theme1_gridBtnstyle + ' '+ classes.margRight5P ;
            case 'Theme2': return classes.Theme2_gridBtnstyle + ' '+ classes.margRight5P;
            case 'Theme3': return classes.Theme3_gridBtnstyle + ' '+ classes.margRight5P;
            default: return classes.Theme1_gridBtnstyle + ' '+ classes.margRight5P;
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

    function getSmallButtonStyle()
    { // Choix du theme courant
      switch(selectedTheme){
        case 'Theme1': return classes.Theme1_BtnstyleSmall ;
        case 'Theme2': return classes.Theme2_BtnstyleSmall ;
        case 'Theme3': return classes.Theme3_BtnstyleSmall ;
        default: return classes.Theme1_BtnstyleSmall ;
      }
    }

    function getCurrentHeaderTheme()
    {  // Choix du theme courant
       switch(selectedTheme){
            case 'Theme1': return classes.Theme1_formHeader+ ' ' + classes.formHeader;
            case 'Theme2': return classes.Theme2_formHeader + ' ' + classes.formHeader;
            case 'Theme3': return classes.Theme3_formHeader + ' ' +classes.formHeader;
            default: return classes.Theme1_formHeader + ' ' +classes.formHeader;
        }
    }


    const optOk=[
        {value: true,  label:'Oui'   },
        {value: false,  label:'Non'  }
    ];

    const optSexe=[        
        {value: 'M',  label:'Masculin' },
        {value: 'F',  label:'Feminin'  }
    ];

    const optStatut=[
        {value: 'mere',  label:'Mere'  },
        {value: 'pere',  label:'Pere'  },
        {value: 'tuteur',  label:'Tuteur'  },
    ];

    const optClasse=[
        {value: '6eme',  label:'6eme'  },
        {value: '5ieme',  label:'5ieme'  },
        {value: '4ieme',  label:'4ieme'  },
    ];

    const optFiliere=[
        {value: 'all',  label:'Allemand'  },
        {value: 'esp',  label:'Espagnol'  },
        {value: 'lat',  label:'Latin'},
        {value: 'c',    label:'Scientifique'    },
        {value: 'd',    label:'D'    },
    ];

    const selectBigtyles = {
        control: base => ({
            ...base,
            height: '2.5vh',
            minHeight: '2.5vh',
            width:'12vw',
            minwidth:'12vw',
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
              height: state.isSelected ? '4.7vh': '4.7vh',
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

    const selectMediumStyles = {
        control: base => ({
            ...base,
            height: '4.7vh',
            minHeight: '4.7vh',
            width:'10vw',
            minwidth:'10vw',
            paddingBottom : 15,
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
              height: state.isSelected ? '4.3vh': '4.3vh',
              marginTop: state.isSelected ? '-1.4vh' : '-1.4vh'
          }),        
          dropdownIndicator:(base,state) => ({
              ...base,
              marginTop: state.isSelected ? '-2.7vh' : '-2.7vh',
              fontSize: state.isSelected ? '1vw' : '1vw'
          }),        
          singleValue: (base,state) => ({
              ...base,
              marginTop: state.isSelected ? '-4.7vh' : '-4.7vh',
              fontSize:  state.isSelected ? '0.9vw' : '0.9vw',
              fontWeight: state.isSelected ? '300' : '300'
          })       
    };

    const selectSmallStyles = {
        control: base => ({
            ...base,
            height: '4.7vh',
            minHeight: '4.7vh',
            width:'7vw',
            minwidth:'7vw',
            paddingBottom : 15,
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
              height: state.isSelected ? '4.3vh': '4.3vh',
              marginTop: state.isSelected ? '-1.4vh' : '-1.4vh'
          }),        
          dropdownIndicator:(base,state) => ({
              ...base,
              marginTop: state.isSelected ? '-2.7vh' : '-2.7vh',
              fontSize: state.isSelected ? '1vw' : '1vw'
          }),        
          singleValue: (base,state) => ({
              ...base,
              marginTop: state.isSelected ? '-4.7vh' : '-4.7vh',
              fontSize:  state.isSelected ? '0.9vw' : '0.9vw',
              fontWeight: state.isSelected ? '670' : '670'
          })       
    };
    
    /************************************ Handlers ************************************/    
    function getUploadError(){
        var errorMsg;
        if(errors.length){
            if(errors[0].fileSizeTooSmall)  {
                errorMsg = 'Le fichier selectionne est trop lourd! la taille du fichier ne doit pas exceder 50Mo !!!';
                return errorMsg;
            }
            
            if(errors[0].fileSizeToolarge)  {
                errorMsg = 'Le fichier selectionne est tres petit! la taille du fichier doit depasser 0.5ko !!!';
                return errorMsg;
            }

            if(errors[0].imageHeightTooSmall)  {
                errorMsg = 'Le fichier a de tres petites dimension !!!';
                return errorMsg;
            }

            if(errors[0].imageWidthTooSmall)  {
                errorMsg = 'Le fichier a de tres petites dimension !!!';
                return errorMsg;
            }    

            if(errors[0].imageHeightTooBig)  {
                errorMsg = 'Le fichier a de grandes dimensions  !!!';
                return errorMsg;
            }

            if(errors[0].imageWidthTooBig)  {
                errorMsg = 'Le fichier a de grandes dimensions  !!!';
                return errorMsg;
            }            
        }       
    }

    function gotoStep2Handler(){
        var errorDiv = document.getElementById('errMsgPlaceHolder');
        getFormData1();
        if(formDataCheck1(CURRENT_ELEVE).length==0){
            if(errorDiv.textContent.length!=0){
                errorDiv.className = null;
                errorDiv.textContent = '';
            }      
            setEtape2Activ(false);
            setEtape(2);
            setFormData2();

        } else {
            setEtape2Activ(true);
            setEtape3Activ(true);           
            errorDiv.className = classes.formErrorMsg;
            errorDiv.textContent = formDataCheck1(CURRENT_ELEVE);
        }
    }

    function backToStep1Handler(){
        setEtape2Activ(true);
        setEtape(1);
        setFormData1();
    }

    function gotoStep3Handler(){
        var errorDiv = document.getElementById('errMsgPlaceHolder');
        getFormData2();
        if(formDataCheck2(CURRENT_ELEVE).length==0){
           if(errorDiv.textContent.length!=0){
                errorDiv.className = null;
                errorDiv.textContent = '';
            }         
            setEtape3Activ(false);
            setEtape(3);
            setFormData3();

        } else {
            if(etape3InActiv==false) setEtape3Activ(true)
            errorDiv.className = classes.formErrorMsg;
            errorDiv.textContent = formDataCheck1(CURRENT_ELEVE);
        }
    }

    function backToStep2Handler(){
        setEtape3Activ(true);
        setEtape(2);
        setFormData2();
    }

    function finishAllSteps(){
        var errorDiv = document.getElementById('errMsgPlaceHolder');
        //console.log('avant:',CURRENT_ELEVE);
        getFormData3();
        //console.log('apres:',CURRENT_ELEVE);
        if(formDataCheck3(CURRENT_ELEVE).length==0){
           if(errorDiv.textContent.length!=0){
                errorDiv.className = null;
                errorDiv.textContent = '';
            }         
            props.actionHandler(CURRENT_ELEVE);
            props.cancelHandler();

        } else {
            errorDiv.className = classes.formErrorMsg;
            errorDiv.textContent = formDataCheck3(CURRENT_ELEVE);
        }
    }   

    function putToEmptyStringIfUndefined(chaine){
        if (chaine==undefined) return '';
        else return chaine;
    }
    
    function getFormData1(){
        CURRENT_ELEVE.matricule = document.getElementById('matricule').value;
        CURRENT_ELEVE.nom = (document.getElementById('nom').value !='') ? putToEmptyStringIfUndefined(document.getElementById('nom').value).trim() : putToEmptyStringIfUndefined(document.getElementById('nom').defaultValue).trim();
        CURRENT_ELEVE.prenom = (document.getElementById('prenom').value !='') ? putToEmptyStringIfUndefined(document.getElementById('prenom').value).trim() : putToEmptyStringIfUndefined(document.getElementById('prenom').defaultValue).trim();
        CURRENT_ELEVE.date_naissance = (document.getElementById('date_naissance').value !='') ? putToEmptyStringIfUndefined(document.getElementById('date_naissance').value).trim() : putToEmptyStringIfUndefined(document.getElementById('date_naissance').defaultValue).trim();
        CURRENT_ELEVE.lieu_naissance = (document.getElementById('lieu_naissance').value !='') ? putToEmptyStringIfUndefined(document.getElementById('lieu_naissance').value).trim() : putToEmptyStringIfUndefined(document.getElementById('lieu_naissance').defaultValue).trim();
        CURRENT_ELEVE.sexe = document.getElementById('sexe').value;
       
        console.log(CURRENT_ELEVE);
    }

    function setFormData1(){
        var tabEleve=[];        
        tabEleve[11] = CURRENT_ELEVE.matricule;
        tabEleve[0]  = CURRENT_ELEVE.nom; 
        tabEleve[1]  = CURRENT_ELEVE.prenom; 
        tabEleve[2]  = CURRENT_ELEVE.date_naissance; 
        tabEleve[3]  = CURRENT_ELEVE.lieu_naissance;

        currentUiContext.setFormInputs(tabEleve);

        /*document.getElementById('nom').value = CURRENT_ELEVE.nom 
        document.getElementById('prenom').value = CURRENT_ELEVE.prenom 
        document.getElementById('date_naissance').value = CURRENT_ELEVE.date_naissance 
        document.getElementById('lieu_naissance').value = CURRENT_ELEVE.lieu_naissance 
        document.getElementById('sexe').value = CURRENT_ELEVE.sexe*/  
    }

    function getFormData2(){
        //on ne prends pas encore en compte l'origine
        CURRENT_ELEVE.etab_origine =(document.getElementById('origine').value !='') ? putToEmptyStringIfUndefined(document.getElementById('origine').value).trim() : putToEmptyStringIfUndefined(document.getElementById('origine').defaultValue).trim();
        CURRENT_ELEVE.classe = document.getElementById('classe').value;
        CURRENT_ELEVE.filiere = document.getElementById('filiere').value;
        CURRENT_ELEVE.redouble = document.getElementById('redouble').value;   

        //console.log(CURRENT_ELEVE);
    }

    function setFormData2(){
       var tabEleve=[];        
        tabEleve[4]  = CURRENT_ELEVE.etab_origine;
        currentUiContext.setFormInputs(tabEleve);
       
        /*tabEleve[0]= CURRENT_ELEVE.nom; 
        tabEleve[1]= CURRENT_ELEVE.prenom; 
        tabEleve[2]= CURRENT_ELEVE.date_naissance; 
        tabEleve[3]= CURRENT_ELEVE.lieu_naissance; 
        tabEleve[4]= CURRENT_ELEVE.sexe;*/
        //Voir comment gerer les selects       
    }

    function getFormData3(){
        CURRENT_ELEVE.nom_pere      = (document.getElementById('nom_pere').value !='') ? putToEmptyStringIfUndefined(document.getElementById('nom_pere').value).trim() : putToEmptyStringIfUndefined(document.getElementById('nom_pere').defaultValue).trim();
        //eleve.prenom_pere   = (document.getElementById('nom_pere').value !='') ? putToEmptyStringIfUndefined(document.getElementById('nom_pere').value).trim() : putToEmptyStringIfUndefined(document.getElementById('nom_pere').defaultValue).trim();
        CURRENT_ELEVE.nom_mere      = (document.getElementById('nom_mere').value !='') ? putToEmptyStringIfUndefined(document.getElementById('nom_mere').value).trim() : putToEmptyStringIfUndefined(document.getElementById('nom_mere').defaultValue).trim();
        //eleve.prenom_mere   = (document.getElementById('nom_pere').value !='') ? putToEmptyStringIfUndefined(document.getElementById('nom_pere').value).trim() : putToEmptyStringIfUndefined(document.getElementById('nom_pere').defaultValue).trim();
        CURRENT_ELEVE.tel_pere      = (document.getElementById('tel_pere').value !='') ? putToEmptyStringIfUndefined(document.getElementById('tel_pere').value).trim() : putToEmptyStringIfUndefined(document.getElementById('tel_pere').defaultValue).trim();
        CURRENT_ELEVE.tel_mere      = (document.getElementById('tel_mere').value !='') ? putToEmptyStringIfUndefined(document.getElementById('tel_mere').value).trim() : putToEmptyStringIfUndefined(document.getElementById('tel_mere').defaultValue).trim();
        CURRENT_ELEVE.email_pere    = (document.getElementById('email_pere').value !='') ? putToEmptyStringIfUndefined(document.getElementById('email_pere').value).trim() : putToEmptyStringIfUndefined(document.getElementById('email_pere').defaultValue).trim();
        CURRENT_ELEVE.email_mere    = (document.getElementById('email_mere').value !='') ? putToEmptyStringIfUndefined(document.getElementById('email_mere').value).trim() : putToEmptyStringIfUndefined(document.getElementById('email_mere').defaultValue).trim();     
        //return CURRENT_ELEVE;
        console.log(CURRENT_ELEVE);
    }

    function setFormData3(){
        var tabEleve=[];
        tabEleve[5] = CURRENT_ELEVE.nom_pere;
        tabEleve[6] = CURRENT_ELEVE.email_pere;
        tabEleve[7] = CURRENT_ELEVE.tel_pere;

        tabEleve[8] = CURRENT_ELEVE.nom_mere;
        tabEleve[9] = CURRENT_ELEVE.email_mere;
        tabEleve[10]= CURRENT_ELEVE.tel_mere;        
        
        currentUiContext.setFormInputs(tabEleve);
    }

    function formDataCheck1(eleve){       
        var errorMsg='';
        if(eleve.nom.length == 0){
            errorMsg="Veuillez entrer le Nom de l'eleve !";
            return errorMsg;
        }

        if (eleve.prenom.length == 0) {
            errorMsg="Veuillez entrer le Prenom de l'eleve !";
            return errorMsg;
        }

        if(eleve.date_naissance.length == 0) {
            errorMsg="Veuillez entrer une date de naissance valide !";
            return errorMsg;
        } 

        if(!((isNaN(eleve.date_naissance) && (!isNaN(Date.parse(eleve.date_naissance)))))){
            errorMsg="Veuillez entrer une date de naissance valide !";
            return errorMsg;
        }

        if(eleve.lieu_naissance.length == 0 ){
            errorMsg="Veuillez entrer le lieu de naissance  !";
            return errorMsg;
        }    
        return errorMsg;  
    }
    

    function formDataCheck2(eleve){       
        var errorMsg='';
        return errorMsg;   
    }


    function formDataCheck3(eleve){       
        var errorMsg='';
        if(eleve.nom_pere.length == 0 && eleve.nom_mere.length == 0){
            errorMsg="Veuillez saisir au moins le nom d'un parent !";
            return errorMsg;
        }
        if( eleve.email_pere.length == 0 &&  eleve.email_mere.length == 0){
            errorMsg="Veuillez saisir au moins l'adresse mail d'un parent !";
            return errorMsg;
        }

        if(eleve.email_pere.length != 0 && !eleve.email_pere.includes('@')){
            errorMsg="Veuillez entrer une adresse mail valide pour le pere !";
            return errorMsg;
        }  

        if(eleve.email_mere.length != 0 && !eleve.email_mere.includes('@')){
            errorMsg="Veuillez entrer une adresse mail valide pour la mere !";
            return errorMsg;
        }  
       
        return errorMsg;  
    }


    function dropDownSexeChangeHandler(e){
        document.getElementById('sexe').value = e.value;
    }

    function dropDownClasseChangeHandler(e){
      document.getElementById('classe').value = e.value;
    }

    function dropDownFiliereChangeHandler(e){
        document.getElementById('filiere').value = e.value;  
    }

    function dropDownRdoublChangeHandler(e){
        document.getElementById('redouble').value = e.value;  
    }

    
   
    /************************************ JSX Code ************************************/

    return (
        <div className={'card '+ classes.formContainer}>
            <div className={getCurrentHeaderTheme()}>
                <div className={classes.formImageContainer}>
                    <img alt='add student' className={classes.formHeaderImg} src='images/AddStudent.png'/>
                </div>
                {(props.formMode == 'creation') ?                
                    <div className={classes.formMainTitle} >
                            ENREGISTREMENT D'UN NOUVEL ELEVE
                    </div>
                : (props.formMode == 'modif') ?
                    <div className={classes.formMainTitle} >
                        MODIFICATION DES INFORMATIONS D'UN ELEVE
                    </div>
                :
                    <div className={classes.formMainTitle} >
                       CONSULTATION DES INFORMATIONS SUR UN ELEVE
                    </div>
                
                }
                
            </div>

            {(errors.length) ?
                    <div className={classes.formErrorMsg} style={{marginTop:'3vh'}}> {getUploadError()}</div>
                    :
                    null
                }           
                <div id='errMsgPlaceHolder'/> 
            {(etape == 1) &&
                <div className={classes.etape}>
                    <div className={classes.inputRowLeft} style={{color:'rgb(6, 146, 18)', fontFamily:'Roboto, sans-serif', fontWeight:570, fontSize:'1.27vw', borderBottomStyle:'solid', borderBottomColor:'rgb(6, 146, 18)', borderBottomWidth:1.97, marginBottom:'3vh'}}> 
                        Etape 1: Saisi des informations personnelles de l'eleve
                        {(props.formMode=='consult')&&
                            <div style={{position:'absolute', right:0, top:'11.3vh' }}>
                                <CustomButton
                                    btnText='Quitter' 
                                    buttonStyle={getGridButtonStyle()}
                                    btnTextStyle = {classes.btnTextStyle}
                                    btnClickHandler={props.cancelHandler}
                                />
                            </div>
                        }
                    </div>
                    <div className={classes.inputRow}>
                        <div className={classes.groupInfo} >
                            <div className={classes.inputRowLeft}> 
                                <input id="matricule" type="hidden"  defaultValue={currentUiContext.formInputs[11]}/>
                                <div className={classes.inputRowLabel} style={{fontWeight:570}}>
                                    Nom:  
                                </div>
                                    
                                <div> 
                                    <input id="nom" type="text" className={classes.inputRowControl + ' formInput'}  defaultValue={currentUiContext.formInputs[0]} style={{marginLeft:'-2vw'}}/>
                                </div>
                            </div>

                            <div className={classes.inputRowLeft}> 
                                <div className={classes.inputRowLabel} style={{fontWeight:570}}>
                                    Prenom(s):  
                                </div>
                                    
                                <div> 
                                    <input id="prenom" type="text" className={classes.inputRowControl + ' formInput'}  defaultValue={currentUiContext.formInputs[1]} style={{marginLeft:'-2vw'}}/>
                                </div>
                            </div>
                    
                            <div className={classes.inputRowLeft}> 
                                <div className={classes.inputRowLabel} style={{fontWeight:570}}>
                                    Date de Naissance :  
                                </div>
                                    
                                <div> 
                                    <input id="date_naissance" type="text" className={classes.inputRowControl + ' formInput medium' }  defaultValue={currentUiContext.formInputs[2]} style={{marginLeft:'-2vw'}}/>
                                </div>
                            </div>

                            <div className={classes.inputRowLeft}> 
                                <div className={classes.inputRowLabel} style={{fontWeight:570}}>
                                    Lieu de Naissance :  
                                </div>
                                    
                                <div> 
                                    <input id="lieu_naissance" type="text" className={classes.inputRowControl + ' formInput'}  defaultValue={currentUiContext.formInputs[3]} style={{marginLeft:'-2vw'}}/>
                                </div>
                            </div>
                            <div className={classes.inputRowLeft}> 
                                <div className={classes.inputRowLabel} style={{fontWeight:570}}>
                                    Sexe :  
                                </div>                    
                                <div style={{marginBottom:'1.3vh', marginLeft:'-2vw'}}> 
                                    <Select
                                        options={optSexe}
                                        className={classes.selectStyle +' slctClasseStat'}
                                        classNamePrefix="select"
                                        defaultValue = {optSexe[0]}
                                        styles={selectMediumStyles}
                                        onChange={dropDownSexeChangeHandler} 
                                    />
                                    <input id="sexe" type="hidden"  defaultValue={optSexe[0].value}/>
                                </div>
                            </div>
                        </div>

                        <div className={classes.inputRowRight} style={{paddingRight:'1vw'}}> 
                            {(filesContent.length==0) ? 
                                <div className={classes.etabLogo}>
                                    <div  className={classes.logoImg}>Photo 4X4</div>
                                    <CustomButton
                                        btnText='Choisir photo' 
                                        buttonStyle={getSmallButtonStyle()}
                                        btnTextStyle = {classes.btnSmallTextStyle}
                                        btnClickHandler = {() => {getFormData1(); setFormData1(); openFileSelector()}}
                                    />
                                </div>  
                                    :
                                <div className={classes.etabLogo}>
                                    <img alt={filesContent[0].name} className={classes.logoImg} src={filesContent[0].content}/>
                                    <div className={classes.photoFileName}>{filesContent[0].name}</div>
                                    <CustomButton
                                        btnText='Choisir photo' 
                                        buttonStyle={getSmallButtonStyle()}
                                        btnTextStyle = {classes.btnSmallTextStyle}
                                        btnClickHandler = {() => {getFormData1(); setFormData1(); openFileSelector();}}
                                    />
                                     <input id="photo_url" type="hidden"  defaultValue=''/>
                                </div>
                            }              
                        </div>                       

                    </div>
                    {(props.formMode != 'consult')&&
                        <div className={classes.inputRowRight}>
                            <CustomButton
                                btnText='Annuler' 
                                buttonStyle={getGridButtonStyle()}
                                btnTextStyle = {classes.btnTextStyle}
                                btnClickHandler={props.cancelHandler}
                            />

                            <CustomButton
                                btnText='Etape 2 >' 
                                buttonStyle={getGridButtonStyle()}
                                btnTextStyle = {classes.btnTextStyle}
                                btnClickHandler={gotoStep2Handler}
                            />
                        </div>
                    }                    
                </div>
            }

            {(etape == 2)&&
                <div className={classes.etape}>
                    <div className={classes.inputRowLeft} style={{color:'rgb(9, 103, 211)', fontFamily:'Roboto, sans-serif', fontWeight:570, fontSize:'1.27vw', borderBottomStyle:'solid', borderBottomColor:'rgb(9, 103, 211)', borderBottomWidth:1.97, marginBottom:'3vh'}}> 
                        Etape 2: Saisi des informations scolaires de l'eleve
                        {(props.formMode=='consult')&&
                            <div style={{position:'absolute', right:0, top:'11.3vh' }}>
                                <CustomButton
                                    btnText='Quitter' 
                                    buttonStyle={getGridButtonStyle()}
                                    btnTextStyle = {classes.btnTextStyle}
                                    btnClickHandler={props.cancelHandler}
                                />
                            </div>
                        }
                    </div>
                    <div className={classes.groupInfo} style={{marginBottom:'3.7vh'}}>
                        <div className={classes.inputRowLeft}> 
                            <div style={{width:'19vw', fontWeight:570}}>
                                Etabablissement de provenance :  
                            </div>
                                
                            <div> 
                                <input id="origine" type="text" className={classes.inputRowControl + ' formInput'}  defaultValue={currentUiContext.formInputs[4]} style={{marginLeft:'-2vw'}}/>
                            </div>
                        </div>
                    
                        <div className={classes.inputRowLeft}> 
                            <div className={classes.inputRowLabel} style={{fontWeight:570}}>
                                Classe :  
                            </div>                    
                            <div style={{marginBottom:'1.3vh', marginLeft:'-2vw'}}>  
                                <Select
                                    options={optClasse}
                                    className={classes.selectStyle +' slctClasseStat'}
                                    classNamePrefix="select"
                                    defaultValue = {optClasse[0]}
                                    styles={selectSmallStyles}
                                    onChange={dropDownClasseChangeHandler} 
                                />
                                 <input id="classe" type="hidden"  defaultValue={optClasse[0].value}/>
                            </div>
                        </div>

                        <div className={classes.inputRowLeft}> 
                            <div className={classes.inputRowLabel} style={{fontWeight:570}}>
                                Filiere :  
                            </div>                    
                            <div style={{marginBottom:'1.3vh', marginLeft:'-2vw'}}>  
                                <Select
                                    options={optFiliere}
                                    className={classes.selectStyle +' slctClasseStat'}
                                    classNamePrefix="select"
                                    defaultValue = {optFiliere[0]}
                                    styles={selectMediumStyles}
                                    onChange={dropDownFiliereChangeHandler} 
                                />
                                <input id="filiere" type="hidden"  defaultValue={optFiliere[0].value}/>
                            </div>
                        </div>

                        <div className={classes.inputRowLeft}> 
                            <div className={classes.inputRowLabel} style={{fontWeight:570}}>
                                Redoublant :  
                            </div>                    
                            <div style={{marginBottom:'1.3vh', marginLeft:'-2vw'}}>  
                                <Select
                                    options={optOk}
                                    className={classes.selectStyle +' slctClasseStat'}
                                    classNamePrefix="select"
                                    defaultValue = {optOk[0]}
                                    styles={selectSmallStyles}
                                    onChange={dropDownRdoublChangeHandler} 
                                />
                                <input id="redouble" type="hidden"  defaultValue={optOk[0].value}/>
                            </div>
                        </div>
                       
                    </div>
                    {(props.formMode != 'consult') &&
                        <div className={classes.inputRowRight}>
                            <CustomButton
                                btnText='< Etape 2 ' 
                                buttonStyle={getGridButtonStyle()}
                                btnTextStyle = {classes.btnTextStyle}
                                btnClickHandler={backToStep1Handler}
                            />
                            <CustomButton
                                btnText='Etape 3 >' 
                                buttonStyle={getGridButtonStyle()}
                                btnTextStyle = {classes.btnTextStyle}
                                btnClickHandler={gotoStep3Handler}
                            />
                        </div>
                    }
                </div>
            }

            {(etape == 3) &&
                <div className={classes.etape}>
                    <div className={classes.inputRowLeft} style={{color:'rgb(185, 131, 14)', fontFamily:'Roboto, sans-serif', fontWeight:570, fontSize:'1.27vw', borderBottomStyle:'solid', borderBottomColor:'rgb(185, 131, 14)', borderBottomWidth:1.97, marginBottom:'3vh'}}> 
                        Etape 1: Saisi des informations des parents de l'eleve
                        {(props.formMode=='consult')&&
                            <div style={{position:'absolute', right:0, top:'11.3vh' }}>
                                <CustomButton
                                    btnText='Quitter' 
                                    buttonStyle={getGridButtonStyle()}
                                    btnTextStyle = {classes.btnTextStyle}
                                    btnClickHandler={props.cancelHandler}
                                />
                            </div>
                        }
                    </div>
                    <div className={classes.groupInfo}>
                        <div className={classes.inputRowLeft}> 
                            <div className={classes.inputRowLabel} style={{fontWeight:570}}>
                                Nom du Pere:  
                            </div>
                                
                            <div> 
                                <input id="nom_pere" enable={(props.formMode != 'consult')} type="text" className={classes.inputRowControl + ' formInput'}  defaultValue={currentUiContext.formInputs[5]} style={{marginLeft:'-2vw'}}/>
                            </div>
                        </div>

                        <div className={classes.inputRowLeft}> 
                            <div className={classes.inputRowLabel} style={{fontWeight:570}}>
                                Email du Pere:  
                            </div>
                                
                            <div> 
                                <input id="email_pere" disable={(props.formMode == 'consult')} type="text" className={classes.inputRowControl + ' formInput'}  defaultValue={currentUiContext.formInputs[6]} style={{marginLeft:'-2vw'}}/>
                            </div>
                        </div>
                        <div className={classes.inputRowLeft}> 
                            <div className={classes.inputRowLabel} style={{fontWeight:570}}>
                                Tel. du Pere :  
                            </div>
                                
                            <div> 
                                <input id="tel_pere" disable={(props.formMode == 'consult')} type="text" className={classes.inputRowControl + ' formInput medium'}   defaultValue={currentUiContext.formInputs[7]} style={{marginLeft:'-2vw'}}/>
                            </div>
                        </div>
                        
                        <div className={classes.inputRowLeft} > 
                            <div className={classes.inputRowLabel} style={{fontWeight:570}}>
                                Nom de la mere:  
                            </div>
                                
                            <div> 
                                <input id="nom_mere" disable={(props.formMode == 'consult')} type="text" className={classes.inputRowControl + ' formInput'}  defaultValue={currentUiContext.formInputs[8]} style={{marginLeft:'-2vw'}}/>
                            </div>
                        </div>

                        <div className={classes.inputRowLeft}> 
                            <div className={classes.inputRowLabel} style={{fontWeight:570}}>
                                Email de la Mere:  
                            </div>
                                
                            <div> 
                                <input id="email_mere" disable={(props.formMode == 'consult')} type="text" className={classes.inputRowControl + ' formInput'}  defaultValue={currentUiContext.formInputs[9]} style={{marginLeft:'-2vw'}}/>
                            </div>
                        </div>
                        <div className={classes.inputRowLeft}> 
                            <div className={classes.inputRowLabel} style={{fontWeight:570}}>
                                Tel. de la Mere :  
                            </div>
                                
                            <div> 
                                <input id="tel_mere" disable={(props.formMode == 'consult')} type="text" className={classes.inputRowControl + ' formInput medium'}   defaultValue={currentUiContext.formInputs[10]} style={{marginLeft:'-2vw'}}/>
                            </div>
                        </div>                        
                    </div>
                    {(props.formMode != 'consult') &&
                        <div className={classes.inputRowRight} style={{marginTop:'-3.7vh'}}>
                            <CustomButton
                                btnText='< Etape2' 
                                buttonStyle={getGridButtonStyle()}
                                btnTextStyle = {classes.btnTextStyle}
                                btnClickHandler={backToStep2Handler}
                            />
                            <CustomButton
                                btnText='Terminer >' 
                                buttonStyle={getGridButtonStyle()}
                                btnTextStyle = {classes.btnTextStyle}
                                btnClickHandler={finishAllSteps}
                            />
                        </div>                        
                    }                    
                    
                </div>
            }
            
            <div className={classes.formButtonRow}>
                <CustomButton
                    btnText='Information Personnelles'
                    hasIconImg= {true}
                    imgSrc='images/etape1.png'
                    imgStyle = {classes.frmBtnImgStyle1}   
                    buttonStyle={classes.buttonEtape1}
                    btnTextStyle = {classes.btnEtapeTextStyle}
                    btnClickHandler={(etape1InActiv)? null: ()=>setEtape(1)}
                    disable={etape1InActiv}
                />
                
                <CustomButton
                    btnText='Informations Scolaires'
                    hasIconImg= {true}
                    imgSrc='images/etape2.png'
                    imgStyle = {classes.frmBtnImgStyle2} 
                    buttonStyle={classes.buttonEtape2}
                    btnTextStyle = {classes.btnEtapeTextStyle}
                    btnClickHandler={(etape2InActiv) ? null: ()=>setEtape(2)}
                    disable={etape2InActiv}
                />

                <CustomButton
                    btnText='Informations des Parents'
                    hasIconImg= {true}
                    imgSrc='images/etape3.png'
                    imgStyle = {classes.frmBtnImgStyle1} 
                    buttonStyle={classes.buttonEtape3}
                    btnTextStyle = {classes.btnEtapeTextStyle}
                    btnClickHandler={(etape3InActiv) ? null:()=>setEtape(3)}
                    disable={etape3InActiv} 
                />
                
            </div>

            

        </div>
       
     );
 }
 export default AddStudent;
 