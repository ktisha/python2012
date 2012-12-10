from django.shortcuts import render_to_response
from models import BookForm, FacultyForm, TeamForm, DepartmentForm, TeacherForm, StudentForm, AuthorForm, IssueForm
from models import Book, Faculty, Team, Department, Teacher, Student, Author, Issue
from django.template import RequestContext
from datetime import timedelta, date

def hello(request):
    return render_to_response('base.html')

def issue_list(request):
    variables = RequestContext(request, {
        'forms': Issue.objects.all()
    })
    return render_to_response('crud/issues/issue_list.html', variables)

def issue_add(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('common/success.html')
    else:
        issue = Issue(issue_out=date.today(), issue_in=date.today()+timedelta(days=10))
        form = IssueForm(instance=issue)

    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response('crud/issues/issue_add.html', variables)

def issue_remove(request, id):
    Issue.objects.get(pk=id).delete()
    return render_to_response('common/success.html')

def issue_edit(request, id):
    issue = Issue.objects.get(pk=id)
    if request.method == "POST":
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            return render_to_response('common/success.html')
    else:
        form  = IssueForm(instance=issue)

    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response("crud/issues/issue_edit.html", variables)



def book_list(request):
    variables = RequestContext(request, {
        'forms': Book.objects.all()
    })
    return render_to_response('crud/book/book_list.html', variables)

def book_add(request):
    if request.method is 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('common/success.html')
    else:
        form = BookForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('crud/book/book_add.html', variables)

def book_remove(request, id):
    Book.objects.get(pk=id).delete()
    return render_to_response('common/success.html')

def book_edit(request, id):
    book = Book.objects.get(pk=id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return render_to_response('common/success.html')
    else:
        form  = BookForm(instance=book)

    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response("crud/book/book_edit.html", variables)

def faculty_list(request):
    variables = RequestContext(request, {
        'forms': Faculty.objects.all()
    })
    return render_to_response('crud/faculty/faculty_list.html', variables)

def faculty_add(request):
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('common/success.html')
    else:
        form = FacultyForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('crud/faculty/faculty_add.html', variables)

def faculty_edit(request, id):
    faculty = Faculty.objects.get(pk=id)
    if request.method == "POST":
        form = FacultyForm(request.POST, instance=faculty)
        if form.is_valid():
            form.save()
            return render_to_response('common/success.html')
    else:
        form  = FacultyForm(instance=faculty)

    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response("crud/faculty/faculty_edit.html", variables)

def faculty_remove(request, id):
    Faculty.objects.get(pk=id).delete()
    return render_to_response('common/success.html')

def group_list(request):
    variables = RequestContext(request, {
        'forms': Team.objects.all()
    })
    return render_to_response('crud/group/group_list.html', variables)

def group_add(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('common/success.html')
    else:
        form = TeamForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('crud/group/group_add.html', variables)

def group_edit(request, id):
    team = Team.objects.get(pk=id)
    if request.method == "POST":
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return render_to_response('common/success.html')
    else:
        form  = TeamForm(instance=team)

    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response("crud/group/group_edit.html", variables)

def group_remove(request, id):
    Team.objects.get(pk=id).delete()
    return render_to_response('common/success.html')

def department_list(request):
    variables = RequestContext(request, {
        'forms': Department.objects.all()
    })
    return render_to_response('crud/department/department_list.html', variables)

def department_add(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('common/success.html')
    else:
        form = DepartmentForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('crud/department/department_add.html', variables)

def department_edit(request, id):
    department = Department.objects.get(pk=id)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return render_to_response('common/success.html')
    else:
        form  = DepartmentForm(instance=department)

    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response("crud/book/department_edit.html", variables)

def department_remove(request, id):
    Department.objects.get(pk=id).delete()
    return render_to_response('common/success.html')

def teacher_list(request):
    variables = RequestContext(request, {
        'forms': Teacher.objects.all()
    })
    return render_to_response('crud/teacher/teacher_list.html', variables)

def teacher_add(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('common/success.html')
    else:
        form = TeacherForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('crud/teacher/teacher_add.html', variables)

def teacher_edit(request, id):
    teacher = Teacher.objects.get(pk=id)
    if request.method == "POST":
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return render_to_response('common/success.html')
    else:
        form  = TeacherForm(instance=teacher)

    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response("crud/teacher/teacher_edit.html", variables)

def teacher_remove(request, id):
    Teacher.objects.get(pk=id).delete()
    return render_to_response('common/success.html')

def student_list(request):
    variables = RequestContext(request, {
        'forms': Student.objects.all()
    })
    return render_to_response('crud/student/student_list.html', variables)

def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('common/success.html')
    else:
        form = StudentForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('crud/student/student_add.html', variables)

def student_edit(request, id):
    student = Student.objects.get(pk=id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return render_to_response('common/success.html')
    else:
        form  = StudentForm(instance=student)

    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response("crud/student/student_edit.html", variables)

def student_remove(request, id):
    Student.objects.get(pk=id).delete()
    return render_to_response('common/success.html')

def author_list(request):
    variables = RequestContext(request, {
        'forms': Author.objects.all()
    })
    return render_to_response('crud/author/author_list.html', variables)

def author_add(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('common/success.html')
    else:
        form = AuthorForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('crud/author/author_add.html', variables)

def author_edit(request, id):
    author = Author.objects.get(pk=id)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return render_to_response('common/success.html')
    else:
        form  = AuthorForm(instance=author)

    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response("crud/author/author_edit.html", variables)

def author_remove(request, id):
    Author.objects.get(pk=id).delete()
    return render_to_response('common/success.html')