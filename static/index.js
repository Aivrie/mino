// Carousel controls
const myCarouselElement = document.querySelector('#quizSlider')
const carousel = new bootstrap.Carousel(myCarouselElement, {
  touch: false,
  wrap: false
})


let checkBoxDataPref
let checkBoxDataCoverage

document.getElementById('quizForm').addEventListener('submit', sendData) // Attach sendData function to submit button
function sendData(event) {
    event.preventDefault();

    let quiz = document.getElementById('quizForm'); // Grab the form div
    let quizData = new FormData(quiz) // Generate a FormData object which grabs all input elements

    // Group all checkBox values from the quizData FormData object and re-append them to the quizData FormData object
    checkBoxDataPref = quizData.getAll('pref')
    quizData.append('prefList', checkBoxDataPref) // Preferences
    checkBoxDataCoverage = quizData.getAll('coverage')
    quizData.append('coverageList', checkBoxDataCoverage) // Coverage


    // Send user data to localStorage
    const localData = localStorage.setItem('User Response', quizData)
    const quizDataJSON = {}

    for (const [key, value] of quizData.entries()) {
        quizDataJSON[key] = value;
    }
    const postData = { ...localData, ...quizDataJSON}

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





