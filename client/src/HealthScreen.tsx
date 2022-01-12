import React from "react";

function ListHealth(props)
{
    var col = "white";
    if (props.value <= (props.maxHealth * .25))
    {
        col = "red";
    }
    return <li style ={{color: col}}>{props.label}: {props.value}</li>
}

function HealthScreen(props)
{
    /*const listValues = {"Max Health": props.maxHealth, 
                        "Current Health": props.currentHealth};
    const healthLabels = Object.entries(listValues).map(([text, number]) =>
    <ListHealth key={text} label={text} value={number.toString()}/>)
    return(
        <ul>
            {healthLabels}
        </ul>
    )*/
    return(
        <ul>
            <ListHealth value={props.maxHealth} label="Max Health" maxHealth={props.maxHealth} />
            <ListHealth value={props.currentHealth} label="Current Health" maxHealth={props.maxHealth} />
        </ul>
    )
}



export default HealthScreen;