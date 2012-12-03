__author__ = 'olya'
from library.models import *
from datetime import date

states = ['Exist',
          'Removed',
          'Planned']

authors = [['Ivanov', 'Ivan', 'Ivanovich'],
           ['Petrov', 'Petr', 'Petrovich'],
           ['Sidorov', 'Sidor', 'Sidorovich']]

faculties = ['Natural faculty',
             'Classical faculty']

books = [
    ['Exist', 'History', 100, 'Moscow', 1990, 'Theory', 321, 'Rus'],
    ['Exist', 'History', 100, 'Moscow', 1990, 'Practice', 128, 'Rus'],
    ['Exist', 'Physics', 200, 'SPb', 2005, 'Theory', 327, 'Rus'],
    ['Exist', 'Physics', 200, 'SPb', 2005, 'Practice', 97, 'Rus'],
    ['Exist', 'Chemistry', 150, 'Moscow', 2010, 'Theory', 467, 'Rus'],
    ['Exist', 'Chemistry', 150, 'Moscow', 2010, 'Practice', 234, 'Rus'],
    ['Exist', 'Biology', 250, 'SPb', 2012, 'Theory', 123, 'Rus'],
    ['Exist', 'Biology', 250, 'SPb', 2012, 'Practice', 70, 'Rus']]

departments = [['Natural faculty', 'Biology department'],
               ['Natural faculty', 'Physics department'],
               ['Natural faculty', 'Chemistry department'],
               ['Classical faculty', 'History department']]

teams = [['Natural faculty', 7301],
         ['Classical faculty', 7303]]

students = [[7301, 'Alexeev', 'Alexey', 'Alexeevich'],
            [7301, 'Alexandrov', 'Alexandr', 'Alexandrovich'],
            [7303, 'Sergeev', 'Sergey', 'Sergeevich'],
            [7303, 'Michailov', 'Michail', 'Michailovich']]

teachers = [['Biology department', 'Ivanov', 'Ivan', 'Ivanovich'],
            ['Physics department', 'Petrov', 'Petr', 'Petrovich'],
            ['History department', 'Sidorov', 'Sidor', 'Sidorovich']]

issues = [
    ['Alexeev', 321, date(2012, 10, 01), date(2012, 10, 15)],
    ['Alexeev', 128, date(2012, 10, 02), date(2012, 10, 16)],
    ['Alexandrov', 327, date(2012, 10, 03), date(2012, 10, 17)],
    ['Alexandrov', 97, date(2012, 10, 04), date(2012, 10, 18)],
    ['Sergeev', 467, date(2012, 10, 05), date(2012, 10, 19)],
    ['Sergeev', 234, date(2012, 10, 06), date(2012, 10, 20)],
    ['Michailov', 123, date(2012, 10, 07), date(2012, 10, 21)],
    ['Michailov', 70, date(2012, 10, 10), date(2012, 10, 23)]]


for state in states:
    s = State(state_title = state)
    s.save()

for author in authors:
    a = Author( author_f = author[0],
        author_i = author[1],
        author_o = author[2])
    a.save()

for faculty in faculties:
    f = Faculty(faculty_title = faculty)
    f.save()


for book in books:
    b = Book(book_state = State.objects.get(
        state_title = book[0]),
        book_title = book[1],
        book_quantity = book[2],
        book_publishing = book[3],
        book_year = book[4],
        book_type = book[5],
        book_pages = book[6],
        book_language = book[7])
    b.save()

for book in Book.objects.all():
    for author in Author.objects.all():
        b.book_authors.add(author)
    b.save()

for department in departments:
    d = Department(
        department_faculty = Faculty.objects.get(faculty_title = department[0]),
        department_title = department[1])
    d.save()

for team in teams:
    t = Team(
        team_faculty = Faculty.objects.get(faculty_title = team[0]),
        team_number = team[1])
    t.save()

for student in students:
    s = Student(
        student_team = Team.objects.get(team_number = student[0]),
        student_f = student[1],
        student_i = student[2],
        student_o = student[3])
    s.save()

for teacher in teachers:
    t = Teacher(
        teacher_department = Department.objects.get(department_title = teacher[0]),
        teacher_f = teacher[1],
        teacher_i = teacher[2],
        teacher_o = teacher[3])
    t.save()

for issue in issues:
    i = Issue(
        issue_student = Student.objects.get(student_f = issue[0]),
        issue_book = Book.objects.get(book_pages = issue[1]),
        issue_out = issue[2],
        issue_in = issue[3])
    i.save()
