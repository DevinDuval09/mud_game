"use strict";
const defaultURL = "127.0.0.1";
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

const getServerResponse = (url, callback) => {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = (evt) => {
        evt.preventDefault();
        evt.stopPropagation();
        if(xhr.readyState == 4 && xhr.status == 200) {
            console.log("received response");
            callback(xhr.responseText);
        }
    }
    xhr.open("GET", url);
    xhr.send();
}

const nameValidation = (string) => {
    const serverResponse = JSON.parse(string);
    const errorList = document.querySelector("#error > ul");
    deleteChildren(errorList);
    if (!serverResponse["name_available"]) {
        const errors = [];
        serverResponse["name_available"] == false? errors.push("Name not available.") : errors.push(serverResponse);
        populateList(errors, errorList);
        return false;
    };
    return true;
}

const verifyNameFromChange = (evt) => {
    evt.preventDefault();
    evt.stopPropagation();
    const name = evt.target.value.trim();
    if(name) {
        const url = `${defaultURL}/verify:${name}`;
        getServerResponse(url, nameValidation);
    }
}

const validateForm = (evt) => {
    evt.preventDefault();
    evt.stopPropagation();
    const form = evt.target;
    const attributeArray = [];
    const errorList = document.querySelector("#error > ul");
    const errors = [];
    //if name not available is listed, keep that in the error list
    if (errorList.innerText.indexOf("Name not available.") > -1) {
        errors.push("Name not available.");
    }
    deleteChildren(errorList);
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
    console.lof("submitting form");
    form.submit();

}

populateValues();
document.querySelector("form").addEventListener("submit", validateForm);
document.getElementById("character-name").addEventListener("change", verifyNameFromChange);