import React from "react";


  type Equipment ={
                    Head: String,
                    Torso: String,
                    Arms?: String,
                    MainHand: String,
                    OffHand: String,
                    Legs: String,
                    Belt?: String,
                    Back: String,
                    Feet?: String,
                    Cloak: String
                  };

function EquipmentSlot(props)
{
    return(
        <li>{props.slot}: {props.value}</li>
    )
}

function EquipmentPanel(equipment: Equipment)
{
    const labels = Object.keys(equipment);
    labels.map((key) => 
                   <EquipmentSlot slot={key} value={equipment[key]}  />);
    return (
        <ul>
            {labels}
        </ul>
    )
}

export default EquipmentPanel;