import {sendData} from "./sendData.js"

let email = "";
async function loadEmail() {
    const request = await fetch("/api/me");
    const response = await request.json();

    email = response.user_email;
    document.getElementById("user-email").innerHTML = email
}
await loadEmail();

sendData("/api/email-sent", {email}, "javascript:void(0);");

document.getElementById("resend-email").addEventListener("click", () => {
    sendData("/api/email-sent", {email}, "javascript:void(0);");
});