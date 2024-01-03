from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, Permission, User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import *
from datetime import date
from xhtml2pdf import pisa
from django.template.loader import get_template
from .forms import *
from .models import *


class ExportAgendaAsPDFView(TemplateView):
    template_name = 'task/agenda_pdf.html'

    def get(self, request, location, *args, **kwargs):
        agenda = self.kwargs.get('agenda', [])

        context = {'agenda': agenda, 'location': location}
        template = get_template(self.template_name)
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="agenda.pdf"'

        pisa_status = pisa.CreatePDF(
            html, dest=response, encoding='utf-8')

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        return response


def get_filtered_employees(request):
    department_id = request.GET.get('department')
    location = request.GET.get('location')
    if (department_id and location):

        try:
            filtered_employees = Employee.objects.filter(department_id=department_id, location=location).exclude(
                user_id=request.user.id).values('id', 'user__first_name', 'user__last_name')
            # Filter the employees based on the department and role

            employees_list = list(filtered_employees)
            return JsonResponse(employees_list, safe=False)
        except Employee.DoesNotExist:
            return JsonResponse([], safe=False)
    else:
        return JsonResponse([], safe=False)


class CreateTask(LoginRequiredMixin, View):
    success_url = reverse_lazy('task:main')
    template_name = 'task/task_form.html'

    def get_context_data(self, form):

        if self.request.user.employee.job_title.title == "Director":
            form.fields['remarks'].disabled = 'disabled'
        else:
            form.fields['reviews'].disabled = 'disabled'
        context = {
            'form': form,
            'department': get_object_or_404(Department, employee__user=self.request.user),
            'locations': Employee.objects.values_list('location', flat=True).distinct(),
        }
        return context

    def get(self, request):
        form = CreateTaskForm()

        context = self.get_context_data(form)
        return render(request, self.template_name, context)

    def post(self, request):
        form = CreateTaskForm(request.POST)
        if not form.is_valid():
            context = self.get_context_data(form)
            return render(request, self.template_name, context)

        current_employee = get_object_or_404(Employee, user=request.user)
        data = form.save(commit=False)
        data.owner_id = current_employee.id

        # Retrieve other POST data
        department = request.POST.get('department')
        assigned_to = request.POST.getlist('assigned_to')

        # Update 'data' with additional form fields and POST data
        data.department_id = department
        data.department = current_employee.department
        data.save()
        data.assigned_to.add(*assigned_to)

        # Assign selected employees to the task
        return redirect(self.success_url)


class TaskListView(LoginRequiredMixin, View):
    template_name = 'task/task_list.html'
    paginate_by = 5

    def get(self, request):
        employee = Employee.objects.get(user=self.request.user)

        if request.user.is_authenticated:
            if request.user.employee.job_title.title == "Director":
                task_list = Task.objects.filter(
                    owner__department=employee.department
                ).order_by('-created_date')
            else:
                task_list = Task.objects.filter(
                    Q(owner__user=self.request.user) | Q(assigned_to=employee)
                ).order_by('-created_date').distinct()

            # Serialize task data to JSON
            task_data = [
                {
                    'id': task.id,
                    'title': task.title,
                    'assigned_to': [employee.fullname for employee in task.assigned_to.all()],
                    'category': task.category,
                    'created_date': task.created_date.strftime('%d-%b-%y @ %I:%M %p'),
                    'target_date': task.target_date.strftime('%d %b %Y'),
                    'status': task.status,
                }
                for task in task_list
            ]

            # Prepare context for template
            context = {
                'task_data': task_data,
                'locations': Employee.objects.values_list('location', flat=True).distinct(),
                'department': get_object_or_404(Department, employee__user=self.request.user),
            }

            if request.is_ajax():
                # If the request is AJAX, return JSON response
                return JsonResponse({'task_data': task_data})

            # Otherwise, render the template with the context
            return render(request, self.template_name, context)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task:list')


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "task/task_detail.html"

    # def get_context_data(self, **kwargs) :
    #     context = super().get_context_data(**kwargs)
    #     context['group'] = User.objects.filter(groups__name__contains='admin')
    #     return context


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = CreateTaskForm
    success_url = reverse_lazy('task:list')
    template_name = 'task/task_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the task instance being updated

        task = self.get_object()
        location = [emp.location for emp in task.assigned_to.all()]
        # Get the department with the task
        department = task.owner.department
        # location = Task.objects.filter(assigned_to__location=location)

        # Add extra context
        context['department'] = department
        if location:
            context['selected_location'] = location[0]
            print(location[0])

        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Edit the attributes of the widgets
        if self.request.user.employee.job_title.title == "Director":
            form.fields['remarks'].disabled = 'disabled'
        else:
            form.fields['reviews'].disabled = 'disabled'
            form.fields['title'].disabled = 'disabled'
            form.fields['target_date'].disabled = 'disabled'
            form.fields['category'].disabled = 'disabled'

        return form


class DashboardView(View):
    template_name = 'task/main.html'

    def get_context_data(self):
        # Fetch data for your dashboard
        user = self.request.user
        is_admin = self.request.user.employee.job_title.title == "Director"
        last_month_start = timezone.now() - timedelta(days=30)
        last_week_start = timezone.now() - timedelta(weeks=1)
        team_members = Employee.objects.filter(
            department=user.employee.department).exclude(user_id=user.id)
        employee = Employee.objects.get(user=self.request.user)
        last_assigned_tasks = Task.objects.filter(
            Q(assigned_to=employee) & Q(created_date__gte=last_week_start)
        ).order_by('-created_date').distinct()
        if is_admin:
            # User is in admin group, can see all stats

            total_tasks = Task.objects.filter(
                created_date__gte=last_month_start).count()
            completed_tasks = Task.objects.filter(
                status='Done', created_date__gte=last_month_start).count()
            inprogress_tasks = Task.objects.filter(
                status='In Progress', created_date__gte=last_month_start).count()
            in_progress = Task.objects.filter(status='In Progress')

        else:
            # User is a normal user, can only see their own stats
            q = (Q(assigned_to=employee) | Q(owner__user=user)) & Q(
                created_date__gte=last_month_start)
            total_tasks = Task.objects.filter(q).count()
            completed_tasks = Task.objects.filter(Q(status='Done') & q).count()
            inprogress_tasks = Task.objects.filter(
                Q(status='In Progress') & q).count()
            in_progress = Task.objects.filter(
                status='In Progress', owner__user=user)

        context = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'inprogress_tasks': inprogress_tasks,
            'in_progress': in_progress,
            'team_members': team_members,
            'last_assigned': last_assigned_tasks,
            # Add more data as needed
        }
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)


class Agenda(View):
    template_name = 'task/agenda.html'

    def get(self, request, *args, **kwargs):
        # Get unique locations
        employees = Employee.objects.values_list(
            'location', flat=True).distinct()

        # Set the default date to the current date
        selected_date = request.GET.get('selected_date', date.today())
        # formatted_selected_date = formats.date_format(selected_date, 'Y-m-d')
        # print(formatted_selected_date)
        tasks_for_date = Task.objects.filter(created_date__date=selected_date)

        # Categorize tasks based on employee location
        categorized_tasks = {}

        for location in employees:
            tasks_for_location = tasks_for_date.filter(
                assigned_to__location=location)

            if location not in categorized_tasks:
                categorized_tasks[location] = {'tasks': tasks_for_location}
            else:
                categorized_tasks[location]['tasks'] |= tasks_for_location
        context = {
            'categorized_tasks': categorized_tasks,
            'selected_date': selected_date,

        }
        return render(request, self.template_name, context)


class AgendaDetailsView(View):
    template_name = 'task/agenda_details.html'

    def get(self, request, location, selected_date, *args, **kwargs):
        # Get tasks for the specified location

        tasks_for_location = Task.objects.filter(
            assigned_to__location=location, created_date__date=selected_date)
        print(request.GET)
        if 'export' in request.GET:
            pdf_view = ExportAgendaAsPDFView.as_view()
            response = pdf_view(
                request, agenda=tasks_for_location, location=location)

            return response

        context = {
            'location': location,
            'tasks_for_location': tasks_for_location,
            # Add other context variables as needed
        }

        return render(request, self.template_name, context)
