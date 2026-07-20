import {sendData} from "./sendData.js"

document.addEventListener("DOMContentLoaded", async () => {

    // Get token from URL
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const token = urlParams.get('token');

    // Send token
    const request = await fetch(`/api/verify?token=${encodeURIComponent(token)}`, {
        method: "POST"
    });
    const response = await request.json();

    if (!request.ok) {
        document.querySelector(".error-message").style.display = "block";
        document.querySelector(".error-message").innerHTML = response.message;
        document.getElementById("loading").style.display = "none";
        document.getElementById("error-occurred").style.display = "block";
        return;
    }

    document.getElementById("loading").style.display = "none";
    document.getElementById("verification-successful").style.display = "block";

    setTimeout(() => {
        window.location.href = "/";
    }, 1550)

});