"use strict";

//build a state manager to handle incoming/outgoing messages from server
//server sends json describing what the page looks like
//state manager decodes json and updates panels as necessary
const PanelHandler = class {
    constructor(elem) {
        this.element = elem;
        //current text values of the bottom of the element.
        //All text should be in a span
        this.currentText = [];
        for (const textSpan of this.element.querySelectorAll("span")) {
            this.currentText.push(textSpan.innerText);
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
    constructor(elem, liLimit) {
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
    constructor(elem, current, max) {
        super(elem)
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

const playerLog = new ListPanelHandler(document.getElementById("log"), 50);
const roomObjects = new ListPanelHandler(document.getElementById("room-objects"), null);
const roomCharacters = new ListPanelHandler(document.getElementById("room-characters", null));
const playerInventory = new ListPanelHandler(document.getElementById("inventory"), 20);

//handles incoming and outgoing json packages from/to server
//connectionHandler
//parser (separate from connection)
//receives json describing character/room state, sends appropriate stuff to the different handlers

//managing player state: serverside

//receives command from input and processes or just sends to server?
