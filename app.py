from flask import Flask, request, render_template, jsonify, json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("questions.html")

@app.route("/recommendations")
def recommendations():
    return render_template("recommendation.html")

@app.route("/review")
def review():
    return render_template("review.html")

@app.route('/submit', methods=['POST'])
def submit():
    try:

        data = request.get_data() # Retrieves the raw data from the request
        data_dict = json.loads(data) # Parses the JSON string into a dictionary

        ethnicity = data_dict['ethnicity'] # Accesses the key field in the JSON data
        complexion = data_dict['comp']
        undertone = data_dict['undertone']
        skinType = data_dict['skin-type']
        coverage = data_dict['coverageList'].replace(",", ", ")
        allergy = data_dict['allergies']
        ingredients = data_dict['ingredients']
        preference = data_dict['prefList'].replace(",", ", ")

        # checkedValuesPref = []
        # for value in preference:
        #     checkedValuesPref.append(value)

        # checkedValuesCoverage = []
        # for value in coverage:
        #     checkedValuesCoverage.append(value)

        return render_template('review.html',
                userEthnicity=ethnicity,
                userComp=complexion,
                userUndertone=undertone,
                userSkinType=skinType,
                userCoverage=coverage,
                userAllergy=allergy,
                userIngredients=ingredients,
                userPref=preference)

    except Exception as e:
        result = {'status': 'error', 'message': str(e)}
        return jsonify(result), 500


if __name__ == '__main__':
    app.run(debug=True)