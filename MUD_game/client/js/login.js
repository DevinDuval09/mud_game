const LOGIN = '/login';

const defaultURL = "127.0.0.1";
const defaultPort = 50000;
const login = (evt) => {
    evt.preventDefault()
    evt.stopPropagation()
    const raw_data = new FormData(document.querySelector("form"));
    console.log(raw_data.get("username"))
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = () => {
        if(xhr.readyState == 4 && xhr.status == 200) {
            //update error boxes OR redirect to appropriate page
            window.location.href = `http://${defaultURL}:${defaultPort}/`;
        }
    }
    xhr.open("POST", LOGIN);
    console.log(raw_data)
    xhr.send(raw_data);
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