# -*- encoding: utf-8 -*-


from django.urls import path, re_path

from . import views

# from .views import AllKeywordsView

app_name='home'

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    path('reportform/', views.reportform, name='reportform'),
    path('submitted-report/<int:page>/', views.ReportsListView.as_view(), name='submitted'),
    
    path('submitted-report/view/<int:pk>', views.DetailView.as_view(), name='view'),
    
    path('profile/edit/<id>', views.edit_report, name='edit_profile'),
    path('profile/view/<int:pk>', views.DetailView.as_view(), name='view_profile'),
    path('profile/<int:page>/', views.ReportsListView.as_view(), name='profile'),
    ]
#     path(
#     "terms.json",
#     views.listing_api,
#     name="terms-api"
# ),
#     path("faux/",AllKeywordsView.as_view(template_name="home/test.html")),

