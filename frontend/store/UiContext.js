import React from 'react';
import { createContext, useState } from 'react';

const UiContext = createContext({
    logo :'',
    theme : 'Theme1',
    selectedTab : 'menuLi0',
    firstLoad : true,
    modalOpen : false,
    formInputs : {},
   
    // Emploi de temps Gestion des Matieres
    CURRENT_DROPPED_MATIERE_LIST:{},
    // Emploi de temps Gestion des profs
    CURRENT_DROPPED_PROFS_LIST:{},
    CURRENT_PROFS_LIST:{},
    //Gestion des sections au niveau de la config
    sectionSelected :{},
    // Pour l'emploi du temps
    listMatieres : {},
    listProfs : {},
    TAB_JOURS : {},
    TAB_VALEUR_HORAIRE : {},
    TAB_CRENEAU_PAUSE : {},
    TAB_PERIODES : {},
    matieresSousEtab : {},
    emploiDeTemps : {},
    classeEmploiTemps : {},
    indexClasse :{},
    intervalleMaxTranche :{},
    nbRefreshEmpoiTemps:{},
    currentIdClasseEmploiTemps :{},
    CURRENT_MATIERE_LIST:{},


          
    
    updateTheme: (newTheme)=> {},
    updateLogo : (newLogo)=> {},
    updateTab : (newTab) => {},
    updateFirstLoad : (boolVal) => {},
    setModalOpen : (boolVal) => {},
    setFormInputs : (formInputsTable) => {}, 

    // Emploi de temps Gestion des Matieres
    addMatiereToDroppedMatiereList : (newMatiere,index) => {},
    removeMatiereFromDroppedMatiereList : (index) => {}, 
    setListMatieres : (liste) => {},
    // Emploi de temps Gestion des profs
    addProfToDroppedProfList: (newProf,index)=> {}, 
    removeProfFromDroppedProfList: (index)=> {},

    //Gestion des sections au niveau de la config
    setSectionselected :(sectionTable) => {}
    
});

export function UiContextProvider(props)
{    
    const [ChangedTheme, setTheme]= useState('Theme1');
    const [ChangedLogo, setLogo] = useState();
    const [ChangedTab, setTab] = useState('menuLi0');
    const [ChangedFirstLoad, setFirstLoad] = useState(true);
    const [modalOpen, setModalOpen] = useState(false);
    const [inputTable, setInputTable] = useState([]);
    const [matiereBoard, setMatiereBoard] = useState([]);
    const [sectionSelected, setSectionSelected] = useState([0,0,0,0,0]);
    const [indexClasse, setIndexClasse] = useState();
    const [intervalleMaxTranche, setIntervalleMaxTranche] = useState("");
    const [nbRefreshEmpoiTemps, setNbRefreshEmpoiTemps] = useState(0);
    const [currentIdClasseEmploiTemps, setCurrentIdClasseEmploiTemps] = useState();

    // Emploi de temps Gestion des Matieres
    const [CURRENT_DROPPED_MATIERE_LIST, setDroppedMatiereList] = useState([]);
    // Emploi de temps Gestion des profs
    const [CURRENT_DROPPED_PROFS_LIST, setDroppedProfList] = useState([]);
    const [CURRENT_PROFS_LIST, setCurrentProfList] = useState([]);
    const [listMatieres, setListMatieres] = useState([]);
    const [listProfs, setListProfs] = useState([]);
    const [TAB_JOURS, setTAB_JOURS] = useState([]);
    const [CURRENT_MATIERE_LIST, setCURRENT_MATIERE_LIST] = useState([]);
    const [emploiDeTemps, setEmploiDeTemps] = useState([]);
    const [classeEmploiTemps, setClasseEmploiTemps] = useState([]);
    const [TAB_VALEUR_HORAIRE, setTAB_VALEUR_HORAIRE] = useState([]);
    const [TAB_CRENEAU_PAUSE, setTAB_CRENEAU_PAUSE] = useState([]);
    const [TAB_PERIODES, setTAB_PERIODES] = useState([]);
    const [matiereSousEtab, setMatiereSousEtab] = useState([]);
    
    


    function updateThemeHandler(newTheme){
        setTheme(newTheme) 
    }

    function updateLogoHandler(newLogo){
        setLogo(newLogo)
    }
    
    function updateTabHandler(newTab){
        setTab(newTab)
    }

    function updateFirstLoadHandler(boolVal){
        setFirstLoad(boolVal)
    }

    function updateModalHandler(boolVal){
        setModalOpen(boolVal)
    }

    function updateInputsTableHandler(inputTable) {
        setInputTable(inputTable)
    }


     // Emploi de temps Gestion des Matieres
    function addMatiereToDroppedMatiereListHandler(newMatiere, index){
        // -2 on update toute la liste newMAtiere represente dans ce cas une liste
        if(index==-2) setDroppedMatiereList(newMatiere);
        else
            if(index!=-1){
                var droppedMatiereTab = [...CURRENT_DROPPED_MATIERE_LIST];
                droppedMatiereTab.splice(index,1);
                droppedMatiereTab.splice(index,0,newMatiere);
                setDroppedMatiereList(droppedMatiereTab);
            }
            else{
                setDroppedMatiereList(newMatiere);
                //setDroppedMatiereList((CURRENT_DROPPED_MATIERE_LIST)=>[...CURRENT_DROPPED_MATIERE_LIST, newMatiere]);
            // console.log(CURRENT_DROPPED_MATIERE_LIST);
            }
    }
    function setListMatieresHandler(listMatieres){
        var liste = [...listMatieres];
        setListMatieres(liste);
    }
    function setListProfsHandler(listProfs){
        var liste = [...listProfs];
        setListProfs(liste);
    }
    function setClasseEmploiTempsHandler(items){
        setClasseEmploiTemps([...items]);
    }
    function setTAB_JOURSHandler(liste){
        setTAB_JOURS(liste);
    }
    function setCURRENT_MATIERE_LISTHandler(liste){
        setCURRENT_MATIERE_LIST(liste);
    }
    function setEmploiDeTempsHandler(liste){
        setEmploiDeTemps(liste);
    }
    function setTAB_VALEUR_HORAIREHandler(liste){
        setTAB_VALEUR_HORAIRE(liste);
    }
    function setTAB_CRENEAU_PAUSEHandler(liste){
        setTAB_CRENEAU_PAUSE(liste);
    }
    function setTAB_PERIODESHandler(liste){
        setTAB_PERIODES(liste);
    }
    function setMatiereSousEtabHandler(matieres){
        var liste = [...matieres];
        setMatiereSousEtab(liste);
    }

    function removeMatiereFromDroppedMatiereListHandler(index){
        var droppedMatiereTab = [...CURRENT_DROPPED_MATIERE_LIST];
        droppedMatiereTab.splice(index,1);        
        setDroppedMatiereList(droppedMatiereTab);       
    }

    // Emploi de temps Gestion des profs
    function addProfToDroppedProfListHandler(newProf, index=-1){
        if(index!=-1){
            var droppedProfTab = [...CURRENT_DROPPED_PROFS_LIST];
            droppedProfTab.splice(index,1);
            droppedProfTab.splice(index,0,newProf);
            setDroppedProfList(droppedProfTab);
        }
        else{
            //setDroppedProfList((CURRENT_DROPPED_PROFS_LIST)=>[...CURRENT_DROPPED_PROFS_LIST, newProf]);
            setDroppedProfList(newProf);
        }
    }

    function removeProfFromDroppedProfListHandler(index){
        var droppedProfTab = [...CURRENT_DROPPED_PROFS_LIST];
        droppedProfTab.splice(index,1);       
        setDroppedProfList(droppedProfTab);        
    }

    function setIndexClasseHandler(classe){
        setIndexClasse(classe);
    }
    function setIntervalleMaxTrancheHandler(intervalle){
        setIntervalleMaxTranche(intervalle);
    }
    function setNbRefreshEmpoiTempsHandler(reinit){
        if(reinit==1) setNbRefreshEmpoiTemps(0)
        else
            setNbRefreshEmpoiTemps(nbRefreshEmpoiTemps+1);
    }
    function setCurrentProfListHandler(items){
        setCurrentProfList(items);
    }
    function setCurrentIdClasseEmploiTempsHandler(classe){
        setCurrentIdClasseEmploiTemps(classe);
    }
    
    //Gestion des sections au niveau de la config
    function updateSection(sectionTab){
        setSectionSelected(sectionTab);
    }



    const UI_Ctx = {
        logo : ChangedLogo,
        theme : ChangedTheme,
        selectedTab : ChangedTab,
        firstLoad : ChangedFirstLoad,
        modalOpen : modalOpen,
        formInputs: inputTable,

        CURRENT_DROPPED_MATIERE_LIST:CURRENT_DROPPED_MATIERE_LIST,
        CURRENT_DROPPED_PROFS_LIST:CURRENT_DROPPED_PROFS_LIST,
        CURRENT_PROFS_LIST:CURRENT_PROFS_LIST,
        listMatieres: listMatieres,
        listProfs: listProfs,
        TAB_JOURS: TAB_JOURS,
        CURRENT_MATIERE_LIST: CURRENT_MATIERE_LIST,
        emploiDeTemps: emploiDeTemps,
        classeEmploiTemps: classeEmploiTemps,
        TAB_VALEUR_HORAIRE: TAB_VALEUR_HORAIRE,
        TAB_CRENEAU_PAUSE: TAB_CRENEAU_PAUSE,
        TAB_PERIODES: TAB_PERIODES,
        matiereSousEtab: matiereSousEtab,

        //Gestion des sections au niveau de la config
        sectionSelected : sectionSelected,
        indexClasse : indexClasse,
        intervalleMaxTranche:intervalleMaxTranche,
        nbRefreshEmpoiTemps:nbRefreshEmpoiTemps,
        currentIdClasseEmploiTemps:currentIdClasseEmploiTemps,
       
       

        updateTheme: updateThemeHandler,
        updateLogo : updateLogoHandler,
        updateTab : updateTabHandler,
        updateFirstLoad: updateFirstLoadHandler,
        setModalOpen: updateModalHandler,
        setFormInputs: updateInputsTableHandler, 
        
        // Emploi de temps Gestion des Matieres
        addMatiereToDroppedMatiereList : addMatiereToDroppedMatiereListHandler,
        removeMatiereFromDroppedMatiereList:removeMatiereFromDroppedMatiereListHandler,
        setListMatieres : setListMatieresHandler,
        setClasseEmploiTemps : setClasseEmploiTempsHandler,
        setListProfs : setListProfsHandler,
        setTAB_JOURS : setTAB_JOURSHandler,
        setCURRENT_MATIERE_LIST : setCURRENT_MATIERE_LISTHandler,
        setEmploiDeTemps : setEmploiDeTempsHandler,
        setTAB_VALEUR_HORAIRE : setTAB_VALEUR_HORAIREHandler,
        setTAB_CRENEAU_PAUSE : setTAB_CRENEAU_PAUSEHandler,
        setTAB_PERIODES : setTAB_PERIODESHandler,
        setMatiereSousEtab : setMatiereSousEtabHandler,
        setCurrentProfList : setCurrentProfListHandler,

        
        // Emploi de temps Gestion des profs
        addProfToDroppedProfList : addProfToDroppedProfListHandler,
        removeProfFromDroppedProfList : removeProfFromDroppedProfListHandler,

        //Gestion des sections au niveau de la config
        setSectionselected : updateSection,
        setIndexClasse : setIndexClasseHandler,
        setIntervalleMaxTranche : setIntervalleMaxTrancheHandler,
        setNbRefreshEmpoiTemps: setNbRefreshEmpoiTempsHandler,
        setCurrentIdClasseEmploiTemps:setCurrentIdClasseEmploiTempsHandler,
       
    };

    return (
        <UiContext.Provider value ={UI_Ctx}>
            {props.children}
        </UiContext.Provider>
    );

}

export default UiContext;