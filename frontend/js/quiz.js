// frontend/js/quiz.js

let questions = [];
let currentQuestion = 0;
let selectedAnswer = null;
let userAnswers = [];

async function startQuiz() {
    try {
        const response = await fetch('/api/quiz/questions');

        if (!response.ok) {
            throw new Error('Quiz questions could not be loaded');
        }

        const data = await response.json();

        questions = data.questions || [];

        if (questions.length === 0) {
            throw new Error('No quiz questions available');
        }

        currentQuestion = 0;
        userAnswers = [];

        document.getElementById('quizIntro').style.display = 'none';
        document.getElementById('quizContainer').style.display = 'block';
        document.getElementById('resultsContainer').style.display = 'none';

        showQuestion();

    } catch (error) {
        console.error('Quiz Error:', error);
        alert('Quiz load nahi ho paya. Backend check karo.');
    }
}


function showQuestion() {
    const question = questions[currentQuestion];

    if (!question) {
        return;
    }

    selectedAnswer = null;

    document.getElementById('questionNumber').textContent =
        `Question ${currentQuestion + 1}`;

    document.getElementById('progressText').textContent =
        `of ${questions.length}`;

    document.getElementById('questionText').textContent =
        question.question;

    const progress =
        ((currentQuestion + 1) / questions.length) * 100;

    document.getElementById('progressFill').style.width =
        `${progress}%`;

    const optionsContainer =
        document.getElementById('optionsContainer');

    optionsContainer.innerHTML = '';

    question.options.forEach((option, index) => {

        const button = document.createElement('button');

        button.className = 'option-button';
        button.type = 'button';

        button.textContent =
            `${String.fromCharCode(65 + index)}. ${option.label}`;

        button.addEventListener('click', () => {
            selectAnswer(option.value, button);
        });

        optionsContainer.appendChild(button);
    });

    document.getElementById('nextButton').style.display = 'none';

    document.getElementById('submitButton').style.display =
        currentQuestion === questions.length - 1
            ? 'none'
            : 'none';
}


function selectAnswer(value, button) {

    selectedAnswer = value;

    document.querySelectorAll('.option-button')
        .forEach(btn => btn.classList.remove('selected'));

    button.classList.add('selected');

    if (currentQuestion === questions.length - 1) {
        document.getElementById('submitButton').style.display =
            'inline-block';
    } else {
        document.getElementById('nextButton').style.display =
            'inline-block';
    }
}


function nextQuestion() {

    if (selectedAnswer === null) {
        alert('Pehle ek option select karo.');
        return;
    }

    userAnswers[currentQuestion] = selectedAnswer;

    currentQuestion++;

    showQuestion();
}


async function submitQuiz() {

    if (selectedAnswer === null) {
        alert('Pehle ek option select karo.');
        return;
    }

    userAnswers[currentQuestion] = selectedAnswer;

    try {

        const response = await fetch('/api/quiz/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                answers: userAnswers
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Quiz submission failed');
        }

        showResults(data);

    } catch (error) {

        console.error('Quiz submission error:', error);

        alert(
            'Quiz submit nahi ho paya: ' +
            error.message
        );
    }
}


function showResults(data) {

    document.getElementById('quizContainer').style.display =
        'none';

    document.getElementById('resultsContainer').style.display =
        'block';

    const score =
        data.score ?? data.result?.score ?? 0;

    const total =
        data.total ?? data.result?.total ?? questions.length;

    const percentage =
        data.percentage ??
        data.result?.percentage ??
        Math.round((score / total) * 100);

    document.getElementById('scoreNumberLarge').textContent =
        score;

    document.getElementById('totalQuestions').textContent =
        total;

    document.getElementById('scorePercentage').textContent =
        `${percentage}%`;

    let level = 'Beginner';

    if (percentage >= 90) {
        level = 'Expert';
    } else if (percentage >= 70) {
        level = 'Advanced';
    } else if (percentage >= 50) {
        level = 'Intermediate';
    }

    document.getElementById('scoreLevel').textContent =
        level;

    document.getElementById('scoreMessage').textContent =
        getScoreMessage(percentage);
}


function getScoreMessage(percentage) {

    if (percentage >= 90) {
        return 'Excellent phishing awareness!';
    }

    if (percentage >= 70) {
        return 'Good cybersecurity awareness.';
    }

    if (percentage >= 50) {
        return 'You have a basic understanding. Keep learning.';
    }

    return 'More practice is recommended.';
}


function reviewAnswers() {

    const container =
        document.getElementById('detailedResults');

    container.style.display = 'block';

    const review =
        document.getElementById('reviewContainer');

    review.innerHTML = '';

    questions.forEach((question, index) => {

        const userAnswer =
            userAnswers[index];

        const correctAnswer =
            question.correct_answer ??
            question.correctAnswer ??
            question.correct;

        const item =
            document.createElement('div');

        item.className = 'card';

        item.innerHTML = `
            <h3>Question ${index + 1}</h3>
            <p>${question.question}</p>
            <p><strong>Your Answer:</strong> ${
                userAnswer ?? 'Not answered'
            }</p>
            <p><strong>Correct Answer:</strong> ${
                correctAnswer ?? 'See explanation'
            }</p>
        `;

        review.appendChild(item);
    });
}


function retakeQuiz() {

    currentQuestion = 0;
    selectedAnswer = null;
    userAnswers = [];

    document.getElementById('resultsContainer').style.display =
        'none';

    document.getElementById('detailedResults').style.display =
        'none';

    document.getElementById('quizIntro').style.display =
        'block';
}