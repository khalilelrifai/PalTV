# -*- encoding: utf-8 -*-


from django.urls import path, re_path

from apps.home import views

# from .views import AllKeywordsView

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    path('reportform/', views.reportform, name='reportform'),
    path('submitted-report/<int:page>/', views.submitted_form, name='submitted'),
    path('submitted-report/view/<id>', views.view_report, name='view'),
    path('profile/edit/<id>', views.edit_report, name='edit_profile'),
    path('profile/view/<id>', views.view_report, name='view_profile'),
    path('profile/<int:page>/', views.profile, name='profile'),
    ]
#     path(
#     "terms.json",
#     views.listing_api,
#     name="terms-api"
# ),
#     path("faux/",AllKeywordsView.as_view(template_name="home/test.html")),

