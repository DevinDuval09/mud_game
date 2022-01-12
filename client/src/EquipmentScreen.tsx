import React from "react";

function EquipmentSlot(props)
{
    return(
        <li>{props.slot}: {props.value}</li>
    )
}

function EquipmentPanel(props)
{
    var equipmentList = Object.keys(props.equipment);
    var labels = equipmentList.map((key) => 
                   <EquipmentSlot slot={key} value={props.equipment[key]}  />);
    return (
        <ul>
            {labels}
        </ul>
    )
}

export default EquipmentPanel;