import {sendData} from "./sendData.js"
import {getCredentials} from "./getCredentials.js"

// Get user's email and creation date
let email, creationDate;
async function checkAuthentication() {

    const button = document.querySelector(".loading-button");
    button.classList.add("loading");

    const request = await fetch("/api/me");
    const response = await request.json();

    email = response.user_email;
    sessionStorage.setItem("resetEmail", email);
    creationDate = response.creation_date;

    document.querySelector(".display-user-email").innerHTML =  `Email: ${email}`;
    document.querySelector(".display-creation-date").innerHTML =  `Created At: ${creationDate}`;
    document.querySelector(".display-verification").innerHTML =  `Verified: ${response.is_verified ? "Yes" : "No"}`;

    button.classList.remove("loading")
}
await checkAuthentication();

document.querySelector(".js-pwreset-button").addEventListener("click", () => {
    window.location.href = "/reset-email-sent";
});

// Delete email verification
const confirmationDialog = document.querySelector(".js-confirmation");
const verificationDialog = document.querySelector(".js-verification");

// Delete email dialog button listeners
document.querySelector(".js-delete-button").addEventListener("click", () => {
    confirmationDialog.showModal();
});

document.querySelector(".js-no-btn").addEventListener("click", () => {
    confirmationDialog.close();
});

document.querySelector(".js-yes-btn").addEventListener("click", () => {
    confirmationDialog.close();
    verificationDialog.showModal();
});

document.querySelector(".js-cancel-btn").addEventListener("click", () => {
    verificationDialog.close();
});

document.querySelector(".js-email-confirmation-button").addEventListener("click", () => {

    const [email, password] = getCredentials(".js-email-confirmation-input", ".js-password-confirmation-input")

    const user = {
        email: email,
        password: password
    };

    // Send credentials
    sendData("/api/delete", user, "/");
});

const emailElement = document.querySelector(".js-email-confirmation-input");
const passwordElement = document.querySelector(".js-password-confirmation-input");

[emailElement, passwordElement].forEach(element => {
    element.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            const [email, password] = getCredentials(".js-email-confirmation-input", ".js-password-confirmation-input");

            const user = {
                email: email,
                password: password
            };

            // Send credentials
            sendData("/api/delete", user, "/");
        }
    });
});