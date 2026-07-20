import {displaySuccess, displayError, hideMessages} from "./displayMessages.js"

export async function sendData(url, data, redirect_url) {

    // Change button to loading state
    const button = document.querySelector(".loading-button");
    button.classList.add("loading");

    hideMessages();

    // Send data to specified url
    try {
        const request = await fetch(`${url}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });
        const response = await request.json();

        // Display appropriate messages
        if (!request.ok) {
            displayError(response.message);
            button.classList.remove("loading");
            return
        }

        displaySuccess(response.message);
        button.classList.remove("loading");

        // Redirect
        window.location.href = `${redirect_url}`
    } 
    catch (error) {
        console.error(error);
    }
}