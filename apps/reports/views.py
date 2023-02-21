from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, Permission, User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import *
# from search_views.filters import BaseFilter
# from search_views.search import SearchListView

from .forms import *
from .models import *


class CreateReport(LoginRequiredMixin,View):
    success_url = reverse_lazy('reports:main')
    template_name = 'reports/report_form.html'

    def get(self,request):
        form=CreateReportForm()
        x = get_object_or_404 (Job_title,employee__user=self.request.user)
        ctx={'form':form}
        ctx['job_title'] = x
        ctx['department'] = x.department
        ctx['form'].fields['task_type'].queryset = Task_type.objects.filter(job_title_id=x.id)
        return render(request,self.template_name,ctx)

    def post(self, request):
        form = CreateReportForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        data = form.save(commit=False)
        data.owner_id = Employee.objects.get(user = self.request.user).id
        data.save()

        return redirect(self.success_url)
    
    
class ReportListView(LoginRequiredMixin,ListView):
    paginate_by = 5
    template_name='reports/report_list.html'
    def get(self, request):
        strval =  request.GET.get("search", False)
        if request.user.is_authenticated:
            if strval :
                query = Q(description__icontains=strval)
                query.add(Q(owner__user__first_name__icontains=strval), Q.OR)
                query.add(Q(owner__user__last_name__icontains=strval), Q.OR)
                query.add(Q(task_type__type__icontains=strval), Q.OR)
                query.add(Q(owner__user=self.request.user), Q.AND)
                report_list = Report.objects.filter(query).select_related().order_by('-created_at')
            else :
                report_list = Report.objects.filter(owner__user=self.request.user).order_by('-created_at')
                
                
            ctx = {'report_list' : report_list, 'search': strval}

            return render(request, self.template_name, ctx)


class ReportDetailView(LoginRequiredMixin,DetailView):
    model = Report
    template_name= "reports/report_detail.html"
    
    def get_context_data(self, **kwargs) :
        ctx = super().get_context_data(**kwargs)
        ctx['group'] = User.objects.filter(groups__name__contains='director')
        return ctx
     

class ReportUpdateView(LoginRequiredMixin,UpdateView):
    model = Report
    form_class = CreateReportForm
    success_url = reverse_lazy('reports:list')
    template_name = 'reports/report_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        x = get_object_or_404 (Job_title,employee__user=self.request.user)
        context['job_title'] = x
        context['department'] = x.department
        context['form'].fields['task_type'].queryset = Task_type.objects.filter(job_title_id=x.id)
        return context


class ReportDeleteView(LoginRequiredMixin,DeleteView):
    model = Report
    success_url = reverse_lazy('reports:list')
    
    
class DirectiorView(LoginRequiredMixin,ListView):
    # model=Report
    template_name = 'reports/director_list.html'
    paginate_by = 5
    def get(self,request):
        strval =  request.GET.get("search", False)
        x = get_object_or_404(Job_title,employee__user=self.request.user)
        if request.user.is_authenticated:
            if strval :
                query = Q(description__icontains=strval)
                query.add(Q(owner__user__first_name__icontains=strval), Q.OR)
                query.add(Q(owner__user__last_name__icontains=strval), Q.OR)
                query.add(Q(task_type__type__icontains=strval), Q.OR)
                query.add(Q(task_type__job_title=x), Q.AND)
                report_list = Report.objects.filter(query).select_related().order_by('-created_at')
            else :
                report_list = Report.objects.filter(task_type__job_title=x).order_by('-created_at')
                

            ctx={'report_list':report_list,'search': strval}
            return render(request, self.template_name, ctx)
    
# class EmployeeView(ReportListView):
    
#     def get_queryset(self):
#         queryset = Report.objects.filter(owner__user=self.request.user).order_by('-created_at')
#         return queryset
    

def approve(request,pk):
    Report.objects.filter(id=pk).update(status='Approved')
    return redirect('reports:director')
    

    
    
    
# class ReportsFilter(BaseFilter):
#     search_fields = {
#         'search_text' : ['name', 'surname'],
#         'search_age_exact' : { 'operator' : '__exact', 'fields' : ['age'] },
#         'search_age_min' : { 'operator' : '__gte', 'fields' : ['age'] },
#         'search_age_max' : { 'operator' : '__lte', 'fields' : ['age'] },  
#     }

# class ReportsSearchList(LoginRequiredMixin,SearchListView):
#   # regular django.views.generic.list.ListView configuration
#     model = Report
# #   paginate_by = 10
#     template_name = "reports/test.html"

#   # additional configuration for SearchListView
#     form_class = ReportSearchForm
#     filter_class = ReportsFilter
    

