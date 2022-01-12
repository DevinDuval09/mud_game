
import React from "react";

const noBullets = {listStyleType: "none"};

function bonusCalc(stat: String, score: number)
{
    if (stat === "Armor Class") return score;
    return Math.floor((score - 10) / 2)
}

function StatSlot(props)
{
    return(
        <li style={noBullets}>{props.slot}: {props.value} + "\t" {bonusCalc(props.slot, props.value)}</li>
    )
}

function StatScreen(props)
{
    var statList = Object.keys(props.stats);
    var labels = statList.map((key) => 
                   <StatSlot slot={key} value={props.equipment[key]}  />);
    return (
        <ul>
            {labels}
        </ul>
    )
}

export default StatScreen;