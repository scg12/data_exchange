import GrilleEmploiTemps from "../../../emploi_de_temps/GrilleEmploiTemps";
import { createPauses } from "../../../../../store/SharedData/DndFuncts";
import UiContext from '../../../../../store/UiContext';

import React from 'react';
import {useEffect, useState, useContext} from "react";

function EmploiDeTemps(props){
    const currentUiContext = useContext(UiContext);

    const [pausecreated, setPauseCreated] = useState(false);

    useEffect(()=> {
        // if(!pausecreated)
        {
            // createPauses(currentUiContext.TAB_CRENEAU_PAUSE,currentUiContext.TAB_VALEUR_HORAIRE);
            setPauseCreated(true);
        }        
    },[currentUiContext.TAB_VALEUR_HORAIRE]);

    return(
        <GrilleEmploiTemps/>
    );
}

export default EmploiDeTemps;


