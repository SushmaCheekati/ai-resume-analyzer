from django.urls import path
from . import views


urlpatterns = [

    path('', views.welcome_page, name='welcome'),

    path('upload/', views.upload_resume, name='upload'),

    path('register/', views.register_user, name='register'),

    path('login/', views.login_user, name='login'),

    path('logout/', views.logout_user, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('download-report/', views.download_report, name='download_report'),

<<<<<<< HEAD
    path('download-pdf/<int:id>/', views.download_report, name='download_report_by_id'),

=======
>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487
    path('history/', views.history, name='history'),

    path('delete-resume/<int:id>/', views.delete_resume, name='delete_resume'),

    path('view-report/<int:id>/', views.view_report, name='view_report'),

<<<<<<< HEAD
=======
    path('logout/', views.logout_user, name='logout'),

>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487
    path('forgot-password/', views.forgot_password, name='forgot_password'),
]