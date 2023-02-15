"use strict";
const defaultPort = 50000;
const defaultURL = "127.0.0.1";
//build a state manager to handle incoming/outgoing messages from server
//server sends json describing what the page looks like
//state manager decodes json and updates panels as necessary
const PanelHandler = class {
    constructor(elem, description) {
        this.element = elem;
        this.type = description;
        //current text values of the bottom of the element.
        //All text should be in a span
        this.currentText = [];
        const spanList = this.element.querySelectorAll("span");
        if (spanList) {
            for (const textSpan of this.element.querySelectorAll("span")) {
                this.currentText.push(textSpan.innerText);
            }
        }
    }
    //remove function? currentText gets updated by subclass
    update() {
        let counter = 0;
        for (const span of this.element.querySelectorAll("span")) {
            if (!this.currentText.includes(span.innerText)) {
                this.currentText.push(span.innerText);
                ++counter;
            }
        }
        return counter;
    }

    isUpToDate(textArray) {
        if (this.currentText.length !== textArray.length) return false;
        for (let i = 0; i < this.currentText.length; ++i) {
            if (textArray[i] != this.currentText[i]) return false;
        }
        return true;
    }

    clearText() {
        for (const span of this.element.querySelectorAll("span")) {
            span.innerText = null;
        }
        this.currentText = [];
    }

    static createTextElement(type) {
        const span = document.createElement("span");
        const element = document.createElement(type);
        element.appendChild(span);
        return element;
    }
}

const ListPanelHandler = class extends PanelHandler {
    constructor(elem, description, liLimit) {
        super(elem);
        this.list = this.element.querySelector("ul");
        this.maxLines = liLimit;
    }

    addLine(text) {
        let liList = this.list.querySelectorAll("li");
        //check list size against maxLines
        if (liList && this.maxLines && liList.length == this.maxLines) {
            //if maxLines has been reached, remove last item from current text
            //later, currentText will be used to repopulate all the list items
            this.currentText.shift();
        } else {
            //if maxLines has not been reached, add another list item and refresh liList
            const newLi = PanelHandler.createTextElement("li");
            this.list.appendChild(newLi);
            liList = this.list.querySelectorAll("li");
        }
        //add new text to current text
        this.currentText.push(text);
        //clear all LI
        while (this.list.children[0]) {
            this.list.children[0].remove();
        }
        //create appropriate number of LI
        while (this.list.children.length < this.currentText.length) {
            const newLi = PanelHandler.createTextElement("li");
            this.list.appendChild(newLi);
        }
        liList = this.list.querySelectorAll("li");
        //populate LI
        for (let i = 0; i < liList.length; ++i) {
            //for each item in currentText, add it to a span and put it into an li
            const span = liList[i].querySelector("span");
            span.appendChild(document.createTextNode(this.currentText[i]));
        }
    }

    clearText() {
        super.clearText();
        while(this.list.children[0]) {
            this.list.children[0].remove();
        }
    }
}

const ConditionalNumberPanel = class extends PanelHandler {
    constructor(elem, description, current, max) {
        super(elem, description)
        this.currentValue = current;
        this.maxValue = max;
    }
    determineColor() {
        const percentage = this.currentValue/this.maxValue;
        if(percentage > .75) return "green";
        if(percentage > .5) return "yellow";
        if(percentage > .25) return "orange";
        return "red";
    }

    display() {
        let span = this.element.querySelector("span");
        if (!span) span = document.createElement("span");
        const text = `${this.currentValue}/${this.maxValue}`;
        const displayColor = this.determineColor();
        span.innerText = null;
        span.appendChild(document.createTextNode(text));
        span.style.color = displayColor;
        this.element.appendChild(span);
    }

    setCurrentValue(currentVal){
        this.currentValue = currentVal;
        this.display();
    }
}

const ParagraphPanel = class extends PanelHandler {
    constructor(element, description){
        super(element, description);
        this.paragraph = this.element.querySelector("p");
        if(!this.paragraph) {
            this.paragraph = document.createElement("p");
            this.element.appendChild(this.paragraph);
        }
    }

    updateText(text){
        this.paragraph.innerText = null;
        this.paragraph.appendChild(document.createTextNode(text));
    }
}

const playerLog = new ListPanelHandler(document.getElementById("log"), "event", 50);
const roomDescription = new ParagraphPanel(document.getElementById("room-description"), "roomDescription");
const roomObjects = new ListPanelHandler(document.getElementById("room-objects"), "roomObjects", null);
const roomCharacters = new ListPanelHandler(document.getElementById("room-characters", "roomCharacters", null));
const playerInventory = new ListPanelHandler(document.getElementById("inventory"), "playerInventory", 20);
const playerHealth = new ConditionalNumberPanel(document.getElementById("hp"), "playerHp");
const playerMana = new ConditionalNumberPanel(document.getElementById("mana"), "playerMana");
const playerEquipment = new ListPanelHandler(document.getElementById("equipment"), "playerEquipment", null);

//handles incoming and outgoing json packages from/to server
//connectionHandler
//parser (separate from connection)
//receives json describing character/room state, sends appropriate stuff to the different handlers

//managing player state: serverside
/**
 * Receives json data from connectionHandler and updates the appropriate panel.
 * Panel types (as labeled on backend):
 * -event
 * -room
 * -character
 */
const objectRouter = class {
    constructor(){
        this.panels = [];
    }

    addPanel(panel){
        this.panels.push(panel);
    }

    handleJson(serverJson) {
        const subJsons = this.splitServerJson(serverJson);
    }
    /**
     * Split the incoming json from the server into the subdivided jsons used on the front end.
     * The following are the subdivided json types:
     * -event
     * -roomDescription
     * -roomObjects
     * -roomCharacters
     * -playerInventory
     * -playerHp
     * -playerMana
     * -playerStatus
     * -playerEquipment
     * @param {string} json - string in a json format
     * @return {array} - array of jsons split into the above types
     */
    splitServerJson(json) {
        console.log(json);
    }
}

/**
 * Maintains connection to back end. When it receives JSON data from the server, it 
 * sends it to a connected objectRouter. When an input is entered, it is run through the
 * inputHandler before being passed to the server.
 */
const connectionHandler = class {
    constructor(){
        this.inputSocket = null;
        this.outputSocket = null;
        this.parser = new objectRouter();
        this.inputHandler = null;
        this.input = document.querySelector("input[type=text]");
    }

    sendCommand(evt) {
        const xhr = new XMLHttpRequest();
        xhr.open("GET", `${defaultURL}/command:${this.input.value.trim()}`);
        xhr.send();
        xhr.onload = () => {
            if (xhr.readState == 4 && xhr.status == 200) {
                const serverJson = xhr.response;
                console.log(serverJson);
                this.parser.splitServerJson(serverJson);
            } else {
                console.log(`Error: ${xhr.status}`)
            }
        }
        this.input.value = null;
    }
}

const connector = new connectionHandler();
const form = document.querySelector("form");
form.addEventListener("submit", (evt) => {
    evt.preventDefault();
    evt.stopPropagation();
    connector.sendCommand(evt);
}
);