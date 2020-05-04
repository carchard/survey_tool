# Anonymous Survey Tool
This is a webapp that will generate a survey based off of an outline provided via a JSON schema. The webapp is extremely basic with minimal formatting and no database (hello local filesystem!). Each time the server is restarted, a new set of survey results will start to be collected.

This has been designed to collect no information about the results as they are submitted (such as IP addresses or the timestamp and order in which responses arrived at the server). The order of answers will be shuffled each time the results are published, although answers submitted in a single form will be kept together to help draw conclusions from the data (i.e. people who answered "yes" to question 1 tended to also answer "no" to question 3).

## Setting Up Surveys
A JSON file named "survey.json" must be placed in the top directory of this project prior to starting the server. This JSON file shall contain the following fields:
* "questions": a list of questions. Each question must take the form of a dictionary. This dictionary will be described later.
* "title": a string for the title of the survey.

The dictionary for each question will contain the following fields:
* "text": the question to be answered. This text will be printed above the field.
* "type": the type of field to generate. Options include: "short_answer", "long_answer", "long_answer_optional", "disagree_agree", "1-5", "1-10"

## Collecting Results
Results will be saved into a csv file that is created when the server starts. This CSV file will be placed in the top directory of the project and will include the data and timestamp that the server was started.

