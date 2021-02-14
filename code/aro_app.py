import flask
from flask import request, jsonify, abort
import json
import pandas as pd
import datetime

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def preprocess(input):
    
    test = pd.read_csv(input)

    country_cond = test['country'].isin(["Denmark", "Germany", "Romania", "Spain", "Sweden"])
    level_cond = test['level'] == 'national'

    test = (
        test[country_cond & level_cond]
        .drop(['level', 'region_name'], axis = 1)
    )

    test['date'] = test.apply(lambda x: datetime.datetime.strptime(x['year_week'] + '-1', "%Y-W%W-%w"), axis=1)
    test['month'] = test.apply(lambda x: x.date.month, axis = 1)
    test = test.drop('date', axis = 1)

    year_cond = test.year_week.str.startswith('2020')
    test = test[year_cond]

    list_year_week = test['year_week'].str.split('-W')
    test['year'] = [elem[0] for elem in list_year_week]

    # Monthly aggregation
    agg_df = (
        test
        .groupby(['year','month', 'country', 'country_code'])
        .agg({'new_cases': 'sum', 'tests_done': 'sum', 'population': 'mean'})
        .reset_index()
    )

    agg_df['testing_rate'] = agg_df['tests_done'] / agg_df['population'] * 100
    agg_df['positivity_rate'] = agg_df['new_cases'] / agg_df['tests_done'] * 100
    agg_df['year_month'] = agg_df['year'] + '-' + agg_df['month'].astype('str')
    agg_df['country'] = agg_df['country_code']

    # Data quality filtering
    agg_df = agg_df[agg_df['positivity_rate'] <= 100]

    final = agg_df[['year', 'month', 'country', 'positivity_rate', 'testing_rate']].to_json(orient='records')
    
    return json.loads(final)


# Preprocess input data
results = preprocess('C:/Users/david/Downloads/covid_testing_data.csv')




@app.route('/', methods=['GET'])
def home():
    return 'COVID-19 data analysis: API testing by Davide Aronadio.'



@app.route('/api/v1/country_test_done/all', methods=['GET'])
def api_all():
    return jsonify(results)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404



@app.route('/api/v1/country_test_done', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.

    if 'country' in request.args:
        country = request.args['country']
        unique_countries = {elem['country'] for elem in results}

        if country not in unique_countries:
            abort(404, description=f"The requested country ({country}) is not in the dataset, or the request is malformed. Please use ISO 3166-1 alpha-2 standard and try one of the following: {unique_countries}.")
    else:
        abort(404, description = "No country code provided. Please specify a country code.")


    # Create an empty list for our results
    output = []


    # Loop through the data and match results that fit the requested ID.
    # Country codes are unique, but other fields might return many results
    for element in results:
        if element['country'] == country:
            output.append(element)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(output), 200

app.run()