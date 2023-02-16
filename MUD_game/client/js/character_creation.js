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

const deleteChildren = (elementList) => {
    while (elementList.children[0]) {
        elementList.children[0].remove();
    }
}

const populateList = (strings, listElement) => {
    deleteChildren(listElement);
    for(const string of strings) {
        const li = document.createElement("li");
        li.appendChild(document.createTextNode(string));
        listElement.appendChild(li);
    }
}

const validateForm = (evt) => {
    evt.preventDefault();
    evt.stopPropagation();
    const form = evt.target;
    const attributeArray = [];
    const errorList = document.querySelector("#error > ul");
    deleteChildren(errorList);
    const errors = [];
    if (document.getElementById("password").value !== document.getElementById("password2").value) {
        errors.push("Passwords do not match.");
    }
    for (const attribute of form.querySelectorAll("select")) {
        attributeArray.push(attribute.value);
    }
    attributeArray.sort();
    for (let i = 1; i < attributeArray.length; i++) {
        if (attributeArray[i] == attributeArray[i-1]) {
            errors.push("Each attribute can only be selected once.")
        }
    }
    if (errors.length > 0) {
        populateList(errors, errorList);
        return;
    }
    form.submit();

}

populateValues();
document.querySelector("form").addEventListener("submit", validateForm);