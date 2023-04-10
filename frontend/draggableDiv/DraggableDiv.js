import React from 'react';
import {useDrag} from 'react-dnd';

function DraggableDiv(props){
    const [{isDragging},drag] = useDrag(()=>({

        type: props.type,

        item:{id:props.id},

        collect: (monitor) => ({
            isDragging:!!monitor.isDragging(),
        })
    }));

    return(
        <div id={props.id} title={props.title} className={props.className} ref={drag} onClick={props.onClick}>
            {props.children}
        </div>
    );
}

export default DraggableDiv;
