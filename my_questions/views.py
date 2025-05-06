from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
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
from django.urls import reverse

from .utils import Renderer
from pprint import pprint



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

# Adds new questions
@login_required
def add_question(request):

    if request.method != 'POST':
        return render(request, "my_questions/add_question.html",
                      {"add_question_form": AddQuestionForm()})
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

# Shows questions as list
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
                  {"quests": quests})

# Handles Question deletion dialog and deletion
@login_required
def delete_question_backend(request):
    if request.method != 'POST':
        return HttpResponseRedirect("404")

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

# Shows question and its versions editing form
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

# Handles question and its versions editing
@login_required
def edit_question_backend(request):
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

# Handles version deletion
@login_required
def version_delete_backend(request):
    if request.method != 'POST':
        print("not post")
        return HttpResponseRedirect("404")

    version_to_delete = get_object_or_404(Version, pk=request.POST.get('version_id'))
    question_id = version_to_delete.question_id

    if version_to_delete.question not in request.user.question_set.all():
        return HttpResponseRedirect("404")

    if request.POST.get('action') == 'delete':
        # Question is deleted here

        version_to_delete.delete()
        return redirect('my_questions:question', question_id=question_id)
    elif request.POST.get('action') == 'keep':
        return redirect('my_questions:question', question_id=question_id)
    else:

        return render(request,
               "my_questions/delete_version_approve.html",
               {"version_to_delete": version_to_delete}
               )

# Handles version duplication
@login_required
def version_copy_backend(request):
    if request.method != 'POST':
        print("not post")
        return HttpResponseRedirect("404")

    version_to_copy = get_object_or_404(Version, pk=request.POST.get('version_id'))
    question_id = version_to_copy.question_id

    if version_to_copy.question not in request.user.question_set.all():
        return HttpResponseRedirect("404")

    if request.POST.get('action') == 'copy':
        version_to_copy.pk = None
        version_to_copy.created = timezone.now()
        version_to_copy.save()
        return redirect('my_questions:question', question_id=question_id)
    else:
        return redirect('my_questions:question', question_id=question_id)

# TESTS

# Shows list of tests
@login_required
def test_list_view(request):
    tests = Test.objects.filter(user=request.user)
    return render(request,
                  "my_questions/test_list_view.html",
                  {"tests": tests})

# Handles test deletion
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

# Handles setting test as committed (set committed to True)
@login_required
def test_commit_backend(request):
    if request.method != 'POST':
        print("not post")
        return HttpResponseRedirect("404")

    test_to_commit = get_object_or_404(Test, pk=request.POST.get('test_id'))
    next_path = request.POST.get('next')
    if request.POST.get('next'):
        next_path = request.POST.get('next')
    else:
        next_path = reverse("my_question:test_list_view")

    if test_to_commit not in request.user.test_set.all():
        return HttpResponseRedirect("404")

    if request.POST.get('action') == 'commit':
        test_to_commit.committed = True
        test_to_commit.committed_datetime = timezone.now()
        test_to_commit.save()
        return redirect(next_path)
    elif request.POST.get('action') == 'keep':
        return redirect(next_path)
    else:
        return render(request,
               "my_questions/commit_test_approve.html",
               {"test_to_commit": test_to_commit,
                "next": next_path}
               )

# Shows the form for creating
# the questions and testers included in test
@login_required
def create_test_view(request):
    quests = request.user.question_set.all()
    testers = request.user.tester_set.all()
    if request.method != 'POST':
        return render(request,
                   "my_questions/edit_test.html",
                      {
                          'quests': quests,
                          'quests_tested':[],
                          'testers': testers,
                          'testers_tested':[],
                          'versions': [],
                          'versions_tested': []
                      }
                   )

# Shows the form for altering
# the questions and testers included in test
@login_required
def edit_test_view(request, test_id: int):
    test = get_object_or_404(Test, pk=test_id)


    if test not in request.user.test_set.all():
        return HttpResponseRedirect("404")

    quests_in_test = test.question.all().order_by('testquestion__order')
    quests_not_in_test = request.user.question_set.exclude(id__in=quests_in_test)
    quests_in_test_ready = [{"preview": q.version_set.latest('created'), "question": q} for q in quests_in_test]
    quests_not_in_test_ready = [{"preview": q.version_set.latest('created'), "question": q} for q in quests_not_in_test]
    testers_in_test = test.testers.all()
    testers_not_in_test = request.user.tester_set.exclude(id__in=testers_in_test)

    versions_in_test = test.version.all()

    if request.method != 'POST':
        return render(request,
                   "my_questions/edit_test.html",
                      {
                          'test':test,
                          'quests': quests_not_in_test,
                          'quests_tested':quests_in_test,
                          'testers': testers_not_in_test,
                          'testers_tested': testers_in_test,
                          'versions': [],
                          'versions_tested': versions_in_test
                      }
                   )

# Handles the form edit_test_view
@login_required
def edit_test_backend(request):

    print(request)

    if request.method == 'POST':
        request_post = dict(request.POST)
        print(request_post)

        with (transaction.atomic()):
            if request.POST.get("test-id") is not None:
                test = Test.objects.get(pk = request.POST.get("test-id"))
                test.name = request.POST.get("test-name")
                test.description = request.POST.get("test-description")
                test.date = timezone.now().date()
            else:
                test = Test(name = request.POST.get("test-name"),
                             description = request.POST.get("test-description"),
                             date = timezone.now().date(),
                             )
            test.save()
            test.user.add(request.user)

            test.question.clear()
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

            test.version.clear()
            for q in Question.objects.filter(
                    user=request.user,
                    pk__in=request.POST.getlist("question")
            ):
                versions = q.version_set.filter(pk__in=request.POST.getlist("version"))
                if len(versions) < 1:
                    versions = [q.version_set.latest("created")]
                a += versions

            test.version.set(a)

            test.testers.clear()
            for t in Tester.objects.filter(
                    user=request.user,
                    pk__in=request.POST.getlist("tester")
            ):
                t.test.add(test)

    return redirect("my_questions:test_list_view")

# Shows test in a readable form
# ready for testing and evaluation
# with relevant forms
@login_required
def show_test_view(request, test_id: int):
    test = get_object_or_404(Test, pk=test_id)
    test_dict = Renderer.test_to_list(test)
    print("Test dict", test_dict)
    return render(
       request,
       "my_questions/show_test_view.html",
       {
           "test": test,
           "test_dict": test_dict
       }
    )

# Handles saving version's editors comments
# from show_test_view AJAX
@login_required
def save_comment_backend(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            print(request.POST)
            form = EditVersionComment(request.POST)
            if form.is_valid():
                if form.cleaned_data != {}:
                    v = Version.objects.get(pk = int(request.POST.get("pk")))
                    v.editor_comments = request.POST.get("editor_comments")
                    v.save()
            return JsonResponse({'status': 'Success'})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')

# Handles saving question rating
# from show_test_view AJAX
@login_required
def save_rating_backend(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            test_question_record = get_object_or_404(
                TestQuestion,
                test_id=request.POST.get("test"),
                question_id=request.POST.get("question")
            )

            # Check if user is allowed to change the data
            if request.user not in test_question_record.question.user.all():
                print('Invalid request')
                return HttpResponseBadRequest('Invalid request')


            test_question_record.rating = request.POST.get("rating")

            try:
                test_question_record.save()
            except ValueError:
                test_question_record.rating = None
                test_question_record.save()

            return JsonResponse({'status': 'Success'})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')

# Handles saving how the team played
# (answered, not answered, etc)
# from show_test_view AJAX
@login_required
def save_is_answered_backend(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            test_question_record = get_object_or_404(
                TestQuestion,
                test_id=request.POST.get("test"),
                question_id=request.POST.get("question")
            )
            # Check if user is allowed to change the data
            if request.user not in test_question_record.question.user.all():
                print('Invalid request')
                return HttpResponseBadRequest('Invalid request')

            print(request.POST)

            test_question_record.is_answered = request.POST.get("is_answered")

            try:
                test_question_record.save()
            except ValueError:
                test_question_record.rating = None
                test_question_record.save()

            return JsonResponse({'status': 'Success'})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')

# TESTERS

# Shows list of testers with add/edit form
@login_required
def testers_view(request):
    testers = Tester.objects.filter(user = request.user)
    return render(request,
                  "my_questions/testers_view.html",
                  {"testers": testers,
                   "tester_form": EditTesterForm()})

# Handles add/edit form from testers_view
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