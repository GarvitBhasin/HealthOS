import { sendData } from "./sendData.js";
import { getToken } from "./getToken.js";
import { getCredentials } from "./getCredentials.js";

const button = document.querySelector(".js-reset-button");
const passwordElement = document.querySelector("new-password");
const confirmElement = document.querySelector("confirm-password");

button.addEventListener("click", () => {

    const [password, confirmPassword] = getCredentials(".new-password", ".confirm-password");
    const token = getToken();

    const passwordObj = {
        pass: password, 
        confirmPass: confirmPassword,
        token: token
    };

    sendData("/api/reset-password", passwordObj, "/login");
});

[passwordElement, confirmElement].forEach(element => {
    element.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {

            const [password, confirmPassword] = getCredentials(".new-password", ".confirm-password");
            const token = getToken();

            const passwordObj = {
                pass: password, 
                confirmPass: confirmPassword,
                token: token
            }; 
        }
    });
});

