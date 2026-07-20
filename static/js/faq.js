const questions = document.querySelectorAll(".question");
const answers = document.querySelectorAll(".answer");
const arrows = document.querySelectorAll(".arrow");

questions.forEach((question, index) => {

    answers[index].style.display = "none";

    question.addEventListener("click", () => {
        if (answers[index].style.display == "none") {
            answers[index].style.display = "block";
            arrows[index].style.transform = "rotate(90deg)"
        } else {
            answers[index].style.display = "none";
            arrows[index].style.transform = "rotate(0deg)"
        }
    })
});