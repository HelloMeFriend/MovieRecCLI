import inquirer
from pathlib import Path

def display_menu():
    questions = [
        inquirer.List('choice',
                      message="Movie Recommendation System CLI Menu",
                      choices=[
                          ('Search Movie Recommendations', 'get_recommendations'),
                          ('Exit', 'exit')
                      ],
                      ),
    ]
    answers = inquirer.prompt(questions)
    return answers['choice']

def getfilePath()->str:
    questions = [
        inquirer.Path('file_path',
                      message="Where is the csv/excel file located?",
                      path_type=inquirer.Path.FILE)
    ]
    answers = inquirer.prompt(questions)
    return answers['file_path']
