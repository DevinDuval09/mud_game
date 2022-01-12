import React from "react";

const noBullets = {listStyleType: "none"};

function EquipmentSlot(props)
{
    return(
        <li style={noBullets}>{props.slot}: {props.value}</li>
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