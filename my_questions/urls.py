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
    path('delete_question_backend/', views.delete_question_backend, name='delete_question_backend'),
    path('delete_version/', views.version_delete_backend, name='version_delete_backend'),
    path('copy_version/', views.version_copy_backend, name='version_copy_backend'),
    path('edit_question_backend/', views.edit_question_backend, name='edit_question_backend'),
    path("question/<int:question_id>", views.question, name="question"),

    path('create_test/', views.create_test_view, name='create_test_view'),
    path('test_list/', views.test_list_view, name='test_list_view'),
    path('edit_test_backend/', views.edit_test_backend, name='edit_test_backend'),
    path('test_commit_backend/', views.test_commit_backend, name='test_commit_backend'),
    path('test_delete_backend/', views.test_delete_backend, name='test_delete_backend'),
    path('test/<int:test_id>', views.show_test_view, name='show_test_view'),
    path('edit_test/<int:test_id>', views.edit_test_view, name='edit_test_view'),
    path('save_comment_backend/', views.save_comment_backend, name='save_comment_backend'),
    path('save_rating_backend/', views.save_rating_backend, name='save_rating_backend'),
    path('save_is_answered_backend/', views.save_is_answered_backend, name='save_is_answered_backend'),

    path('testers/', views.testers_view, name='testers_view'),
    path('edit_tester/', views.edit_tester_backend, name='edit_tester_backend'),
    # Registration page
]