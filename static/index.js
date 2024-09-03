// Carousel controls
const myCarouselElement = document.querySelector('#quizSlider')
const carousel = new bootstrap.Carousel(myCarouselElement, {
  touch: false,
  wrap: false
})



document.getElementById('quizForm').addEventListener('submit', sendData) // Attach sendData function to submit button

let checkBoxDataPref
let checkBoxDataCoverage

// Quiz Submission
function sendData(event) {
    event.preventDefault();


        // Grab form div and generate a formData object to collect all input elements
    let quiz = document.getElementById('quizForm');
    let quizData = new FormData(quiz)

    

        // Group all checkBox values from the quizData FormData object and re-append them to the quizData FormData object
    checkBoxDataPref = quizData.getAll('pref')
    quizData.append('prefList', checkBoxDataPref) // Preferences
    checkBoxDataCoverage = quizData.getAll('coverage')
    quizData.append('coverageList', checkBoxDataCoverage) // Coverage



        // Send user data to localStorage
    const localData = localStorage.setItem('User Response', quizData)
    const quizDataJSON = {}


        // Send localStorage data and quizData to postData object
    for (const [key, value] of quizData.entries()) {
        quizDataJSON[key] = value;
    }
    const postData = { ...localData, ...quizDataJSON}


        // FetchAPI for 'submit' - Quiz submission
    fetch('/submit', {
        method: 'POST',
        body: JSON.stringify(postData),
        headers: {'Content-type': 'application/json'}
    })
    .then(response => response.text())
    .then(html => 
    {
       const newPage = document.open('text/html', 'replace')
       newPage.write(html)
       newPage.close()
    }
    )
    .catch(error => console.log(error));

}


    // Prevent Empty Submission for each quix question
// const questions = document.querySelectorAll('input')
const nextBtns = document.querySelectorAll('.page-button')
const activeSlide = myCarouselElement.querySelector('.active')
const inputs = activeSlide.querySelectorAll('input, select, textarea');


nextBtns.forEach(btn => {


    btn.removeAttribute('data-bs-slide');
    

    inputs.forEach(input => {
        input.addEventListener('change', () => {
            if (input.checked) {
                btn.setAttribute('data-bs-slide', 'next');
            }
        }
        );
    });


    btn.addEventListener('click', () => {
        if (!Array.from(inputs).some(q => q.checked)) {
            alert('Please select an option.');
            return;
        }
        // else {
        //     location.reload()

        // }
    });


});


    // Product Preference Disable Functionality
/**
 * If user selects 'No preference' (checked) - Disable all other options
 * If user selects any other check box - Disable 'No preference' option
 */
const pdtPrefList = document.querySelectorAll('input[name="pref"]')
const noPref = document.getElementById('no-pref')

for (const checkElement of pdtPrefList) {
    checkElement.addEventListener('change', disableCheck)
}

function disableCheck(event) {
    event.preventDefault();

    switch(this.id) {
        case "no-pref":
            inputElement.forEach(elem => {
                elem.disabled=true
            });
            break
        default:
            noPref.disabled=true
    }
}


    // Skin Allergies Disable Functionality
/**
 * If user selects 'No' (checked) - Disable textarea element
 * If user selects 'Yes' allow textarea to show
 */
const allergyChoice = document.querySelectorAll('input[name="allergies"]')
const allergenText = document.getElementById('allergenList')

for (const choiceElement of allergyChoice) {
    choiceElement.addEventListener('change', disableInput)
}

function disableInput(event) {
    event.preventDefault();

    if(this.id === "no") {
        allergenText.setAttribute('readonly', true)
        allergenText.value="I have no allergens"
        allergenText.setAttribute('style', 'color: grey')
    }
    else {
        allergenText.removeAttribute('readonly')
    }
}






