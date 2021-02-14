# covid_results

COVID-19 analysis by Davide Aronadio.

&nbsp;

To run and test the API, please run the following:

1. Run the Flask app by executing the `run_flask_app` batch file:

      ```
      python C:/your/local/path/code/aro_app.py
      ```

2. Once the Flask app is running, test the API by running:

      ```
      python C:/your/local/path/code/api_test.py ^
      --url http://127.0.0.1:5000 ^
      --field country ^
      --value DK
      ```
      > N.B. Available country values: DK, DE, SE, RO, ES.
