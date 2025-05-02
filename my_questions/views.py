from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.utils import timezone
from django.forms.models import model_to_dict
from django.forms import modelformset_factory
from django.db import transaction

from .utils import Renderer


def index(request):
    return HttpResponse("Привет юзернейм, ты в редакторке")
# TODO rewrite

# LOGIN

# Define a view function for the home page
@login_required
def home_backend(request):
    return redirect("my_questions:questions_list_view")

@login_required
def logout_backend(request):
    logout(request)
    return redirect('my_questions:login_view')

# Define a view function for the login page
def login_view(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('../login/')

        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)

        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('my_questions:login_view')
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            return redirect('my_questions:home')

    # Render the login page template (GET request)
    return render(request, 'my_questions/login_group/login.html')
# TODO rewrite

def register_page_view(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)

        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('../register/')

        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )

        # Set the user's password and save the user object
        user.set_password(password)
        user.save()

        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect('my_questions:login_view')

    # Render the registration page template (GET request)
    return render(request, 'my_questions/login_group/register.html')
# TODO rewrite


# QUESTION

@login_required
def add_question(request):

    if request.method != 'POST':
        return render(request, "my_questions/add_question.html",
                      {"add_question_form": AddQuestionForm()})
    print(request.POST, request.FILES)
    form = AddQuestionForm(request.POST, request.FILES)

    if form.is_valid():
        with (transaction.atomic()):
            q = Question(created = timezone.now(), last_edited = timezone.now() )
            q.save()
            q.user.set([request.user])
            ver = form.save(commit=False)
            ver.question = q
            ver.created = timezone.now()
            ver.last_edited = timezone.now()
            q.save()
            form.save_m2m()
            ver.save()
            return redirect("my_questions:questions_list_view")
    else:
        return redirect("my_questions:homw")

    # incoming = request.POST.dict()

@login_required
def questions_list_view(request):
    # user = User.objects.filter(pk = request.user)
    quests = request.user.question_set.all()
    quests2 = []
    for q in quests:
        try:
            quests2.append(q.version_set.latest('created'))
        except Version.DoesNotExist:
            quests2.append(Version(text="нет версий", question = q))

    return render(request,
                  "my_questions/questions_list_view.html",
                  {"quests": quests2})

@login_required
def delete_question(request):
    if request.method != 'POST':
        return HttpResponseRedirect("404")

    print(request.POST.get('question_id'))
    question_to_delete = get_object_or_404(Question, pk = request.POST.get('question_id'))

    if question_to_delete not in request.user.question_set.all():
        return HttpResponseRedirect("404")

    if request.POST.get('action') == 'delete':
        # Question is deleted here
        question_to_delete.delete()
        return redirect('my_questions:questions_list_view')
    elif request.POST.get('action') == 'keep':
        return redirect('my_questions:questions_list_view')
    else:
        return render(request,
               "my_questions/delete_approve.html",
               {"question_to_delete": question_to_delete}
               )

@login_required
def question(request, question_id: int):
    my_question = get_object_or_404(Question, pk = question_id)

    if my_question not in request.user.question_set.all():
        return HttpResponseRedirect("404")

    formset = VersionFormSet(queryset = my_question.version_set.all())

    if request.method != 'POST':
        return render(request,
                   "my_questions/question.html",
                   {"my_question": my_question,
                            "version_set": my_question.version_set.all(),
                            "question_form_set": formset}
                   )

@login_required
def edit_question(request):
    formset = VersionFormSet(request.POST, request.FILES)
    my_question = get_object_or_404(Question, pk = int(request.POST.get("question")))

    if formset.is_valid():
        for form in formset:
            if form.cleaned_data !={}:
                instance = form.save(commit=False)
                if instance.created is None:
                    instance.created = timezone.now()
                instance.question = my_question
                instance.save()

    return redirect('my_questions:question', question_id = my_question.id)

# TESTS

@login_required
def test_list_view(request):
    tests = Test.objects.filter(user=request.user)
    for t in tests:
        print(t.version.all())
    return render(request,
                  "my_questions/test_list_view.html",
                  {"tests": tests})

@login_required
def test_delete_backend(request):
    if request.method != 'POST':
        print("not post")
        return HttpResponseRedirect("404")

    test_to_delete = get_object_or_404(Test, pk=request.POST.get('test_id'))

    if test_to_delete not in request.user.test_set.all():
        print(test_to_delete)
        print("not user", test_to_delete.user, request.user)
        return HttpResponseRedirect("404")

    if request.POST.get('action') == 'delete':
        # Question is deleted here
        test_to_delete.delete()
        return redirect('my_questions:test_list_view')
    elif request.POST.get('action') == 'keep':
        return redirect('my_questions:test_list_view')
    else:
        return render(request,
               "my_questions/delete_test_approve.html",
               {"test_to_delete": test_to_delete}
               )

@login_required
def create_test_view(request):
    quests = request.user.question_set.all()
    quests2 = [{"preview": q.version_set.latest('created'), "question": q} for q in quests]
    testers = request.user.tester_set.all()
    if request.method != 'POST':
        return render(request,
                   "my_questions/edit_test.html",
                      {
                          'quests': quests2,
                          'quests_tested':[],
                          'testers': testers,
                          'testers_tested':[],
                      }
                   )

@login_required
def edit_test_backend(request):
    if request.method == 'POST':
        request_post = dict(request.POST)
        print(request_post)

        with (transaction.atomic()):
            test = Test(name = request.POST.get("test-name"),
                         description = request.POST.get("test-description"),
                         date = timezone.now().date(),
                         )
            test.save()
            test.user.add(request.user)

            i = 0
            for q_id in request.POST.getlist("question"):
                q = Question.objects.get(pk=q_id, user=request.user)
                if q is not None:
                    qt = TestQuestion(
                        test = test,
                        question = q,
                        order = i
                    )
                    qt.save()
                    i += 1

            a = []
            for q in Question.objects.filter(
                    user=request.user,
                    pk__in=request.POST.getlist("question")
            ):
                a += q.version_set.filter(pk__in=request.POST.getlist("version"))

            test.version.set(a)

            for t in Tester.objects.filter(
                    user=request.user,
                    pk__in=request.POST.getlist("tester")
            ):
                t.test.add(test)

    return HttpResponse(request.POST)

@login_required
def show_test_view(request, test_id: int):
    test = get_object_or_404(Test, pk=test_id)
    test_dict = Renderer.test_to_list(test)

    return render(
       request,
       "my_questions/show_test_view.html",
       {
           "test": test,
           "test_dict": test_dict
       }
    )

# TESTERS

@login_required
def testers_view(request):
    testers = Tester.objects.filter(user = request.user)
    return render(request,
                  "my_questions/testers_view.html",
                  {"testers": testers,
                   "tester_form": EditTesterForm()})

@login_required
def edit_tester_backend(request):
    if request.method != 'POST':
        return HttpResponseRedirect("404")

    print(request.POST)
    tester_form = EditTesterForm(request.POST)
    if tester_form.is_valid():
        tester = tester_form.save(commit=False)
        if request.POST.get('id') and request.POST.get('id') != "":
            print("ID", request.POST.get('id'))
            tester.id = int(request.POST.get('id'))
        tester.save()
        tester.user.set([request.user])
        tester.save()

    return redirect("my_questions:testers_view")