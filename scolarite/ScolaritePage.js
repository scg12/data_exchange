import React from "react";
import Select from 'react-select';
import { useTranslation } from "react-i18next";
import MenuItemList from '../../layout/menuItemList/MenuItemList';
import classes from './ScolaritePage.module.css';
import M_classes from './M_ScolaritePage.module.css';
import MenuItem from '../../layout/menuItem/MenuItem';
import M from 'materialize-css';

import { useState,useContext,useEffect } from "react";
import UiContext from '../../../../store/UiContext'

import Enregistrement from "./subPages/Enregistrement";
import ListeDesEleves from "./subPages/ListeDesEleves";
import CarteScolaire from "./subPages/CarteScolaire";
import ChangementClasse from "./subPages/ChangementClasse";
import AdmissionClasseSup from "./subPages/AdmissionClasseSup";
import EmploiDeTemps from "./subPages/EmploiDeTemps";
import CahierDeTexte from "./subPages/CahierDeTexte";
import ConseilClasse from "./subPages/ConseilClasse";
import FicheProgession from "./subPages/FicheProgession";
import ProgramClasse from "./subPages/ProgramClasse";
import Appel from "./subPages/Appel";
import ConseilDiscipline from "./subPages/ConseilDiscipline";
import Studentprofile from "./subPages/Studentprofile";
import BilletEntree from "./subPages/BilletEntree";
import BilletSortie from "./subPages/BilletSortie";
import NewEvaluation from "./subPages/NewEvaluation";
import SaveNotes from "./subPages/SaveNotes";
import PrintStudentReport from "./subPages/PrintStudentReport";
import LookStudentReport from "./subPages/LookStudentReport";
import NewOfficialExam from "./subPages/NewOfficialExam";
import SaveExamNotes from "./subPages/SaveExamNotes";
import ListAdmis from "./subPages/ListAdmis"

import ProgressBar from 'react-bootstrap/ProgressBar';
import AppContext from "../../../../store/AppContext";
import axiosInstance from "../../../../axios";
import FormLayout from "../../layout/formLayout/FormLayout"
import {isMobile} from 'react-device-detect';


function ScolaritePage() {
    
  const { t, i18n } = useTranslation();
  const currentUiContext = useContext(UiContext);
  const currentAppContext = useContext(AppContext);
  
  //Cette constante sera lu lors de la configuration de l'utilisateur.
  const selectedTheme = currentUiContext.theme;
  const [curentMenuItemId,setMenuItemId]=useState(0);
  let listMatieres = [];
  let matieres = [];
  let classess = [];
  let indexClasse = -1;
  let emploiDeTemps = [];
  let listProfs = [];
  let tab_jours = [];
  let tab_periodes = [];
  let tab_creneau_pause = [];
  let tab_valeur_horaire = [];
  function showSideMenu(e) {
    const itemId = e.currentTarget.id
    setMenuItemId(itemId);
    const menus = document.querySelectorAll('.side-menu');
    M.Sidenav.init(menus, {edge: 'right'});
  }

  function showSideMenu2(e) {
    const itemId = e.currentTarget.id
    setMenuItemId(itemId);
    const menus = document.querySelectorAll('.side-menu');
    M.Sidenav.init(menus, {edge: 'right'});

    axiosInstance.post(`get-current-emploi-de-temps/`, {
              id_sousetab: currentAppContext.currentEtab
          }).then((res)=>{
              console.log(res.data);
          res.data.matieres.map((m)=>{matieres.push(m)});
          res.data.classes.map((c)=>{classess.push(c)});
          res.data.ListMatieres.map((lm)=>{listMatieres.push(lm)});
          res.data.emploiDeTemps.map((em)=>{emploiDeTemps.push(em)});
          res.data.listProfs.map((lp)=>{listProfs.push(lp)});
          res.data.TAB_JOURS.map((j)=>{tab_jours.push(j)});
          res.data.TAB_PERIODES.map((p)=>{tab_periodes.push(p)});
          res.data.TAB_CRENEAU_PAUSE.map((p)=>{tab_creneau_pause.push(p)});
          res.data.TAB_VALEUR_HORAIRE.map((vh)=>{tab_valeur_horaire.push(vh)});
          // Affichage initial des matières pr la première classe selectionnée
          //  if(res.data.classes.length>0){
          //     currentClasseId = res.data.classes[0].id;
          //     indexClasse = matieres.findIndex(m=>m.id==currentClasseId);
          //     console.log("INDEX: ",indexClasse);
      
          //  }
          currentUiContext.setClasseEmploiTemps(classess);
           currentUiContext.setListMatieres(listMatieres);
           currentUiContext.setListProfs(listProfs);
           currentUiContext.setIndexClasse(indexClasse);
           currentUiContext.setMatiereSousEtab(matieres);
           currentUiContext.setTAB_JOURS(tab_jours);
           currentUiContext.setTAB_PERIODES(tab_periodes);
           currentUiContext.setTAB_VALEUR_HORAIRE(tab_valeur_horaire);
           currentUiContext.setEmploiDeTemps(emploiDeTemps);
           currentUiContext.setTAB_CRENEAU_PAUSE(tab_creneau_pause);

           if(tab_valeur_horaire.length>0){
            currentUiContext.setIntervalleMaxTranche(tab_valeur_horaire[0]+"_"+tab_valeur_horaire[tab_valeur_horaire.length-1]);
        }
    })      
    
  }

//   useEffect(()=> {
//     console.log("$$$$$$$ ",currentAppContext);
//     axiosInstance.post(`get-current-emploi-de-temps/`, {
//         id_sousetab: currentAppContext.currentEtab
//     }).then((res)=>{
//         console.log(res.data);
//     res.data.matieres.map((m)=>{matieres.push(m)});
//     res.data.ListMatieres.map((lm)=>{listMatieres.push(lm)});
//     res.data.emploiDeTemps.map((em)=>{emploiDeTemps.push(em)});
//     res.data.listProfs.map((lp)=>{listProfs.push(lp)});
//     res.data.TAB_JOURS.map((j)=>{tab_jours.push(j)});
//     res.data.TAB_PERIODES.map((p)=>{tab_periodes.push(p)});
//     res.data.TAB_CRENEAU_PAUSE.map((p)=>{tab_creneau_pause.push(p)});
//     res.data.TAB_VALEUR_HORAIRE.map((vh)=>{tab_valeur_horaire.push(vh)});
//     // Affichage initial des matières pr la première classe selectionnée
//     //  if(res.data.classes.length>0){
//     //     currentClasseId = res.data.classes[0].id;
//     //     indexClasse = matieres.findIndex(m=>m.id==currentClasseId);
//     //     console.log("INDEX: ",indexClasse);

//     //  }
//      currentUiContext.setListMatieres(listMatieres);
//      currentUiContext.setListProfs(listProfs);
//      currentUiContext.setIndexClasse(indexClasse);
//      currentUiContext.setMatiereSousEtab(matieres);
//      currentUiContext.setTAB_JOURS(tab_jours);
//      currentUiContext.setTAB_PERIODES(tab_periodes);
//      currentUiContext.setTAB_CRENEAU_PAUSE(tab_creneau_pause);
//      currentUiContext.setTAB_VALEUR_HORAIRE(tab_valeur_horaire);
//      currentUiContext.setEmploiDeTemps(emploiDeTemps);
    
//     }) 
// },[]);
    /******************* pour ce qui concerne le cahier de texte ******************/
  
 
  function getCurrentContaintTheme()
  { // Choix du theme courant
    if(isMobile){
      switch(selectedTheme){
        case 'Theme1': return M_classes.Theme1_mainContentPosition ;
        case 'Theme2': return M_classes.Theme2_mainContentPosition ;
        case 'Theme3': return M_classes.Theme3_mainContentPosition ;
        default: return M_classes.Theme1_mainContentPosition ;
      }

    } else {
      switch(selectedTheme){
        case 'Theme1': return classes.Theme1_mainContentPosition ;
        case 'Theme2': return classes.Theme2_mainContentPosition ;
        case 'Theme3': return classes.Theme3_mainContentPosition ;
        default: return classes.Theme1_mainContentPosition ;
      }

    }
   
  }

  
  return (

    <div className= {classes.viewContent}>
      <div className= {(isMobile)?  M_classes.pageTitle  : classes.pageTitle}>
        <div className={(isMobile)? M_classes.rowDisplay : classes.rowDisplay}>
          {(isMobile) ? null:< img src="images/scolariteP.png"  className={classes.imageMargin1} alt="my image"/>}
          SCOLARITE
        </div>
      </div>

      <div className= {getCurrentContaintTheme()}>
      {(currentAppContext.enableProfiles["SCOLARITE_A"]=='1') ? 
        <MenuItemList minWtdhStyle={classes.size72Vw}  libelle= 'Enregistrement Et Admissions en Classe Superieure' theme={selectedTheme}>
          {(currentAppContext.enableProfiles["SCOLARITE_A1"]=='1') ?   <MenuItem menuItemId ='1'  imgSource='images/AddStudent.png'        libelle='Enregistrement et Gestion des Effectifs' itemSelected={showSideMenu} ></MenuItem> : null}
          {(currentAppContext.enableProfiles["SCOLARITE_A2"]=='1') ?   <MenuItem menuItemId ='2'  imgSource='images/ListStudent.png'       libelle='Consultation Des Listes Des Eleves' itemSelected={showSideMenu}></MenuItem> : null}
          {(currentAppContext.enableProfiles["SCOLARITE_A3"]=='1') ?   <MenuItem menuItemId ='3'  imgSource='images/ChangemtClass.png'     libelle='Changement De Classe'itemSelected={showSideMenu}></MenuItem> : null}
          {(currentAppContext.enableProfiles["SCOLARITE_A4"]=='1') ?   <MenuItem menuItemId ='4'  imgSource='images/PrintSchoolCard.png'   libelle='Generation De Cartes Scolaires' itemSelected={showSideMenu}></MenuItem> : null}
          {(currentAppContext.enableProfiles["SCOLARITE_A5"]=='1') ?   <MenuItem menuItemId ='5'  imgSource='images/ConseilClasse.png'     libelle='Conseil De Classe' itemSelected={showSideMenu}></MenuItem> : null}
          {(currentAppContext.enableProfiles["SCOLARITE_A6"]=='1') ?   <MenuItem menuItemId ='6'  imgSource='images/ClassSup.png'          libelle='Admission En classe superieure' itemSelected={showSideMenu}></MenuItem> : null}
        </MenuItemList>
        :
        null
      }

      {(currentAppContext.enableProfiles["SCOLARITE_B"]=='1') ?
        <MenuItemList minWtdhStyle={classes.size72Vw}   libelle= 'Emplois de Temps, Cours Et Programmes' theme={selectedTheme}>
          {(currentAppContext.enableProfiles["SCOLARITE_B1"]=='1') ? <MenuItem menuItemId ='7' imgSource='images/Schedule.png'           libelle='Emploi De Temps' itemSelected={showSideMenu2}></MenuItem> : null}
          {(currentAppContext.enableProfiles["SCOLARITE_B2"]=='1') ? <MenuItem menuItemId ='8' imgSource='images/FicheProgession.png'    libelle='Fiche De Progression' itemSelected={showSideMenu}></MenuItem> : null}
          {(currentAppContext.enableProfiles["SCOLARITE_B2"]=='1') ? <MenuItem menuItemId ='9' imgSource='images/ProgramClasse.png'      libelle='Programme des Classes' itemSelected={showSideMenu}></MenuItem> : null}
          {(currentAppContext.enableProfiles["SCOLARITE_B2"]=='1') ? <MenuItem menuItemId ='10' imgSource='images/CahierTexte.png'        libelle='Cahier De Texte' itemSelected={showSideMenu}></MenuItem> : null}
          {/*<MenuItem libelle='Admission en claase2 ' itemSelected={showSideMenu}></MenuItem>*/}
        </MenuItemList>
        :
        null
      }

        
      {(currentAppContext.enableProfiles["SCOLARITE_C"]=='1') ?
        <MenuItemList minWtdhStyle={classes.size72Vw} libelle= 'Discipline Et Assiduite' theme={selectedTheme}>
          {(currentAppContext.enableProfiles["SCOLARITE_C1"]=='1') ? <MenuItem menuItemId ='11'  imgSource='images/Appel.png'        libelle="Faire l'Appel"itemSelected={showSideMenu}></MenuItem> : null}
          {(currentAppContext.enableProfiles["SCOLARITE_C2"]=='1') ? <MenuItem menuItemId ='12'  imgSource='images/ConseilDiscipline.png'  libelle='Conseil De Discipline'itemSelected={showSideMenu}></MenuItem> : null}
          {(currentAppContext.enableProfiles["SCOLARITE_C3"]=='1') ? <MenuItem menuItemId ='13'  imgSource='images/Studentprofile.png'  libelle='Situation Disciplinaire des Eleves'itemSelected={showSideMenu}></MenuItem> : null}
          {(currentAppContext.enableProfiles["SCOLARITE_C4"]=='1') ? <MenuItem menuItemId ='14'  imgSource='images/BilletEntree.png' libelle="Billet D'Entree" itemSelected={showSideMenu}></MenuItem> : null}
          {(currentAppContext.enableProfiles["SCOLARITE_C5"]=='1') ? <MenuItem menuItemId ='15'  imgSource='images/BilletSortie.png' libelle='Billet De Sortie' itemSelected={showSideMenu}></MenuItem> : null}
        </MenuItemList>
        :
        null
      }

      {(currentAppContext.enableProfiles["SCOLARITE_D"]=='1') ?
        <MenuItemList minWtdhStyle={classes.size72Vw} libelle= 'Evaluations De Classe Et Notes' theme={selectedTheme}>
          {(currentAppContext.enableProfiles["SCOLARITE_D1"]=='1') ? <MenuItem menuItemId ='16' imgSource='images/NewEvaluation.png' libelle='Nouvelle Evaluation' itemSelected={showSideMenu}></MenuItem> : null}
          {(currentAppContext.enableProfiles["SCOLARITE_D2"]=='1') ? <MenuItem menuItemId ='17' imgSource='images/SaveNotes.png'     libelle='Notes Aux Evaluatons'itemSelected={showSideMenu}></MenuItem> : null}
          {(currentAppContext.enableProfiles["SCOLARITE_D3"]=='1') ? <MenuItem menuItemId ='18' imgSource='images/PrintStudentReport.png'  libelle='Generation De Bulletin de Notes'itemSelected={showSideMenu}></MenuItem> : null}
          {(currentAppContext.enableProfiles["SCOLARITE_D4"]=='1') ? <MenuItem menuItemId ='19' imgSource='images/LookStudentReport.png'  libelle='Consultation Bulletin de Notes' itemSelected={showSideMenu}></MenuItem> : null}
          {/*<MenuItem imgSource='images/BilletSortie.png'  libelle='Admission en claase ' itemSelected={showSideMenu}></MenuItem>*/}
        </MenuItemList>
        :
        null
      }

      {(currentAppContext.enableProfiles["SCOLARITE_E"]=='1') ?
        <MenuItemList minWtdhStyle={classes.size72Vw} libelle= 'Examens officiels' theme={selectedTheme}>
          {(currentAppContext.enableProfiles["SCOLARITE_E1"]=='1') ? <MenuItem menuItemId ='20' imgSource='images/NewEvaluation.png' libelle='Nouvel Examen Officiel'itemSelected={showSideMenu}></MenuItem> : null}
          {(currentAppContext.enableProfiles["SCOLARITE_E2"]=='1') ? <MenuItem menuItemId ='21' imgSource='images/SaveNotes.png'  libelle='Saisi Des Resultats Aux Examens'itemSelected={showSideMenu}></MenuItem>: null}
          {(currentAppContext.enableProfiles["SCOLARITE_E3"]=='1') ? <MenuItem menuItemId ='22' imgSource='images/ListAdmis.png'  libelle='Liste Des Admis Aux Examens'itemSelected={showSideMenu}></MenuItem> : null}
          {/*<MenuItem imgSource='images/BilletSortie.png'  libelle='Changement de classe' itemSelected={showSideMenu}></MenuItem>
          <MenuItem imgSource='images/BilletSortie.png'  libelle='Admission en claase ' itemSelected={showSideMenu}></MenuItem>*/}
        </MenuItemList>
        :
        null
      }
        

     
       

        

                
       {/* <MenuItemList libelle= 'Enregistrement & Admissions' theme={selectedTheme}>
          <MenuItem libelle='Inscription'itemSelected={showSideMenu}></MenuItem>
          <MenuItem libelle='Liste des Eleves'itemSelected={showSideMenu}></MenuItem>
          <MenuItem libelle='Carte Scolaire'itemSelected={showSideMenu}></MenuItem>
          <MenuItem libelle='Changement de classe' itemSelected={showSideMenu}></MenuItem>
          <MenuItem libelle='Admission en claase ' itemSelected={showSideMenu}></MenuItem>
        </MenuItemList>


        <MenuItemList libelle= 'Enregistrement & Admissions' theme={selectedTheme}>
          <MenuItem libelle='Inscription'itemSelected={showSideMenu}></MenuItem>
          <MenuItem libelle='Liste des Eleves'itemSelected={showSideMenu}></MenuItem>
          <MenuItem libelle='Carte Scolaire'itemSelected={showSideMenu}></MenuItem>
          <MenuItem libelle='Changement de classe' itemSelected={showSideMenu}></MenuItem>
          <MenuItem libelle='Admission en claase ' itemSelected={showSideMenu}></MenuItem>
        </MenuItemList>

        <MenuItemList libelle= 'Enregistrement & Admissions' theme={selectedTheme}>
          <MenuItem libelle='Inscription'itemSelected={showSideMenu}></MenuItem>
          <MenuItem libelle='Liste des Eleves'itemSelected={showSideMenu}></MenuItem>
          <MenuItem libelle='Carte Scolaire'itemSelected={showSideMenu}></MenuItem>
          <MenuItem libelle='Changement de classe' itemSelected={showSideMenu}></MenuItem>
          <MenuItem libelle='Admission en claase ' itemSelected={showSideMenu}></MenuItem>
        </MenuItemList> */}
      </div>
                  
      <div id="side-menu" class="sidenav side-menu">
        <FormLayout formCode={curentMenuItemId}>
          {curentMenuItemId==1 && <ListeDesEleves formMode='ajout'/>      } 
          {curentMenuItemId==2 && <ListeDesEleves formMode='liste'/>      }
          {curentMenuItemId==3 && <ChangementClasse/>    }
          {curentMenuItemId==4 && <CarteScolaire/>       }
          {curentMenuItemId==5 && <ConseilClasse/>       } 
          {curentMenuItemId==6 && <AdmissionClasseSup/>  }
          {curentMenuItemId==7 && <EmploiDeTemps/>       }
          {curentMenuItemId==8 && <FicheProgession/>     }
          {curentMenuItemId==9 && <ProgramClasse/>       } 
          {curentMenuItemId==10 && <CahierDeTexte/>      }
          {curentMenuItemId==11 && <Appel formMode='appel'/>              }
          {curentMenuItemId==12 && <ConseilDiscipline/>  }
          {curentMenuItemId==13 && <Studentprofile/>     }
          {curentMenuItemId==14 && <BilletEntree/>       }
          {curentMenuItemId==15 && <BilletSortie/>       }
          {curentMenuItemId==16 && <NewEvaluation/>      }
          {curentMenuItemId==17 && <SaveNotes/>          }
          {curentMenuItemId==18 && <PrintStudentReport/> }
          {curentMenuItemId==19 && <LookStudentReport/>  }
          {curentMenuItemId==20 && <NewOfficialExam/>    }
          {curentMenuItemId==21 && <SaveExamNotes/>      }
          {curentMenuItemId==22 && <ListAdmis/>          }
          {/*curentMenuItemId==8 && <EmploiDeTemps/>    */  }
        </FormLayout>     
      </div>
    </div>
  );
}

export default ScolaritePage;