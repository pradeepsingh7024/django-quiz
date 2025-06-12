import random
from django.core.management.base import BaseCommand
from api.models import QuestionPaper, Question

class Command(BaseCommand):
    help = 'Seed 100 logical reasoning MCQ questions'

    def handle(self, *args, **kwargs):
        paper, created = QuestionPaper.objects.get_or_create(title='Logical Reasoning Paper')

        questions_data = [
            ("Which number comes next in the series: 1, 3, 6, 10, 15, ?", ["21", "20", "22", "18"], "21"),
            ("Find the odd one out: Lion, Tiger, Leopard, Cow", ["Lion", "Tiger", "Leopard", "Cow"], "Cow"),
            ("If TABLE is coded as GZYOV, what is CHAIR in that code?", ["SXZRI", "XZRIS", "XZIRS", "XZRSI"], "XZIRS"),
            ("Which shape completes the pattern: Circle, Triangle, Square, Circle, Triangle, ?", ["Hexagon", "Square", "Circle", "Rectangle"], "Square"),
            ("Which number fits in the blank: 2, 6, 12, 20, 30, ?", ["36", "42", "44", "48"], "42"),
            ("Which of the following is a prime number?", ["39", "51", "53", "55"], "53"),
            ("If 'A' = 1, 'Z' = 26, what is the value of 'CAT'?", ["24", "27", "30", "29"], "24"),
            ("Which number does not belong in the series: 5, 10, 20, 25, 50, 100", ["5", "25", "50", "10"], "25"),
            ("How many sides does a regular hexagon have?", ["4", "5", "6", "8"], "6"),
            ("Find the missing letter: A, D, G, J, ?", ["K", "L", "M", "N"], "M"),
        ]

        # Duplicate to reach 100 questions
        questions_full = (questions_data * 10)[:100]

        for idx, (question_text, options, correct) in enumerate(questions_full):
            question = Question(
                paper=paper,
                question_text=f"Q{idx+1}. {question_text}",
                question_type='MCQ',
                option1=options[0],
                option2=options[1],
                option3=options[2],
                option4=options[3],
                correct_option=correct
            )
            question.save()

        self.stdout.write(self.style.SUCCESS('✅ Successfully seeded 100 logical reasoning questions'))
