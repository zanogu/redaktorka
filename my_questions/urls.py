from django.urls import path

from . import views

app_name="my_questions"
urlpatterns = [
    path("", views.index, name="index"),
    path('home/', views.home_backend, name="home"),      # Home page
    path('login/', views.login_view, name='login_view'),    # Login page
    path('register/', views.register_page_view, name='register_page_view'),
    path('logout_me/', views.logout_backend, name='logout_me'),

    path('add_question/', views.add_question, name='add_question'),
    path('list/', views.questions_list_view, name='questions_list_view'),
    path('delete_question/', views.delete_question, name='delete_question'),
    path('edit_question/', views.edit_question, name='edit_question'),
    path('create_test/', views.create_test_view, name='create_test_view'),
    path('test_list/', views.test_list_view, name='test_list_view'),
    path('edit_test_backend/', views.edit_test_backend, name='edit_test_backend'),
    path('test_delete_backend/', views.test_delete_backend, name='test_delete_backend'),
    path('test/<int:test_id>', views.show_test_view, name='show_test_view'),
    path('testers/', views.testers_view, name='testers_view'),
    path('edit_tester/', views.edit_tester_backend, name='edit_tester_backend'),
    path("question/<int:question_id>", views.question, name="question")# Registration page
]