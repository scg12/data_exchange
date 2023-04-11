import React from 'react';
import classes from "./SubPages.module.css";
import CustomButton from "../../../customButton/CustomButton";
import UiContext from "../../../../../store/UiContext";
import { useContext, useState, useEffect } from "react";
import axiosInstance from '../../../../../axios';
import {Grid, GridColumn} from "@progress/kendo-react-grid";

import AddStudent from "../modals/AddStudent";
import BackDrop from "../../../backDrop/BackDrop";
import Select from 'react-select'
import { alpha, styled } from '@mui/material/styles';
import { DataGrid, gridClasses } from '@mui/x-data-grid';

let CURRENT_CLASSE_ID;

function ListeEleves(props) {
    const currentUiContext = useContext(UiContext);
    const [isValid, setIsValid] = useState(false);
    const [gridRows, setGridRows] = useState([]);
    const [modalOpen, setModalOpen] = useState(0); //0 = close, 1=creation, 2=modif
    const selectedTheme = currentUiContext.theme;

    useEffect(()=> {
        //listEtabs()
        if(gridRows.length==0){
            CURRENT_CLASSE_ID = undefined;
        }
        
    },[]);


    const ODD_OPACITY = 0.2;
    
    const StripedDataGrid = styled(DataGrid)(({ theme }) => ({
      [`& .${gridClasses.row}.even`]: {
        backgroundColor: theme.palette.grey[200],
        '&:hover, &.Mui-hovered': {
          backgroundColor: alpha(theme.palette.primary.main, ODD_OPACITY),
          '@media (hover: none)': {
            backgroundColor: 'transparent',
          },
        },
        '&.Mui-selected': {
          backgroundColor: alpha(
            theme.palette.primary.main,
            ODD_OPACITY + theme.palette.action.selectedOpacity,
          ),
          '&:hover, &.Mui-hovered': {
            backgroundColor: alpha(
              theme.palette.primary.main,
              ODD_OPACITY +
                theme.palette.action.selectedOpacity +
                theme.palette.action.hoverOpacity,
            ),
            // Reset on touch devices, it doesn't add specificity
            '@media (hover: none)': {
              backgroundColor: alpha(
                theme.palette.primary.main,
                ODD_OPACITY + theme.palette.action.selectedOpacity,
              ),
            },
          },
        },
      },
    }));

    
    
/*************************** DataGrid Declaration ***************************/    
    const columns = [
       
        {
            field: 'matricule',
            headerName: 'MATRICULE',
            width: 100,
            editable: false,
            headerClassName:classes.GridColumnStyle
        },
        {
            field: 'nom',
            headerName: 'NOM ET PRENOM(S)',
            width: 200,
            editable: false,
            headerClassName:classes.GridColumnStyle
        },
        {
            field: 'date_naissance',
            headerName: 'DATE NAISSANCE',
            width: 110,
            editable: false,
            headerClassName:classes.GridColumnStyle
        },
        {
            field: 'lieu_naissance',
            headerName: 'LIEU NAISANCE',
            width: 120,
            editable: false,
            headerClassName:classes.GridColumnStyle
        },
        {
            field: 'date_entree',
            headerName: 'DATE ENTREE',
            width: 110,
            editable: false,
            headerClassName:classes.GridColumnStyle,
                
        },
        {
            field: 'nom_pere',
            headerName: 'NOM PARENT',
            width: 200,
            editable: false,
            headerClassName:classes.GridColumnStyle
        },

        {
            field: 'redouble',
            headerName: 'SITUATION',
            width: 110,
            editable: false,
            headerClassName:classes.GridColumnStyle,
                
        },

        {
            field: 'modif',
            headerName: '',
            width: 15,
            editable: false,
            hide:(props.formMode=='ajout')? false : true,
            headerClassName:classes.GridColumnStyle,
            renderCell: (params)=>{
                return(
                    <div className={classes.inputRow}>
                        <img src="icons/baseline_edit.png"  
                            width={17} 
                            height={17} 
                            className={classes.cellPointer} 
                            onClick={(event)=> {
                                event.ignore = true;
                            }}
                            alt=''
                        />
                    </div>
                )}           
                
            },


        
            {
                field: 'id',
                headerName: '',
                width: 15,
                editable: false,
                headerClassName:classes.GridColumnStyle,
                hide:(props.formMode=='ajout')? false : true,
                renderCell: (params)=>{
                    return(
                        <div className={classes.inputRow}>
                            <img src="icons/baseline_delete.png"  
                                width={17} 
                                height={17} 
                                className={classes.cellPointer} 
                                //onClick={deleteRow}
                                alt=''
                            />
                        </div>
                    );
                    
                }
            },
        ];

      const rows1 = [
        { matricule:"03p256", nom: 'Mbala Simplice', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant', modif:1, id:1},
        { matricule:"03p257", nom: 'Mengue Elise', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant',   modif:1, id:2},
        { matricule:"03p258", nom: 'Abessolo Andre', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant', modif:1, id:3},
        { matricule:"03p259", nom: 'Kengne Mathias', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant', modif:1, id:4},
        { matricule:"03p255", nom: 'Sadjo Alice', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant',    modif:1, id:5},
        { matricule:"03p254", nom: 'Marga Calixte', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant',  modif:1, id:6},
        { matricule:"03p258", nom: 'Eteme Ruth', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant',     modif:1, id:7},
        { matricule:"03p252", nom: 'Pekele Luc', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant',     modif:1, id:8}
      ];

      const rows2 = [
        { matricule:"03p246", nom: 'Mbala Simplice', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant', modif:1, id:1},
        { matricule:"03p247", nom: 'Mengue Elise', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant',   modif:1, id:2},
        { matricule:"03p248", nom: 'Abessolo Andre', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant', modif:1, id:3},
        { matricule:"03p249", nom: 'Kengne Mathias', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant', modif:1, id:4},
        { matricule:"03p245", nom: 'Sadjo Alice', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant',    modif:1, id:5},
        { matricule:"03p244", nom: 'Marga Calixte', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant',  modif:1, id:6},
        { matricule:"03p248", nom: 'Eteme Ruth', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant',     modif:1, id:7},
        { matricule:"03p242", nom: 'Pekele Luc', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant',     modif:1, id:8}
      ];

      const rows3 = [
        { matricule:"03p236", nom: 'Mbala Simplice', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant', modif:1, id:1},
        { matricule:"03p237", nom: 'Mengue Elise', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant',   modif:1, id:2},
        { matricule:"03p238", nom: 'Abessolo Andre', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant', modif:1, id:3},
        { matricule:"03p239", nom: 'Kengne Mathias', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant', modif:1, id:4},
        { matricule:"03p235", nom: 'Sadjo Alice', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant',    modif:1, id:5},
        { matricule:"03p234", nom: 'Marga Calixte', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant',  modif:1, id:6},
        { matricule:"03p238", nom: 'Eteme Ruth', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant',     modif:1, id:7},
        { matricule:"03p232", nom: 'Pekele Luc', date_naissance: '12/07/2007', lieu_naissance:'yaounde', date_entree:'12/01/2019', nom_pere: 'Mbala Lucien',  redouble: 'redoublant',     modif:1, id:8}
      ];

    function getClassStudentList(classId){
        switch(classId){
            case '6em1': return rows1 ;
            case '5em2': return rows2 ;
            case '4A2':  return rows3 ;
            case '3E':   return rows1 ;
            case '2c1':  return rows2 ;
            case '1L':   return rows3 ;
            case 'TD':   return rows2 ;
        }

    }
    
    const optClasse=[
        {value: '0',      label:'Choisir une classe'    },
        {value: '6em1',   label:'6ieme 1'               },
        {value: '5em2',   label:'5ieme 2'               },
        {value: '4A2',    label:'4ieme A2'              },
        {value: '3E',     label:'3ieme Esp'             },
        {value: '2c1',    label:'2nd C1'                },
        {value: '1L',     label:'1ere L'                },
        {value: 'TD',     label:'Tle D'                 }
    ]


/*************************** Theme Functions ***************************/
    function getGridButtonStyle()
    { // Choix du theme courant
        switch(selectedTheme){
            case 'Theme1': return classes.Theme1_gridBtnstyle + ' '+ classes.margRight5P ;
            case 'Theme2': return classes.Theme2_gridBtnstyle + ' '+ classes.margRight5P;
            case 'Theme3': return classes.Theme3_gridBtnstyle + ' '+ classes.margRight5P;
            default: return classes.Theme1_gridBtnstyle + ' '+ classes.margRight5P;
        }
    }
    
/*************************** Handler functions ***************************/
    

    function handleDeleteRow(params){
        if(params.field=='id'){
            //console.log(params.row.matricule);
            deleteRow(params.row.matricule);            
        }
    }

    function handleEditRow(row){       
        var inputs=[];

        inputs[0]= row.nom;
        inputs[1]= row.prenom;
        inputs[2]= row.date_naissance;
        inputs[3]= row.lieu_naissance;
        inputs[4]= row.etab_origine;

        inputs[5]= row.nom_pere;
        inputs[6]= row.email_pere;
        inputs[7]= row.tel_pere;

        inputs[8]= row.nom_mere;
        inputs[9]= row.email_mere;
        inputs[10]= row.tel_mere;

        inputs[11]= row.matricule;

     
        currentUiContext.setFormInputs(inputs)
        setModalOpen(2);

    }

    function consultRowData(row){
        var inputs=[];

        inputs[0]= row.nom;
        inputs[1]= row.prenom;
        inputs[2]= row.date_naissance;
        inputs[3]= row.lieu_naissance;
        inputs[4]= row.etab_origine;

        inputs[5]= row.nom_pere;
        inputs[6]= row.email_pere;
        inputs[7]= row.tel_pere;

        inputs[8]= row.nom_mere;
        inputs[9]= row.email_mere;
        inputs[10]= row.tel_mere;

        inputs[11]= row.matricule;

     
        currentUiContext.setFormInputs(inputs)
        setModalOpen(3);

    }

    function addNewStudent(eleve) {       
       // e.preventDefault();        
        console.log('Ajout',eleve);

        //var etablismnt = getFormData();

        /*if (formDataCheck(etablismnt).length==0) {                        
            axiosInstance.post(`create-etab/`, {
                    libelle: etablismnt.libelle,
                    date_creation: etablismnt.date_creation,
                    nom_fondateur:  etablismnt.nom_fondateur,
                    localisation: etablismnt.localisation,
                    bp: etablismnt.bp,
                    email: etablismnt.email,
                    tel: etablismnt.tel,
                    devise: etablismnt.devise,
                    logo: etablismnt.logo,
                    langue: etablismnt.langue,
                    site_web: etablismnt.site_web
            }).then((res)=>{
                console.log(res.data);
                //Retourner la liste des etablissements et charger le tableau avec(map)
                // Mettre a jour le useState.
                listEtabs();
                ClearForm();
                setModalOpen(0);
            }) 
            
        } else {
            var errorDiv = document.getElementById('errMsgPlaceHolder');
            errorDiv.className = classes.errorMsg;
            errorDiv.textContent = formDataCheck(etablismnt);
        }*/
        
    }
    
    function modifyStudent(eleve) {
        //e.preventDefault();
        console.log('Modif',eleve);
     
        /*if (formDataCheck(etablismnt).length==0) { 
            axiosInstance.post(`update-etab/`, {
                id: etablismnt.id,
                libelle: etablismnt.libelle,
                date_creation: etablismnt.date_creation,
                nom_fondateur:  etablismnt.nom_fondateur,
                localisation: etablismnt.localisation,
                bp: etablismnt.bp,
                email: etablismnt.email,
                tel: etablismnt.tel,
                devise: etablismnt.devise,
                logo: etablismnt.logo,
                langue: etablismnt.langue,
                site_web: etablismnt.site_web
            }).then((res)=>{
                console.log(res.data);
                 //Retourner la liste des etablissements et charger le tableau avec(map)
                // Mettre a jour le useState.
                listEtabs();
                ClearForm();
                setModalOpen(0);
            })          

        } else {
            var errorDiv = document.getElementById('errMsgPlaceHolder');
            errorDiv.className = classes.errorMsg;
            errorDiv.textContent = formDataCheck(etablismnt);
        }*/
    }

    function deleteRow(rowId) {
        alert(rowId);
        //Message de confirmation
        /*if(window.confirm('Voulez-vous vraiment supprimer la section selectionnée?')){
            //requete  axios de suppression de l'eatab qui a cet id
            axiosInstance
            .post(`delete-etab/`, {
                id:rowId,
            }).then((res)=>{
                console.log(res.data.status)
                 //Mise a jour du tableau
                //setDataState(result)
            })              
        }*/
    } 

    function quitForm() {
        //ClearForm();
        setModalOpen(0)
    }
   
    function dropDownHandler(e){
        //console.log(e.target.value)
        if(e.target.value != optClasse[0].value){
            var grdRows = getClassStudentList(e.target.value);
            setGridRows(grdRows);
            CURRENT_CLASSE_ID = e.target.value;  
        }else{
            CURRENT_CLASSE_ID = undefined;
            setGridRows([]);
        }
    }

    function AddNewStudentHandler(e){
        e.preventDefault();
        //setModalOpen(1); 
        //currentUiContext.setFormInputs([])
        //alert(document.getElementById('classeId').value);
        console.log(CURRENT_CLASSE_ID);
        if(CURRENT_CLASSE_ID != undefined){
            setModalOpen(1); 
            currentUiContext.setFormInputs([])
        } else{
            alert("Vous devez d'abord selectionner la classe dans laquelle vous voulez ajouter l'eleve")
        }
    }

    /********************************** JSX Code **********************************/   
    return (
        <div className={classes.formStyleP}>
             {(modalOpen!=0) && <BackDrop/>}
             {(modalOpen!=0) && <AddStudent formMode= {(modalOpen==1) ? 'creation': (modalOpen==2) ?  'modif' : 'consult'}  actionHandler={(modalOpen==1) ? addNewStudent : modifyStudent} cancelHandler={quitForm} />}
            <div className={classes.inputRow}>
                {(props.formMode=='ajout')?  
                    <div className={classes.formTitle}>
                        ENREGISTREMENT ET GESTION DES EFFECTIFS 
                    </div>
                    :
                    <div className={classes.formTitle}>
                        CONSULTATION DES LISTES PAR CLASSES 
                    </div>
                }
            </div>
            <div className={classes.formGridContent}>
              
                <div className={classes.gridTitleRow}> 
                    <div className={classes.gridTitle}>                  
                        <div className={classes.gridTitleText}>
                            LISTE DES ELEVES POUR LA CLASSE DE :
                        </div>
                      
                        <div className={classes.selectZone}>
                            <select onChange={dropDownHandler} className={classes.comboBoxStyle} style={{width:'11.3vw', marginBottom:1}}>
                                {(optClasse||[]).map((option)=> {
                                    return(
                                        <option  value={option.value}>{option.label}</option>
                                    );
                                })}
                            </select>                          
                        </div>
                    </div>
                    
                                
                    <div className={classes.gridAction}> 
                        {(props.formMode=='ajout')?
                            <CustomButton
                                btnText='Nvel. Eleve'
                                hasIconImg= {true}
                                imgSrc='images/addNewUserOrg.png'
                                imgStyle = {classes.grdBtnImgStyle}  
                                buttonStyle={getGridButtonStyle()}
                                btnTextStyle = {classes.gridBtnTextStyle}
                                btnClickHandler={AddNewStudentHandler}
                                disable={(modalOpen==1||modalOpen==2)}   
                            />
                            :
                            null
                        }

                        <CustomButton
                            btnText='Imprimer'
                            hasIconImg= {true}
                            imgSrc='images/printing1.png'
                            imgStyle = {classes.grdBtnImgStyle}  
                            buttonStyle={getGridButtonStyle()}
                            btnTextStyle = {classes.gridBtnTextStyle}
                            btnClickHandler={()=>{setModalOpen(1); currentUiContext.setFormInputs([])}}
                            disable={(modalOpen==1||modalOpen==2)}   
                        />

                        <CustomButton
                            btnText='Importer'
                            hasIconImg= {true}
                            imgSrc='images/import.png'
                            imgStyle = {classes.grdBtnImgStyle} 
                            buttonStyle={getGridButtonStyle()}
                            btnTextStyle = {classes.gridBtnTextStyle}
                            btnClickHandler={()=>{setModalOpen(1); currentUiContext.setFormInputs([])}}
                            disable={(modalOpen==1||modalOpen==2)}   
                        />
                    </div>
                        
                    </div>
                    
                

                {(modalOpen==0) ?
                    <div className={classes.gridDisplay} >
                        <StripedDataGrid
                            rows={gridRows}
                            columns={columns}
                            getCellClassName={(params) => (params.field==='nom')? classes.gridMainRowStyle : classes.gridRowStyle }
                            onCellClick={handleDeleteRow}
                            onRowClick={(params,event)=>{
                                if(event.ignore) {
                                    //console.log(params.row);
                                    handleEditRow(params.row)
                                }
                            }}  
                            
                            onRowDoubleClick ={(params, event) => {
                                event.defaultMuiPrevented = true;
                                consultRowData(params.row)
                            }}
                            
                            //loading={loading}
                            //{...data}
                            sx={{
                                //boxShadow: 2,
                                //border: 2,
                                //borderColor: 'primary.light',
                                '& .MuiDataGrid-cell:hover': {
                                  color: 'primary.main',
                                  border:0,
                                  borderColor:'none'
                                },
                              
                            }}
                            getRowClassName={(params) =>
                                params.indexRelativeToCurrentPage % 2 === 0 ? 'even ' + classes.gridRowStyle : 'odd '+ classes.gridRowStyle
                            }
                        />
                    </div>
                    :
                    null
                }
            
            </div>
        </div>
        
    );
} 
export default ListeEleves;