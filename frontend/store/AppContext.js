import React from 'react';
import { createContext, useState } from 'react';
import FeaturesCode from '../components/computers-screens/Features/FeaturesCode';

const AppContext = createContext({
    usrLogin :'',
    usrIsLogged : false,
    isDataLoaded : false,
    userProfile : '',
    enableProfiles : {},
    idUser : {},
    idEtabInit : {},
    activatedYear : {},
    currentYear : {},
    currentEtab : {},
    currentCycle : {},
    infoAnnees : {},
    infoSetabs : {},
    infoCycles : {},
    infoNiveaux : {},
    infoClasses : {},

    setUsrLogin: (givenLogin, givenProfile) => {},
    setUsrConnected: ()=> {},
    logOut:() => {},
    setIsDataLoaded:(boolValue) => {},
    setUserProfile : (userProfile) => {},
    setEnableProfiles :(profilecodeMap) => {},
    setCurrentEtab :(givenEtab) => {},
    setCurrentCycle :(givenCycle) => {},
    setCurrentYear :(givenYear) => {},
    setIdUser :(givenIdUser) => {},
    setIdEtabInit :(givenIdEtab) => {},
    setActivatedYear :(givenYear) => {},
    setInfoAnnees :(givenAnnee) => {},
    setInfoSetabs :(infoSetab) => {},
    setInfoCycles :(infoCycle) => {},
    setInfoNiveaux :(infoNiveau) => {},
    setInfoClasses :(infoClasse) => {},
});

export function AppContextProvider(props)
{    
    const [isUsrLogged, setConnected]= useState(false);
    const [usrLogin, setUserLogin]= useState('');
    const [isDataLoaded,setIsDataLoaded] = useState(false);
    const [userProfile, setUserProfile] = useState('');
    const [enableProfiles, setEnableProfiles] = useState(FeaturesCode);
    const [idUser, setIdUser] = useState(0);
    const [currentYear, setCurrentYear] = useState(0);
    const [currentEtab, setCurrentEtab] = useState(0);
    const [currentCycle, setCurrentCycle] = useState(0);
    const [idEtabInit, setIdEtabInit] = useState(0);
    const [activatedYear, setActivatedYear] = useState();
    const [infoAnnees, setInfoAnnees] = useState();
    const [infoSetabs, setInfoSetabs] = useState([]);
    const [infoCycles, setInfoCycles] = useState([]);
    const [infoNiveaux, setInfoNiveaux] = useState([]);
    const [infoClasses, setInfoClasses] = useState([]);
    
    function connectHandler(givenLogin, givenProfile){
        setConnected(true);
        setUserLogin(givenLogin);
        setUserProfile(givenProfile); 
    }

    function connectedUserHandler(givenLogin){
        setUserLogin(givenLogin);  
    }

    function logOutHandler() {
        setConnected(false);
        setUserLogin('');
        setUserProfile('');
    }

    function setIsDataLoadedHandler(boolValue) {
        setIsDataLoaded(boolValue)
    }

    function setUserProfileHandler(userProfile) {
        setUserProfile(userProfile)
    }

    function setEnableProfilesHandler(profilecodeMap) {
        setEnableProfiles(profilecodeMap)
    }
    function setIdUserHandler(givenIdUser) {
        setIdUser(givenIdUser)
    }
    function setCurrentYearHandler(givenYear) {
        setCurrentYear(givenYear)
    }
    function setCurrentEtabHandler(givenEtab) {
        setCurrentEtab(givenEtab)
    }
    function setCurrentCycleHandler(givenCycle) {
        setCurrentCycle(givenCycle)
    }
    function setIdEtabInitHandler(givenIdEtab) {
        setIdEtabInit(givenIdEtab)
    }
    function setActivatedYearHandler(givenActivatedYear) {
        setActivatedYear(givenActivatedYear)
    }
    function setInfoAnneesHandler(givenAnnee) {
        setInfoAnnees(givenAnnee)
    }
    function setInfoSetabsHandler(infoSetab) {
        setInfoSetabs(infoSetab)
    }
    function setInfoCyclesHandler(infoCycle) {
        setInfoCycles(infoCycle)
    }
    function setInfoNiveauxHandler(infoNiveau) {
        setInfoNiveaux(infoNiveau)
    }
    function setInfoClassesHandler(infoClasse) {
        setInfoClasses(infoClasse)
    }

    
    const APP_Ctx = {
        usrLogin : usrLogin,
        usrIsLogged : isUsrLogged,
        isDataLoaded : isDataLoaded,
        userProfile : userProfile,
        enableProfiles: enableProfiles,
        idUser: idUser,
        currentYear: currentYear,
        currentCycle:currentCycle,
        currentEtab:currentEtab,
        idEtabInit: idEtabInit,
        activatedYear: activatedYear,
        infoAnnees: infoAnnees,
        infoSetabs: infoSetabs,
        infoCycles: infoCycles,
        infoNiveaux: infoNiveaux,
        infoClasses: infoClasses,
       
        setUsrConnected: connectHandler,
        setUsrLogin : connectedUserHandler,
        logOut: logOutHandler,
        setIsDataLoaded: setIsDataLoadedHandler,
        setUserProfile : setUserProfileHandler,
        setEnableProfiles: setEnableProfilesHandler,
        setIdUser: setIdUserHandler,
        setCurrentEtab: setCurrentEtabHandler,
        setCurrentCycle: setCurrentCycleHandler,
        setCurrentYear: setCurrentYearHandler,
        setIdEtabInit: setIdEtabInitHandler,
        setActivatedYear: setActivatedYearHandler,
        setInfoAnnees: setInfoAnneesHandler,
        setInfoSetabs: setInfoSetabsHandler,
        setInfoCycles: setInfoCyclesHandler,
        setInfoNiveaux: setInfoNiveauxHandler,
        setInfoClasses: setInfoClassesHandler,
    };


    return (
        <AppContext.Provider value ={APP_Ctx}>
            {props.children}
        </AppContext.Provider>
    );

}

export default AppContext;