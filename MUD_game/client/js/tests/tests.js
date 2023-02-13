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
     * @param {function} setUP - setup function to run before test
     * @param {function} tearDown - teardown function to run after test
     */
    runTest(func, params, expectedValue, setUp, tearDown){
        if (setUp) setUp();
        let testVal = null;
        if (this.object) {
            testVal = this.object[func](...params);
        } else {
            testVal = func(...params);
        }
        console.assert(expectedValue === testVal, `Got ${testVal} from ${func} with params ${params}, expected ${expectedValue}`);
        if (tearDown) tearDown();
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
     * @param {string} testName - optional parameter. Name of test to appear in console on fail.
     */
    domEditTest(func, params, expectedContainer, actualContainer, query, setUp, tearDown, checkStyle, testName) {
        //run setup
        if (setUp) setUp();
        //execute function
        this.runTest(func, params, undefined, null, null);
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
                `${testName}::Expected container contains ${expectedContainer.childNodes.length} elements while test Element contains ${nodes.length}`);
            return;
        }
        const testNodeList = [];
        nodes.forEach((node) => {testNodeList.push(node)});
        const correctNodeList = [];
        expectedContainer.childNodes.forEach((node) => {correctNodeList.push(node)});
        while (testNodeList.length > 0) {
            const testElement = testNodeList.shift();
            const expectedElement = correctNodeList.shift();
            if (testElement.childNodes.length > 0) {
                for (const node of testElement.childNodes) testNodeList.push(node);
            }
            if (expectedElement.childNodes.length > 0) {
                for (const node of expectedElement.childNodes) correctNodeList.push(node);
            }
            //compare all attributes of expectedElement
            for(const attribute of ["innerHTML", "outerHTML", "innerText"]) {
                console.assert(expectedElement[attribute] == testElement[attribute],
                    `${testName}::Expected ${attribute} value ${expectedElement[attribute]}, got ${testElement[attribute]}`);
            }
            if (checkStyle){
            //compare node style
            for (const styleAttribute of Object.keys(expectedElement.style)) {
                console.assert(expectedElement.style[styleAttribute] == testElement.style[styleAttribute],
                    `${testName}::Expected ${styleAttribute} value ${expectedElement.style[styleAttribute]}, got ${testElement.style[styleAttribute]}`);
            }
            }
        }

        if (tearDown) tearDown();
    }
}
const playerLogTest = new ListPanelHandler(document.getElementById("log"), 3);
const listPanelHandlerTests = new unitTest(playerLogTest, document.getElementById("log"));
const testLines = ["line 1", "line 2", "line 3"];
const createDivWithUl = (list, precedingText) => {
    const expectedDiv = document.createElement("div");
    if (precedingText) {
        expectedDiv.appendChild(document.createTextNode(precedingText));
    }
    const ul = document.createElement("ul");
    expectedDiv.appendChild(ul);
    for (const line of list) {
        const newItem = document.createElement("li");
        const newSpan = document.createElement("span");
        newSpan.appendChild(document.createTextNode(line));
        newItem.appendChild(newSpan);
        ul.appendChild(newItem);
    }
    return expectedDiv;
}

//Tests below this line---------------------------------------------------------------
listPanelHandlerTests.domEditTest(
    "addLine",
    [testLines[0]],
    createDivWithUl([testLines[0]], "log of stuff you've done"),
    document.getElementById("log"),
    null,
    null,
    () => {listPanelHandlerTests.object.clearText()},
    false,
    "addLineUnderLimitTest"
);
listPanelHandlerTests.domEditTest (
    "addLine",
    ["line4"],
    createDivWithUl([testLines[1], testLines[2], "line4"], "log of stuff you've done"),
    document.getElementById("log"),
    null,
    () => {
        for(const line of testLines) listPanelHandlerTests.object.addLine(line);
    },
    () => {listPanelHandlerTests.object.clearText()},
    false,
    "addLineOverLimitTest"
)
listPanelHandlerTests.runTest(
    "update",
    [],
    0,
    () => {
        for(const line of testLines) listPanelHandlerTests.object.addLine(line);
    },
    () => {listPanelHandlerTests.object.clearText()}
);