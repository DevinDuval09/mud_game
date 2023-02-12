"use strict";

const unitTest = class {
    constructor(obj, elem) {
        this.object = obj;
        this.element = elem;
    }
    /**
     * Runs a test on a function that returns something that can be tested
     * @param {function or string} func - the function to call. If unitTests has an object attached, this should be a string, otherwise it should be a fucntion
     * @param {list} params - parameters to pass to the function 
     * @param {*} expectedValue - the expected result
     */
    runTest(func, params, expectedValue){
        let testVal = null;
        if (this.object) {
            testVal = this.object[func](...params);
        } else {
            testVal = func(...params);
        }
        console.assert(expectedValue === testVal, `Got ${testVal} from ${func.name} with params ${params}, expected ${expectedValue}`);
    }
    /**
     * Runs a test on a function that does not return any values, but edits the DOM
     * @param {function} func - function or string for method call
     * @param {list} params - parameters to pass to function
     * @param {Element} expectedContainer - HTML Element that is the expected result of function
     * @param {Element} actualContainer - the actual HTML Element that will be edited
     * @param {string} query - optional parameter. querySelectorAll string to narrow down the test elements in the actualContainer
     * @param {function} setUp - optional parameter. Function to run before executing function
     * @param {function} tearDown - optional parameter. Function to run to cleanup dom after running function
     * @param {boolean} checkStyle - optional parameter. Flag telling test whether or not to compare style
     */
    domEditTest(func, params, expectedContainer, actualContainer, query, setUp, tearDown, checkStyle) {
        //run setup
        if (setUp) setUp();
        //execute function
        this.runTest(func, params, undefined);
        //dom edit test
        let nodes = null;
        if (query) {
            nodes = actualContainer.querySelectorAll(query);
        } else {
            nodes = actualContainer.childNodes;
        }
        //compare node attributes
        if( nodes.length !== expectedContainer.childNodes.length) {
            console.assert(true == false,
                `Expected container contains ${expectedContainer.childNodes.length} elements while test Element contains ${nodes.length}`);
            return;
        }
        for (let i = 0; i < nodes.length; i++) {
            const testElement = nodes[i];
            const expectedElement = expectedContainer.childNodes[i];
            //compare all attributes of expectedElement
            for(const attribute of Object.keys(expectedElement)) {
                console.assert(expectedElement[attribute] == testElement[attribute],
                    `Expected ${attribute} value ${expectedElement[attribute]}, got ${testElement[attribute]}`);
            }
            if (checkStyle){
            //compare node style
            for (const styleAttribute of Object.keys(expectedElement.style)) {
                console.assert(expectedElement.style[styleAttribute] == testElement.style[styleAttribute],
                    `Expected ${styleAttribute} value ${expectedElement.style[styleAttribute]}, got ${testElement.style[styleAttribute]}`);
            }
            }
        }

        if (tearDown) tearDown();
    }

    clearContainer() {
        for(const node of this.element.childNodes) {
            this.element.removeChild(node);
        }
        this.element.innerText = null;
    }
}

const playerLogTest = new ListPanelHandler(document.getElementById("log"), 50);
const listPanelHandlerTests = new unitTest(playerLogTest, document.getElementById("log"));
const testLines = ["line 1", "line 2", "line 3"];
const createDivWithUl = (list, precedingText) => {
    const expectedDiv = document.createElement("div");
    if (precedingText) {
        expectedDiv.appendChild(document.createTextNode(precedingText));
    }
    expectedDiv.appendChild(document.createElement("ul"));
    for (const line of list) {
        const newItem = document.createElement("li");
        const newSpan = document.createElement("span");
        newItem.appendChild(newSpan.appendChild(document.createTextNode(line)));
    }
    return expectedDiv;
}
listPanelHandlerTests.domEditTest(
    "addLine",
    [testLines[0]],
    createDivWithUl([testLines[0]], "log of stuff you've done"),
    document.getElementById("log"),
    null,
    null,
    () => {listPanelHandlerTests.clearContainer()},
    false
);