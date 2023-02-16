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
    return rolls.reduce((total, next)=> {return total + next;});
}

const populateValues = () => {
    const attributeValueInputs = document.querySelectorAll("input.character-attribute");
    for (const input of attributeValueInputs) {
        input.value = roll4d6DropLowest();
    }
}

populateValues();