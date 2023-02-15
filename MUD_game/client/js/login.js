const defaultURL = "127.0.0.1";
const defaultPort = 50000;
const login = (evt) => {
    const data = {};
    data["password"] = document.getElementById("password").value;
    data["characterName"] = document.getElementById("username").value;
    const xhr = new XMLHttpRequest();
    xhr.open("POST", defaultURL, true);
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.onreadystatechange = () => {
        if(xhr.readState == 4 && xhr.status == 200) {
            //update error boxes OR redirect to appropriate page
            console.log(xhr.response);
        }
    }
    xhr.send(JSON.stringify(data));
}

const printErrors = (jsonData) => {
    for(const id in jsonData) {
        const errorLabel = document.getElementById(id);
        errorLabel.innerText = null;
        for (const error in jsonData[id]) {
            errorLabel.appendChild(document.createTextNode(error + " "));
        }
    }
}

const form = document.querySelector("form");
form.addEventListener("submit", login);