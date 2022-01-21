import React from "react";

function EquipmentSlot(props)
{
    return(
        <tr>
            <td style={{textAlign:"left"}}>{props.slot}:</td>
            <td style={{textAlign:"left"}}>{props.value}</td>
        </tr>
    )
}

function EquipmentPanel(props)
{
    var equipmentList = Object.keys(props.equipment);
    var data = equipmentList.map((key) => 
                   <EquipmentSlot slot={key} value={props.equipment[key]}  />);
    var labels = <tr>
                    <th>Slot</th>
                    <th>Item</th>
                </tr>
    return (
        <div style={{display: "table"}}>
            <table>
                {labels}
                {data}
            </table>
        </div>
    )
}

export default EquipmentPanel;