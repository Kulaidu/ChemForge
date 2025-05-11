document.addEventListener('DOMContentLoaded', function () {
    const questionContainers = document.querySelectorAll('.question-container');
    const totalQuestions = questionContainers.length;
    let isTestActive = true;
    let currentQuestion = 0;
    let score = 0;

    const progressBar = document.getElementById('quiz-progress');

    function updateProgress() {
        let progress = ((currentQuestion + 1) / totalQuestions) * 100;
        progressBar.style.width = `${progress}%`;
        progressBar.setAttribute('aria-valuenow', progress);
    }

    const subscriptFormula = (formula) => {
        return formula.replace(/(\d+)/g, '<sub>$1</sub>');
    };

    document.querySelectorAll('label[data-display]').forEach(label => {
        const originalFormula = label.getAttribute('data-display');
        label.innerHTML = subscriptFormula(originalFormula);
    });

    function showModal() {
        isTestActive = false;
        const testModal = new bootstrap.Modal(document.getElementById('testModal'));
        document.getElementById('modal-score').textContent = `${score}/${totalQuestions}`;
        testModal.show();
    }

    function showQuestion(index) {
        questionContainers.forEach((container, i) => {
            container.classList.toggle('hidden', i !== index);
        });
        resetQuestionState(index);
        updateProgress()
    }

    function resetQuestionState(questionIndex) {
        const form = document.getElementById(`test-form-${questionIndex}`);
        const feedbackContainer = document.getElementById(`feedback-${questionIndex}`);
        const submitButton = form.querySelector('.submit-answer');
        const nextButton = form.querySelector('.next-quest');

        if (feedbackContainer) {
            feedbackContainer.classList.add('hidden');
            feedbackContainer.querySelector('.error-message')?.classList.add('hidden');
            feedbackContainer.querySelector('.correct-message')?.classList.add('hidden');
        }

        const inputs = form.querySelectorAll('input[type="radio"]');
        inputs.forEach(input => {
            input.disabled = false;
            
            // Reset radio button and text input styles
            if (input.type === 'radio') {
                const label = form.querySelector(`label[for="${input.id}"]`);
                if (label) {
                    label.style.backgroundColor = '';
                    label.style.color = '';
                }
                input.checked = false;
            } else if (input.type === 'text') {
                input.value = '';
                input.style.backgroundColor = '';
                input.style.color = '';
            }
        });

        submitButton.hidden = false;
        nextButton.hidden = true;
    }
    
    /*
    function getElementCounts(formula) {
        const regex = /([A-Z][a-z]*)(\d*)/g;
        let match, elements = [];
    
        while ((match = regex.exec(formula)) !== null) {
            const element = match[1];
            const count = match[2] === "" ? 1 : parseInt(match[2]);  
            
            elements.push(count === 1 ? element : `${element}${count}`);
        }
    
        return elements;
    }

    function generatePermutations(elements) {
        const permutationsArray = [];
        function permute(arr, m = []) {
            if (arr.length === 0) {
                permutationsArray.push(m.join(""));
            } else {
                for (let i = 0; i < arr.length; i++) {
                    let newArr = arr.slice();
                    newArr.splice(i, 1);
                    permute(newArr, m.concat(arr[i]));
                }
            }
        }
        permute(elements);
        return permutationsArray;
    }
    */

    function validateAnswer(questionIndex) {
        const form = document.getElementById(`test-form-${questionIndex}`);
        const correctAnswer = form.querySelector('input[name="correct_answer"]').value.trim();
        const feedbackContainer = document.getElementById(`feedback-${questionIndex}`);
        const errorMessage = feedbackContainer.querySelector('.error-message');
        const correctMessage = feedbackContainer.querySelector('.correct-message');
        const incorrectAnswerSpan = feedbackContainer.querySelector('#incorrect-answer-' + questionIndex);

        const submitButton = form.querySelector('.submit-answer');
        const nextButton = form.querySelector('.next-quest');
        const resultButton = form.querySelector('.show-result');

        // Check input type and validate
        let userAnswerInput, userAnswer;
        const radioInputs = form.querySelectorAll('input[type="radio"]');
        const textInput = form.querySelector('input[type="text"][name="answer"]');

        if (radioInputs.length > 0) {
            // Radio button validation
            userAnswerInput = form.querySelector('input[type="radio"]:checked');
            if (!userAnswerInput) {
                // Highlight all radio button labels to indicate selection is required
                radioInputs.forEach(input => {
                    const label = form.querySelector(`label[for="${input.id}"]`);
                    label.style.border = '2px solid #ff6b6b';
                });
                return false;
            }
            userAnswer = userAnswerInput.value.trim();
        } else if (textInput) {
            // Text input validation
            userAnswer = textInput.value.trim();
            if (!userAnswer) {
                textInput.style.border = '2px solid #ff6b6b';
                return false;
            }
            userAnswerInput = textInput;
        } else {
            return false;
        }

        let isCorrect = userAnswer.trim().toLowerCase() === correctAnswer.trim().toLowerCase();
        
        /*
        if (document.querySelector('.mol3D')) {
            console.log("existing mol3D")
            const correctElements = getElementCounts(correctAnswer);
            const userElements = getElementCounts(userAnswer);
            const correctPermutations = generatePermutations(correctElements);
            const userPermutations = generatePermutations(userElements);
            isCorrect = correctPermutations.some(perm => userPermutations.includes(perm));
        } else {
            isCorrect = userAnswer === correctAnswer;
        }
        */

        // Display feedback
        feedbackContainer.classList.remove('hidden');
        errorMessage.classList.toggle('hidden', isCorrect);
        correctMessage.classList.toggle('hidden', !isCorrect);

        if (!isCorrect) {
            incorrectAnswerSpan.textContent = correctAnswer;
            
            // Style for incorrect answer
            if (userAnswerInput.type === 'radio') {
                const incorrectLabel = form.querySelector(`label[for="${userAnswerInput.id}"]`);
                const correctInput = form.querySelector(`input[type="radio"][value="${correctAnswer}"]`);
                const correctLabel = form.querySelector(`label[for="${correctInput.id}"]`);
                setTimeout(() => {
                    incorrectLabel.style.backgroundColor = '#ff6b6b';
                    incorrectLabel.style.color = 'white';
                    correctLabel.style.backgroundColor = 'rgb(132,220,198)';
                    correctLabel.style.color = 'white';
                }, 10);
            } else {
                userAnswerInput.style.backgroundColor = '#ff6b6b';
                userAnswerInput.style.color = 'white';
            }
        } else {
            // Style for correct answer
            if (userAnswerInput.type === 'radio') {
                const label = form.querySelector(`label[for="${userAnswerInput.id}"]`);
                setTimeout(() => {
                    label.style.backgroundColor = 'rgb(132,220,198)';
                    label.style.color = 'white';
                }, 10);
            } else {
                userAnswerInput.style.backgroundColor = 'rgb(132,220,198)';
                userAnswerInput.style.color = 'black';
            }
        }

        // Disable inputs after submission
        const inputs = form.querySelectorAll('input[type="radio"], input[type="text"]');
        inputs.forEach(input => {
            //console.log(`Disabling input: ${input.id || input.name}`);
            input.style.border = '';

            if (input.type === 'radio') {
                const label = form.querySelector(`label[for="${input.id}"]`);
                if (label) {
                    label.style.border = ''; // Reset label border
                    label.style.backgroundColor = ''; // Also reset background color if changed
                    label.style.color = ''; // Reset text color if changed
                }
            }

            input.disabled = true;
        });

        // Disable submit button
        submitButton.hidden = true;
        
        if (questionIndex === totalQuestions - 1) {
        // Last question
        nextButton.hidden = true;
        resultButton.hidden = false;
    } else {
        nextButton.hidden = false;
    }

        return isCorrect;
    }

    function setupQuestionNavigation() {
        const submitButtons = document.querySelectorAll('.submit-answer');
        const nextButtons = document.querySelectorAll('.next-quest');
        const resultButton = document.querySelector('.show-result');

        submitButtons.forEach((button, index) => {
            button.addEventListener('click', function(event) {
                event.preventDefault();
                const isCorrect = validateAnswer(index);
                
                if (isCorrect) {
                    score++;
                }
            });
        });
    
        nextButtons.forEach((button, index) => {
            button.addEventListener('click', function(event) {
                event.preventDefault();
                
                if (index < totalQuestions - 1) {
                    currentQuestion++;
                    showQuestion(currentQuestion);
                } else {
                    button.hidden = true;
                    const form = document.getElementById(`test-form-${index}`);
                    isTestActive = false;
                    resultButton.hidden = false;
                }
            });
        });

        resultButton.addEventListener('click', function(event) {
            event.preventDefault();
            showModal();
        });
    }

    function initTest() {
        setupQuestionNavigation();
        showQuestion(currentQuestion);
        updateProgress()
    }

    initTest();

    // Redirection Handle
    document.querySelectorAll(".nav-link, .navbar-brand").forEach(link => {
        link.addEventListener("click", function(event){
            let destination = this.href;

            if (isTestActive) {
                event.preventDefault();
                showRedirectModal(destination);
            }
        });
    });

    function showRedirectModal(destination){
        let redirectModal = new bootstrap.Modal(document.getElementById("redirectModal"));
        let confirmButton = document.getElementById("confirmRedirect");

        confirmButton.onclick = function () {
            isTestActive = false;
            window.location.href = destination;
        }

        redirectModal.show();
    }
});