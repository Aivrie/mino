from flask import Flask, request, render_template, jsonify, json, redirect, url_for
from flask_caching import Cache
# import openai
from openai import OpenAI
import re
import requests
import os

# Load enviroment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Access enviroment variables
# OPEN_API_KEY = os.getenv('API_KEY')
brand_name = os.getenv('prompt_1')
product_url = os.getenv('prompt_2')

app = Flask(__name__)

# OpenAI Configure
client = OpenAI(
    # This is the default and can be omitted
    api_key='OPEN_API_KEY',

)

# Cache configuring
cache = Cache(app, config={
    'CACHE_TYPE': 'simple'
})


def check_url(text):
    url_pattern = re.compile(r'^https?://\S+$')
    return bool(url_pattern.match(text))


# Flask Routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/timeout")
def timeout():
    return render_template("timeout.html")


@app.route("/questions")
def questions():
    return render_template("questions.html")


@app.route('/review', methods=['POST', 'GET'])
def review():
    if request.method == 'GET':
        # query = request.args.get('data')
        try:
            cachedUserData = cache.get('userData')
            json_str = cachedUserData.decode('utf-8')
            dict_obj = json.loads(json_str)

            ethnicity = dict_obj['ethnicity'] # Accesses the key field in the dict object data
            complexion = dict_obj['comp']
            undertone = dict_obj['undertone']
            skinType = dict_obj['skin-type']
            coverage = dict_obj['coverageList'].replace(",", ", ")
            allergy = dict_obj['allergies']
            ingredients = dict_obj['ingredients']
            preference = dict_obj['prefList'].replace(",", ", ")

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
            return render_template('timeout.html')
        
    else:
        try:

            data = request.get_data() # Retrieves the raw data from the request
            cache.set('userData', data, timeout=3600) # Cache the data
            data_dict = json.loads(data) # Parses the JSON string into a dictionary
            ethnicity = data_dict['ethnicity'] # Accesses the key field in the JSON data
            complexion = data_dict['comp']
            undertone = data_dict['undertone']
            skinType = data_dict['skin-type']
            coverage = data_dict['coverageList'].replace(",", ", ")
            allergy = data_dict['allergies']
            ingredients = data_dict['ingredients']
            preference = data_dict['prefList'].replace(",", ", ")

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

    


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    
    if request.method == 'GET':
        query = request.args.get('data', 'defaultQuery')
        check_url(query)

        # cachedUserData = cache.get('userData')

        ''' Converting the bytes-object of form What format is this object; b'{"ethnicity":"Black / African-American","comp":"Medium","undertone":"Warm","skin-type":"Dry","coverage":"Light",
        "allergies":"No","ingredients":"","pref":"Cruelty-free","prefList":"SPF,Vegan,Cruelty-free","coverageList":"Light"}'  into a dict by decoding and then using json.loads()'''
    
        # json_str = cachedUserData.decode('utf-8')
        # dict_obj = json.loads(json_str)

        # ethnicity = dict_obj['ethnicity'] # Accesses the key field in the dict object data
        # complexion = dict_obj['comp']
        # undertone = dict_obj['undertone']
        # skinType = dict_obj['skin-type']
        # coverage = dict_obj['coverageList'].replace(",", ", ")
        # allergy = dict_obj['allergies']
        # ingredients = dict_obj['ingredients']
        # preference = dict_obj['prefList'].replace(",", ", ")

        # if check_url(query): 
        #     user_prompt = f"Please suggest the best {query} for an individual of {ethnicity} with a {complexion} complexion and {undertone} undertone. \
        #                     They have a {skinType} skin type and prefer the following coverage types: {coverage}. If {allergy} is 'Yes', kindly avoid recommending any \
        #                     products that contain the following allergens: {ingredients}. If there are no allergies, feel free to disregard {ingredients}. Additionally, \
        #                     ensure that your recommendations align with the following preferences: {preference}." 
        # else: 
        #     user_prompt = f"For an individual of {ethnicity} with a {complexion} complexion and {undertone} undertone, \
        #                     what is the best shade in this product line: {query}?"
            
        # recommendation = get_recommendations(user_prompt)
            
        return render_template("recommendation.html")


    

if __name__ == '__main__':
    app.run(debug=True)