
document.getElementById('recommendationInput').addEventListener('submit', sendRecommendationData) // Attach sendData function to submit button
function sendRecommendationData(event) {

    event.preventDefault();

    let recommendationQuery = document.getElementById('recommendation-input').value; // Grab the form div

    console.log(recommendationQuery)

    fetch(`/recommend?data=${recommendationQuery}`, {
        method: 'GET'
    })
    .then(response => response.text())
    .then(html => 
        {
           const newPage = document.open('text/html', 'replace')
           newPage.write(html)
           newPage.close()
        })
    .catch(error => console.error(error));

    // fetch(`/recommend?data=${recommendationQuery}`, {
    //     method: 'POST',
    //     body: recommendationQuery
    // })
    // .then(response => response.text())
    // .then(html => 
    //     {
    //        const newPage = document.open('text/html', 'replace')
    //        newPage.write(html)
    //        newPage.close()
    //     })
    // .catch(error => console.error(error));
}