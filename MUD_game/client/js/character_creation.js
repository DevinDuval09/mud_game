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

const transformFormInputs = (formdata) => {
    const transformedData = new FormData();
    let success = true;
    for (const attribute_array of formdata.entries()){
        if (/character-[a-z]{4}/.test(attribute_array[0])) {
            const serverAttr = attribute_array[0].match(/(?<=-)[a-z]{4}/g);
            console.log("server attribute: ", serverAttr);
            transformedData.append(serverAttr, attribute_array[1]);
            continue;
        }
        if (/attribute[\d]-value/.test(attribute_array[0])) {
            const inputNumber = attribute_array[0].match(/(?<=attribute)\d/g);
            transformedData.append(formdata.get(`attribute${inputNumber}-name`), attribute_array[1]);
            continue;
        }
        if (/attribute[\d]-name/.test(attribute_array[0])) {
            continue;
        }
        if (attribute_array[0] == "password") {
            transformedData.append(attribute_array[0], attribute_array[1]);
            continue;
        }
        success = false;

        }
        return success? transformedData: null;
    }

const validateForm = (evt) => {
    evt.preventDefault();
    evt.stopPropagation();
    const form = document.querySelector("form");
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
    const raw_data = new FormData(document.querySelector("form"));
    const cleaned_data = transformFormInputs(raw_data);
    if (!cleaned_data) {
        console.log("Error transforming data.");
        return;
    }
    const post = new XMLHttpRequest();
    post.onreadystatechange = (evt) => {
        if (post.readyState == 4 && post.status == 200) {
            window.location = `${defaultURL}`;
        }
    }
    post.open("post", `/character_creation`);
    post.send(cleaned_data);
}

populateValues();
document.querySelector("form").addEventListener("submit", validateForm);
document.getElementById("character-name").addEventListener("change", verifyNameFromChange);