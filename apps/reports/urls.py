


from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views.generic.base import TemplateView

from . import views


app_name='reports'

urlpatterns = [


    path('', TemplateView.as_view(template_name='reports/main.html'), name='main'),
    path('create_report/',views.CreateReport.as_view(),name='create_report'),
]
    # # Matches any html file
    # path('reportform/', views.reportform, name='reportform'),
    # path('submitted-report/<int:page>/',login_required(views.ReportsListView.as_view()), name='submitted'),
    
    # path('submitted-report/view/<int:pk>', login_required(views.DetailView.as_view()), name='view'),
    
    # path('profile/edit/<id>', views.edit_report, name='edit_profile'),
    # path('profile/view/<int:pk>', login_required(views.DetailView.as_view()), name='view_profile'),
    # path('profile/<int:page>/', login_required(views.ReportsListView.as_view()), name='profile'),
    # path('all/', login_required(views.ReportsListView.as_view()), name='all'),
    # ]
#     path(
#     "terms.json",
#     views.listing_api,
#     name="terms-api"
# ),
#     path("faux/",AllKeywordsView.as_view(template_name="home/test.html")),
