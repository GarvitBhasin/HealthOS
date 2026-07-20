// Check if user is authenticated
export async function checkAuthentication() {
    const button = document.querySelector(".account-loading-button");
    button.classList.add("loading");

    const request = await fetch("/api/me");
    const response = await request.json();
    const isVerified = response.is_verified;
    
    // Change nav buttons according to authentication state
    if (response.authenticated === false) {
        document.querySelector(".no-account-buttons").style.display = "block";
        document.querySelector(".my-account-button").style.display = "none";
        button.classList.remove("loading");
        
    } else {
        document.querySelector(".no-account-buttons").style.display = "none";
        document.querySelector(".my-account-button").style.display = "block";
        document.querySelector(".user-email").innerHTML = response.user_email;
        button.classList.remove("loading");
    }
    
    return isVerified;
}

const verified = checkAuthentication();
const themeButton = document.querySelector(".theme-toggle")

// Get and set saved theme (if any)
let savedTheme = localStorage.getItem("theme")
if (savedTheme == "dark") {
    themeButton.innerHTML = 
    `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="sun-icon" viewBox="0 0 16 16">
        <path d="M8 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6m0 1a4 4 0 1 0 0-8 4 4 0 0 0 0 8M8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0m0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13m8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5M3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8m10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0m-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0m9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707M4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708"/>
    </svg>`;
    document.body.classList.toggle("dark-mode");
}

// Listen for button click
themeButton.addEventListener("click", () => {

    // Light to dark
    if (themeButton.innerHTML.includes("moon-icon")) {
        themeButton.innerHTML = 
        `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="sun-icon" viewBox="0 0 16 16">
            <path d="M8 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6m0 1a4 4 0 1 0 0-8 4 4 0 0 0 0 8M8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0m0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13m8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5M3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8m10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0m-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0m9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707M4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708"/>
        </svg>`;
        document.body.classList.toggle("dark-mode");

        localStorage.setItem("theme", "dark");
    } 
    
    // Dark to light
    else {
        themeButton.innerHTML = 
        `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="moon-icon" viewBox="0 0 16 16">
            <path d="M6 .278a.77.77 0 0 1 .08.858 7.2 7.2 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277q.792-.001 1.533-.16a.79.79 0 0 1 .81.316.73.73 0 0 1-.031.893A8.35 8.35 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.75.75 0 0 1 6 .278M4.858 1.311A7.27 7.27 0 0 0 1.025 7.71c0 4.02 3.279 7.276 7.319 7.276a7.32 7.32 0 0 0 5.205-2.162q-.506.063-1.029.063c-4.61 0-8.343-3.714-8.343-8.29 0-1.167.242-2.278.681-3.286"/>
        </svg>`;
        document.body.classList.toggle("dark-mode");

        localStorage.setItem("theme", "light");
    }
});

// Send logout request
document.querySelector(".js-logout-button").addEventListener("click", () => {
    async function sendData() {
        const request = await fetch("/api/logout", {
            method: "POST"
        });
        if (request.ok) {
            window.location.href = "/";
        }

    }
    sendData()
    checkAuthentication();
});

// Nav responsiveness
const accountButton = document.querySelector(".my-account-button");
const dropdown = document.querySelector(".account-dropdown");
accountButton.addEventListener("click", () => {
    if (dropdown.style.display === "block") {
        dropdown.style.display = "none";
    } else {
        dropdown.style.display = "block";
    }
});