import React from 'react';
import classes from "./SubPages.module.css";
import CustomButton from "../../../customButton/CustomButton";
import UiContext from "../../../../../store/UiContext";
import AppContext from "../../../../../store/AppContext";
import { useContext, useState, useEffect } from "react";
import axiosInstance from '../../../../../axios';

// import AddStudent from "../modals/AddStudent";
// import BackDrop from "../../../backDrop/BackDrop";
// import Select from 'react-select'
import { alpha, styled } from '@mui/material/styles';
import { DataGrid, gridClasses } from '@mui/x-data-grid';

let CURRENT_CLASSE_ID;
let notes = [],libelle_classe="";

function SaveNotes(props) {
    const currentUiContext = useContext(UiContext);
    const currentAppContext = useContext(AppContext);
    const [isValid, setIsValid] = useState(false);
    const [gridRows, setGridRows] = useState([]);
    const [optClasse, setOptClasse] = useState([]);
    const [modalOpen, setModalOpen] = useState(0); //0 = close, 1=creation, 2=modif
    const selectedTheme = currentUiContext.theme;

    useEffect(()=> {
        //listEtabs()
        if(gridRows.length==0){
            CURRENT_CLASSE_ID = undefined;
        }
        setOptClasse(createOption(currentAppContext.infoClasses.filter((classe)=>classe.id_setab == currentAppContext.currentEtab),'id_classe','libelle'));
        
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
            headerName: 'NOM',
            width: 100,
            editable: false,
            headerClassName:classes.GridColumnStyle
        },
        {
            field: 'prenom',
            headerName: 'PRENOM',
            width: 100,
            editable: false,
            headerClassName:classes.GridColumnStyle
        },
        {
            field: 'score',
            headerName: 'NOTE',
            width: 60,
            editable: true,
            headerClassName:classes.GridColumnStyle,
            renderCell: (params) => (
                // <label>10</label>
                <input defaultValue="10" onKeyPress={checkKey} type="number" min="0" max="20" tabIndex="0" />
            ),
        },
        

        // {
        //     field: 'modif',
        //     headerName: '',
        //     width: 33,
        //     editable: false,
        //     headerClassName:classes.GridColumnStyle,
        //     renderCell: (params)=>{
        //         return(
        //             <div className={classes.inputRow}>
        //                 <img src="icons/baseline_edit.png"  
        //                     width={20} 
        //                     height={20} 
        //                     className={classes.cellPointer} 
        //                     onClick={(event)=> {
        //                         event.ignore = true;
        //                     }}
        //                     alt=''
        //                 />
        //             </div>
        //         )}                
        // },
    ];

    function checkKey(e){
        if(e.keyCode == '38')
        console.log('esd')
        else if(e.keyCode == '40')
        console.log('fgdf')
        else if(e.keyCode == '37')
        console.log('cvbf')
        else if(e.keyCode == '39')
        console.log('wsdf')
    }
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

    function getSelectDropDownTextColr() {
        switch(selectedTheme){
            case 'Theme1': return 'rgb(60, 160, 21)';
            case 'Theme2': return 'rgb(64, 49, 165)';
            case 'Theme3': return 'rgb(209, 30, 90)';
            default: return 'rgb(60, 160, 21)';
        }   
    }
    
/*************************** Handler functions ***************************/
    

    function handleDeleteRow(params){
        if(params.field=='id'){
            //console.log(params.row.matricule);
            // deleteRow(params.row.matricule);            
        }
    }

    function handleEditRow(row){       
        var inputs=[];
        console.log(row);
        // inputs[0]= row.nom;
        // inputs[1]= row.prenom;
        // inputs[2]= row.date_naissance;
        // inputs[3]= row.lieu_naissance;
        // inputs[4]= row.etab_origine;

        // inputs[5]= row.nom_pere;
        // inputs[6]= row.email_pere;
        // inputs[7]= row.tel_pere;

        // inputs[8]= row.nom_mere;
        // inputs[9]= row.email_mere;
        // inputs[10]= row.tel_mere;

        // inputs[11]= row.matricule;

     
        currentUiContext.setFormInputs(inputs)
        setModalOpen(2);

    }

    function consultRowData(row){
        var inputs=[];

        // inputs[0]= row.nom;
        // inputs[1]= row.prenom;
        // inputs[2]= row.date_naissance;
        // inputs[3]= row.lieu_naissance;
        // inputs[4]= row.etab_origine;

        // inputs[5]= row.nom_pere;
        // inputs[6]= row.email_pere;
        // inputs[7]= row.tel_pere;

        // inputs[8]= row.nom_mere;
        // inputs[9]= row.email_mere;
        // inputs[10]= row.tel_mere;

        // inputs[11]= row.matricule;

     
        currentUiContext.setFormInputs(inputs)
        setModalOpen(3);

    }

    function listNotes(id_classe,id_sequence,id_cours){
        console.log("currentAppContext.currentEtab: ",currentAppContext.currentEtab)
        notes=[];
        axiosInstance
        .post(`list-note-matiere-classe/`,{
            id_sousetab: currentAppContext.currentEtab,
            id_classe:id_classe,
            id_sequence:id_sequence,
            id_cours:id_cours
        }).then((res)=>{
            res.data.notes.map((note)=>{notes.push(note)});
            setGridRows(notes);
        })  
    }

    function quitForm() {
        //ClearForm();
        setModalOpen(0)
    }
   
    function dropDownHandler(e){
        //console.log(e.target.value)
        // if(e.target.value != optClasse[0].value){
        //     // var grdRows = getClassStudentList(e.target.value);
        //     setGridRows(grdRows);
        //     CURRENT_CLASSE_ID = e.target.value;  
        // }else{
        //     CURRENT_CLASSE_ID = undefined;
        //     setGridRows([]);
        // }
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

    function dropDownClasseChangeHandler(e){
        CURRENT_CLASSE_ID = document.getElementById('id_classe').value;
        let select = document.getElementById('id_classe');
        console.log("Classe: ",e)
        if(CURRENT_CLASSE_ID!=""){
            let id_sequence = 1;
            let id_cours = 1;
            listNotes(CURRENT_CLASSE_ID,id_sequence,id_cours);
            libelle_classe = select.options[select.selectedIndex].text;
        }
        else{
            libelle_classe = "";
            setGridRows([]);
        } 
    }  
    function createOption(tabOption,idField, labelField){
        var newTab=[];
        newTab.push({value:"",label:""})
        for(var i=0; i< tabOption.length; i++){
            var obj={
                value: tabOption[i][idField],
                label: tabOption[i][labelField]
            }
            newTab.push(obj);
        }
        return newTab;
    }
    /********************************** JSX Code **********************************/   
    return (
        <div className={classes.formStyleP}>
             {/* {(modalOpen!=0) && <BackDrop/>}
             {(modalOpen!=0) && <AddStudent formMode= {(modalOpen==1) ? 'creation': (modalOpen==2) ?  'modif' : 'consult'}  actionHandler={(modalOpen==1) ? addNewStudent : modifyStudent} cancelHandler={quitForm} />} */}
            <div className={classes.inputRow}>
                {/* {(props.formMode=='ajout')?  
                    <div className={classes.formTitle}>
                        SAISIE DES NOTES 1
                    </div>
                    : */}
                    <div className={classes.formTitle}>
                        SAISIE DES NOTES
                    </div>
                {/* } */}
            </div>
            <div className={classes.formGridContent}>
              
                <div className={classes.gridTitleRow}> 
                    <div className={classes.gridTitle}>                  
                        <div className={classes.gridTitleText}>
                            Classe:
                        </div>
                      
                        <div className={classes.selectZone}>
                            <select className={classes.comboBoxStyle} id="id_classe" style={{color:getSelectDropDownTextColr(), width:'10vw',borderColor:getSelectDropDownTextColr()}}
                            onChange={dropDownClasseChangeHandler}>
                                {(optClasse||[]).map((option)=> {
                                    return(
                                        <option  value={option.value}>{option.label}</option>
                                    );
                                })}
                            </select>                          
                        </div>
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
                                if(event.ignore) 
                                {
                                    //console.log(params.row);
                                    handleEditRow(params.row)
                                }
                            }}  
                            
                            // onRowDoubleClick ={(params, event) => {
                            //     event.defaultMuiPrevented = true;
                            //     consultRowData(params.row)
                            // }}
                            
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
export default SaveNotes;