# -*- encoding: utf-8 -*-


from django.urls import path, re_path

from apps.home import views
from .views import AllKeywordsView



urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    path('reportform/', views.reportform, name='reportform'),
    path('submitted-report/<int:page>/', views.submitted_form, name='submitted'),
    path('submitted-report/view/<id>', views.view_report, name='view'),
    path('submitted-report/edit/<id>', views.edit_report, name='edit'),
    path('profile/', views.profile, name='profile'),
    path(
    "terms.json",
    views.listing_api,
    name="terms-api"
),
    path("faux/",AllKeywordsView.as_view(template_name="home/test.html")),
]
