
import React from "react";

function bonusCalc(stat: String, score: number)
{
    if (stat === "AC") return null;
    if (stat === "") return null;
    return Math.floor((score - 10) / 2)
}

function StatHeaders()
{
    return(
        <tr>
            <th style={{textAlign: "left"}}>Ability</th>
            <th style={{textAlign: "center"}}>Score</th>
            <th style={{textAlign: "left"}}>Bonus</th>
        </tr>
    )
}

function StatLine(props)
{
    var slot = props.slot;
    var score;
    var bonus;

    if (slot === "AC")
    {
        score = "";
        bonus = props.value;
    } else if(slot === "")
    {
        score = "";
        bonus = "";
    } else
    {
        score = props.value;
        bonus = bonusCalc(slot, score);
    }
    return(
        <tr>
            <td style={{textAlign: "left"}}>{slot}</td>
            <td style={{textAlign:"center"}}>{score}</td>
            <td style={{textAlign:"right"}}>{bonus}</td>
        </tr>
    )
}

function StatScreen(props)
{
    var statList = Object.keys(props.stats);
    var labels = statList.map((key) =>
                    { if (key === "")
                        {return <StatLine slot={key} value={""} />}
                      return <StatLine slot={key} value={props.stats[key]}  />
                    });
    return (
        <table>
            <StatHeaders />
            {labels}
        </table>
    )
}

export default StatScreen;