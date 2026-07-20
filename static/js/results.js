async function loadResults() {
    try {
        const response = await fetch("/api/results");

        if (!response.ok) {
            throw new Error("Failed to load results");
        }

        const data = await response.json();
        const assessment = data.assessment;

        renderOverall(assessment);

        const categories = [
            "strength",
            "flexibility",
            "cardio",
            "nutrition",
            "recovery",
            "metabolic"
        ];

        categories.forEach(category => {
            renderCategory(category, assessment);
        });

    } catch (error) {
        console.error(error);

        document.querySelector(".HealthOS-score").textContent =
            "Unable to load results.";
    }
}

function renderOverall(assessment) {
    const scores = Object.values(assessment.scores);

    const overall = Math.round(
        scores.reduce((sum, score) => sum + score, 0) / scores.length
    );

    document.querySelector(".HealthOS-score").textContent =
        `${overall}%`;

    document.querySelector(".confidence").textContent =
        `${Math.round(assessment.confidence)}% confidence`;
}

function renderCategory(category, assessment) {
    const card = document.querySelector(
        `[data-category="${category}"]`
    );

    if (!card) return;

    const score = assessment.scores[category];
    const blindspots = assessment.blindspots[category] || [];
    const weaknesses = assessment.weaknesses[category] || [];

    card.querySelector(".category-score").textContent =
        `${Math.round(score)}%`;

    card.querySelector(".progress-fill").style.width =
        `${score}%`;

    card.querySelector(".blindspots").innerHTML =
        blindspots.length
            ? blindspots.map(item => `<div>• ${item}</div>`).join("")
            : "None identified";

    card.querySelector(".weaknesses").innerHTML =
        weaknesses.length
            ? weaknesses.map(item => `<div>• ${item}</div>`).join("")
            : "None identified";
}

loadResults();