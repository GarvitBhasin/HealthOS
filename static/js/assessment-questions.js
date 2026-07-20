import {sendData} from "./sendData.js"
import {checkAuthentication} from "./general.js"

async function checkVerification() {
    const isVerified = await checkAuthentication();
    if (!isVerified) {
        window.location.href = "/email-sent";
    }
}

checkVerification();

const sections = ["Physical Activity", "Body Composition", "Lifestyle", "Biometric Data", "Bloodwork"];

// Display all sections
    sections.forEach(section => {
    document.querySelector(".sections-container").innerHTML += `
        <div class="section">
            <div class="section-name" data-section="${section}">${section}</div>
            <div class="progress-bar" data-section="${section} Progress Bar"></div>
        </div>
    `
    });

// all questions and options with their corrosponding section and descriptions
// Initialize answers array 
let assessment = [];
let answers = []
async function loadAssessment() {
    const request = await fetch("/api/assessment-questions");
    assessment = await request.json();
    
    renderQuestion();

    assessment.forEach((section, i) => {
        answers[i] = new Array(section.questions.length);
    });
}

let currentSectionIndex = 0;
let currentQuestionIndex = 0;

// Render the first question
loadAssessment();

// Accept answer thruough number input
document.querySelector(".options").addEventListener("keydown", (event) => {

    if (event.target.classList.contains("numerical-option") && event.key === "Enter") {

        document.querySelector(".error-message").style.display = "none";
        
        const answer = Number(event.target.value);

        if (answer === 0) {
            document.querySelector(".error-message").style.display = "block";
            document.querySelector(".error-message").innerHTML = "Please enter a valid value.";
            return;
        }

        answers[currentSectionIndex][currentQuestionIndex] = answer;
        updateProgressSection();

        currentQuestionIndex++;

        renderQuestion();
    }

    console.log(answers);
});

// Update UI once an option is clicked
document.querySelector(".options").addEventListener("click", (event) => {

    if (!event.target.classList.contains("option")) {
        return;
    }

    // save answer 
    answers[currentSectionIndex][currentQuestionIndex] = Number(event.target.dataset.index);
    
    console.log(answers);
    
    updateProgressSection();

    // Submit assessment if last question is answered
    if (currentSectionIndex === assessment.length - 1 && currentQuestionIndex === assessment[assessment.length - 1].questions.length - 1) {
        currentSectionIndex++;
        document.querySelector(".completed-sections").innerHTML = `${currentSectionIndex} of ${sections.length} completed`;
        sendData("/api/submit", answers, "/results");
        return;
    }

    // Update the question and section we are on
    const amountOfQuestions = assessment[currentSectionIndex].questions.length;
    if (currentQuestionIndex === amountOfQuestions - 1) {
        currentSectionIndex++;
        currentQuestionIndex = 0;
    } else {
        currentQuestionIndex++;
    }

    // Update number of completed sections
    document.querySelector(".completed-sections").innerHTML = `${currentSectionIndex} of ${sections.length} completed`;

    renderQuestion();
});

// Update UI once back is clicked
document.querySelector(".back").addEventListener("click", () => {

    // Handle pressing back on first question
    if (currentQuestionIndex === 0 && currentSectionIndex === 0) {
        return;
    }
    
    // Update indexes
    let amountOfQuestions = assessment[currentSectionIndex].questions.length;
    if (currentQuestionIndex === 0) {
        currentSectionIndex--;
        amountOfQuestions = assessment[currentSectionIndex].questions.length;
        currentQuestionIndex = amountOfQuestions - 1;
    } else {
        currentQuestionIndex--;
    }
    
    // Update number of completed sections
    document.querySelector(".completed-sections").innerHTML = `${currentSectionIndex} of ${sections.length} completed`;
    
    updateProgressSection();
    renderQuestion();
});

function updateProgressSection() {

    // Make the section text we are on black font color
    document.querySelector(`[data-section="${sections[currentSectionIndex]}"]`).style.color = "black";

    // Update progress bar after question is answered
    const amountOfQuestions = assessment[currentSectionIndex].questions.length;
    const answeredQuestions = answers[currentSectionIndex].filter((answer) => {
        return answer !== undefined;
    }).length;
    const progress = (answeredQuestions / amountOfQuestions) * 100;
    document.querySelector(`[data-section="${sections[currentSectionIndex]} Progress Bar"]`).style.setProperty('--progress', `${progress}%`);
};

function renderQuestion() {

    // Extract current question, description and options
    let currentQuestion = assessment[currentSectionIndex].questions[currentQuestionIndex].question;
    let currentDescription = assessment[currentSectionIndex].questions[currentQuestionIndex].description;
    let currentOptions = assessment[currentSectionIndex].questions[currentQuestionIndex].options;

    // Clear previous options
    document.querySelector(".options").innerHTML = "";
    
    // Display current question, description and options
    document.querySelector(".question-heading").innerHTML = currentQuestion;
    document.querySelector(".question-description").innerHTML = currentDescription;

    if (assessment[currentSectionIndex].questions[currentQuestionIndex].type === "number") {
        document.querySelector(".options").innerHTML = `
            <input type="number" class="numerical-option">
        `;
    } else {
        currentOptions.forEach((option, index) => {
            document.querySelector(".options").innerHTML += `
                <div class="option" data-index="${index}">
                    ${option}
                </div>
            `;
        });
    }
}