import React from "react";

const noBullets = {listStyleType: "none"};

function ListHealth(props)
{
    var col = "white";
    if (props.value <= (props.maxHealth * .25))
    {
        col = "red";
    }
    return <li style ={Object.assign({},{color: col}, {lineHeight: "100%"}, noBullets)}>{props.label}: {props.value}</li>
}

function HealthScreen(props)
{
    return(
        <ul>
            <ListHealth key={"MaxHealth"} value={props.maxHealth} label="Max Health" maxHealth={props.maxHealth} />
            <ListHealth key={"CurrentHealth"} value={props.currentHealth} label="Current Health" maxHealth={props.maxHealth} />
        </ul>
    )
}



export default HealthScreen;