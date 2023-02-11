"use strict";

//build a state manager to handle incoming/outgoing messages from server
//server sends json describing what the page looks like
//state manager decodes json and updates panels as necessary
const PanelHandler = class ElementHandler {
    constructor(element) {
        this.element = element;
        //current text values of the bottom of the element.
        //All text should be in a span
        this.currentText = [];
        for (const textSpan of this.element.querySelectorAll("span")) {
            this.currentText.push(textSpan.innerText);
        }
    }
    isUpToDate = (textArray) => {
        if (this.currentText.length !== textArray.length) return false;
        for (let i = 0; i < this.currentText.length; ++i) {
            if (textArray[i] != this.currentText[i]) return false;
        }
        return true;
    }
}

const ListPanelHandler = class extends PanelHandler {
    constructor(element, liLimit) {
        super(element);
        this.list = this.element.querySelector("ul");
        this.maxLines = liLimit;
    }

    update(text) {
        let liList = this.list.querySelectorAll("li");
        //check list size against maxLines
        if (liList && this.maxLines && liList.length == this.maxLines) {
            //if maxLines has been reached, remove las item from current text
            //later, currentText will be used to repopulate all the list items
            this.currentText.pop();
        } else {
            //if maxLines has not been reached, add another list item and refresh liList
            this.list.appendChild(document.createElement("li"));
            liList = this.list.querySelectorAll("li");
        }
        this.currentText.push(text);
        while (this.list.children.length > this.currentTex) {
            this.list.removeChild(this.list.children.item(0));
        }
        liList = this.list.querySelectorAll("li");
        for (let i = 0; i < liList.length; ++i) {
            //for each item in currentText, add it to a span and put it into an li
            const newSpan = document.createElement("span");
            newSpan.appendChild(document.createTextNode(this.currentText[i]));
            liList[i].appendChild(newSpan);
        }
    }
}

const playerLog = new ListPanelHandler(document.getElementById("log"), 50);
const roomObjects = new ListPanelHandler(document.getElementById("room-objects"), null);
const roomCharacters = new ListPanelHandler(document.getElementById("room-characters", null));
const playerInventory = new ListPanelHandler(document.getElementById("inventory"), 20);