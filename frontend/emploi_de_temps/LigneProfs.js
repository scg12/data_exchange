import React from 'react';
import classes from './EmploiT.module.css';
import { useContext } from "react";
import UiContext from '../../../store/UiContext';

import { useTranslation } from "react-i18next";
import '../../../translation/i18n';

import ProfDiv from './profDiv/ProfDiv';
import {TAB_ENSEIGNANTS} from '../../../store/SharedData/DndConst'


 
function LigneProfs(props) {
  
    const currentUiContext = useContext(UiContext);

     //Cette constante sera lu lors de la configuration de l'utilisateur.
    const selectedTheme = currentUiContext.theme;
    const { t, i18n } = useTranslation();
    
    const changeLanguage = (event) => {
        i18n.changeLanguage(event.target.id);
    };

    
    function getCurrentTheme()
    {  // Choix du theme courant
       switch(selectedTheme){
            case 'Theme1': return classes.Theme1_footer;
            case 'Theme2': return classes.Theme2_footer;
            case 'Theme3': return classes.Theme3_footer;
            default: return classes.Theme1_footer;
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


   return (
        <div id='profList' className={classes.profList}>
            {currentUiContext.listProfs.map((prof) => {
                return (
                    <ProfDiv
                        id={"prof_"+prof.id}
                        dragDivClassName= {null}
                        profImgStyle = {null}
                        profNameStyle = {null}
                        title = ''
                        imgSrc=""
                        imgClass={classes.imgStyle}
                    />
                );
            })}           
        </div>      
    );
}

// export default LigneMatieres;
export default LigneProfs;