"use strict";

const rollDice = (diceSize) => {
    return Math.floor(Math.random() * diceSize) + 1;
}

const roll4d6DropLowest = () => {
    let rolls = [];
    for (let dice = 0; dice < 4; dice++){
        rolls.push(rollDice(6));
    }
    rolls.sort();
    rolls.shift();
    console.log(rolls);
    return rolls.reduce((total, next)=> {return total + next;});
}

console.log(roll4d6DropLowest());