import {sendData} from "./sendData.js"

const email = sessionStorage.getItem("resetEmail");
document.getElementById("user-email").innerHTML = email

document.addEventListener("DOMContentLoaded", () => {
    sendData("/api/reset-email-sent", {email}, "javascript:void(0);");
});

document.getElementById("resend-email").addEventListener("click", () => {
    sendData("/api/reset-email-sent", {email}, "javascript:void(0);");
});