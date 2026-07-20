import {sendData} from "./sendData.js"
import {getCredentials} from "./getCredentials.js"

const emailElement = document.querySelector(".js-email");
const passwordElement = document.querySelector(".js-password");
const button = document.querySelector(".js-signup-button");

button.addEventListener("click", () => {

    const [email, password] = getCredentials(".js-email", ".js-password");
    const creationDate = new Date().toLocaleDateString();

    const user = {
        email: email,
        password: password,
        creationDate: creationDate
    };

    // Send credentials to backend
    sendData("api/sign-up", user, "/email-sent");
});

[emailElement, passwordElement].forEach(element => {
    element.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {

            const [email, password] = getCredentials(".js-email", ".js-password");
            const creationDate = new Date().toLocaleDateString();

            const user = {
                email: email,
                password: password,
                creationDate: creationDate
            };

            // Send data to backend
            sendData("/api/sign-up", user, "/email-sent");
        }
    });
});