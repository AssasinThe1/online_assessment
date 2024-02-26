import json
from django.core.management.base import BaseCommand
from assessment.models import Test, Question, Choice

class Command(BaseCommand):
    help = 'Load a list of questions from a JSON file'

    def handle(self, *args, **kwargs):
        with open('assessment/templates/assessment/questions.json', 'r') as file:
            data = json.load(file)
            for test_data in data:
                test, created = Test.objects.get_or_create(type_id=test_data['type_id'], defaults={'name': test_data['name']})

                for question_data in test_data['questions']:
                    question = Question.objects.create(test=test, text=question_data['text'])

                    for choice_data in question_data['choices']:
                        Choice.objects.create(question=question, text=choice_data['text'], is_correct=choice_data['is_correct'])

        self.stdout.write(self.style.SUCCESS('Successfully loaded cat questions'))
