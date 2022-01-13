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
            <ListHealth value={props.maxHealth} label="Max Health" maxHealth={props.maxHealth} />
            <ListHealth value={props.currentHealth} label="Current Health" maxHealth={props.maxHealth} />
        </ul>
    )
}



export default HealthScreen;