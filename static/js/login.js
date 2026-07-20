import {sendData} from "./sendData.js"
import {getCredentials} from "./getCredentials.js"

const emailElement = document.querySelector(".js-email");
const passwordElement = document.querySelector(".js-password");
const button = document.querySelector(".js-login-button");
const checkbox = document.querySelector(".remember-me-checkbox");
const resetElement = document.querySelector(".password-reset");
let rememberMe;

document.querySelector(".js-login-button").addEventListener("click", () => {

    checkbox.checked ? rememberMe = true : rememberMe = false;
    const [email, password] = getCredentials(".js-email", ".js-password");

    const user = {
        "email": email,
        "password": password,
        "rememberMe": rememberMe
    };
        
    // Send data to backend
    sendData("/api/login", user, "/");
});

[emailElement, passwordElement].forEach(element => {
    element.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {

            checkbox.checked ? rememberMe = true : rememberMe = false;
            const [email, password] = getCredentials(".js-email", ".js-password");

            const user = {
                "email": email,
                "password": password,
                "rememberMe": rememberMe
            };

            // Send data to backend
            sendData("/api/login", user, "/");
        }
    });
});


resetElement.addEventListener("click", async () => {

    const email = document.querySelector(".js-email").value;
    sessionStorage.setItem("resetEmail", email);

    resetElement.classList.add("reset-unresponsive");
    await sendData("/api/reset-email-sent", {email}, "/reset-email-sent")
    resetElement.classList.remove("reset-unresponsive");
});