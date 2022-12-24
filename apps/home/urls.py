# -*- encoding: utf-8 -*-


from django.urls import path, re_path

from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    path('reportform/', views.reportform, name='reportform'),
    path('submitted-report/', views.submitted_form, name='submitted'),
    path('submitted-report/details/<id>', views.view_report, name='view')

]
