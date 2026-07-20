export function displaySuccess(message) {
    document.querySelector(".success-message").style.display = "block";
    document.querySelector(".success-message").innerHTML = message;
}

export function displayError(message) {
    document.querySelector(".error-message").style.display = "block";
    document.querySelector(".error-message").innerHTML = message;
}

export function hideMessages() {
    document.querySelector(".success-message").style.display = "none";
    document.querySelector(".error-message").style.display = "none";
}