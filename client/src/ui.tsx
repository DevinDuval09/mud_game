import React from "react";

function ListHealth(props)
{
    var col = "white";
    if (props.value <= (props.maxHealth * .25))
    {
        col = "red";
    }
    return <li style ={{color: col}}>{props.label}: {props.currentHealth}</li>
}

function HealthScreen(props)
{
    const listValues = {"Max Health": props.maxHealth, 
                        "Current Health": props.currentHealth};
    const healthLabels = Object.entries(listValues).map(([text, number]) =>
    <ListHealth key={text} label={text} value={number}/>)
    return(
        <ol>
            {healthLabels}
        </ol>
    )
}



export {
    HealthScreen,
}