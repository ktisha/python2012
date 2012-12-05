from django.db import models
from django.forms import ModelForm

class Author(models.Model):
    author_f = models.CharField('Surname', help_text = 'Author surname', max_length = 255)
    author_i = models.CharField('Name', help_text = 'Author name', max_length = 255)
    author_o = models.CharField('Middlename', help_text = 'Author middlename', max_length = 255)

    def __unicode__(self):
        return '%s %s %s' % (self.author_f, self.author_i, self.author_o)

class State(models.Model):
    state_title = models.CharField(max_length=255)

    def __unicode__(self):
        return self.state_title

class Book(models.Model):
    book_state = models.ForeignKey(State)
    book_title = models.CharField('Book title', help_text = 'Title of the book', max_length = 255)
    book_quantity = models.PositiveIntegerField('Book quantity', help_text = 'Quantity of the book')
    book_publishing = models.CharField('Book publishing', help_text = 'Publishing of the book', max_length = 255)
    book_year = models.PositiveIntegerField('Book publishing year', help_text = 'Publishing year of the book')
    book_type = models.CharField('Book type', help_text = 'Type of the book', max_length = 255)
    book_pages = models.PositiveIntegerField('Book pages number', help_text = 'Number of the book pages')
    book_language = models.CharField('Book language', help_text = 'Language of the book', max_length = 3)
    book_authors = models.ManyToManyField(Author)

    def __unicode__(self):
        return '%s, %s, %s' % (self.book_title, self.book_type, self.book_year)

class Faculty(models.Model):
    faculty_title = models.CharField('Title', help_text = 'Faculty title', max_length=255)

    def __unicode__(self):
        return self.faculty_title

class Department(models.Model):
    department_faculty = models.ForeignKey(Faculty)
    department_title = models.CharField('Title', help_text = 'Department title', max_length=255)

    def __unicode__(self):
        return self.department_title

class Team(models.Model):
    team_faculty = models.ForeignKey(Faculty)
    team_number = models.PositiveIntegerField('Number', help_text = 'Group number', max_length=4)

    def __unicode__(self):
        return '%i' % self.team_number

class Student(models.Model):
    student_team = models.ForeignKey(Team)
    student_f = models.CharField('Surname', help_text = 'Student surname', max_length=255)
    student_i = models.CharField('Name', help_text = 'Student name', max_length=255)
    student_o = models.CharField('Middlename', help_text = 'Student middlename', max_length=255)

    def __unicode__(self):
        return '%s %s %s' % (self.student_f, self.student_i, self.student_o)

class Issue(models.Model):
    issue_student = models.ForeignKey(Student)
    issue_book = models.ForeignKey(Book)
    issue_out = models.DateTimeField('Issue date', help_text = 'Date of the issue')
    issue_in = models.DateTimeField('Return date', help_text = 'Date when student must return book')

    def __unicode__(self):
        return '%s / %s / %s / %s' % (self.issue_student, self.issue_book, self.issue_in, self.issue_out)

class Teacher(models.Model):
    teacher_department = models.ForeignKey(Department)
    teacher_f = models.CharField('Surname', help_text = 'Teacher surname', max_length=255)
    teacher_i = models.CharField('Name', help_text = 'Teacher name', max_length=255)
    teacher_o = models.CharField('Middlename', help_text = 'Teacher middlename', max_length=255)

    def __unicode__(self):
        return '%s %s %s' % (self.teacher_f, self.teacher_i, self.teacher_o)

class AuthorForm(ModelForm):
    class Meta:
        model = Author

class StudentForm(ModelForm):
    class Meta:
        model = Student

class BookForm(ModelForm):
    class Meta:
        model = Book

class FacultyForm(ModelForm):
    class Meta:
        model = Faculty

class TeamForm(ModelForm):
    class Meta:
        model = Team

class DepartmentForm(ModelForm):
    class Meta:
        model = Department

class TeacherForm(ModelForm):
    class Meta:
        model = Teacher

class IssueForm(ModelForm):
    class Meta:
        model = Issue



