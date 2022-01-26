import os
import datetime
import xlwt

from django.db.models import F
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls.base import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from markdown import markdown
from decimal   import Decimal

from projects.forms import ProjectForm
from projects.models import Project, ProjectLog


class AssignmentView(TemplateView):
    template_name = 'projects/assignment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        with open(os.path.join(os.path.dirname(settings.BASE_DIR), 'README.md'), encoding='utf-8') as f:
            assignment_content = f.read()

        context.update({
            'assignment_content': mark_safe(markdown(assignment_content))
        })

        return context


class DashboardView(LoginRequiredMixin, ListView):
    model = Project
    ordering = [F('end_date').desc(nulls_first=True)]
    context_object_name = 'projects'
    template_name = 'projects/dashboard.html'

    def get_queryset(self):
        projects = super().get_queryset()
        projects = projects.select_related('company')

        return projects


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('dashboard')


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        project_object = Project.objects.get(id=self.object.id)

        project_details = Project.objects.filter(pk=self.object.id).values()[0]
        project_form = ProjectForm(request.POST or None, instance=project_object)
        if project_form.is_valid():
            form = ProjectForm(request.POST, initial=project_details)
            if form.has_changed():
                project_object = project_form.save(commit=False)
                project_log = ProjectLog()
                if Decimal(request.POST['actual_design']) != Decimal(project_details['actual_design']):
                    project_log.initial_actual_design = project_details['actual_design']
                    project_log.changed_actual_design = request.POST['actual_design']
                    project_log.total_actual_design = Decimal(project_details['actual_design']) + Decimal(request.POST['actual_design'])
                    project_object.actual_design = project_log.total_actual_design
                    project_object.save()
                
                if Decimal(request.POST['actual_development']) != Decimal(project_details['actual_development']):
                    project_log.initial_actual_development = project_details['actual_development']
                    project_log.changed_actual_development = request.POST['actual_development']
                    project_log.total_actual_development = Decimal(project_details['actual_development']) + Decimal(request.POST['actual_development'])
                    project_object.actual_development = project_log.total_actual_development
                    project_object.save()
                
                if Decimal(request.POST['actual_testing']) != Decimal(project_details['actual_testing']):
                    project_log.initial_actual_testing = project_details['actual_testing']
                    project_log.changed_actual_testing = request.POST['actual_testing']
                    project_log.total_actual_testing = Decimal(project_details['actual_testing']) + Decimal(request.POST['actual_testing'])
                    project_object.actual_testing = project_log.total_actual_testing
                    project_object.save()
                
                project_log.changed_at = datetime.datetime.now()
                project_log.project = self.object
                project_log.user = self.request.user
                project_log.save()
                
        
        return super().post(request, *args, **kwargs)

def export_project_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="project.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Project')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    #columns = ['Project', 'Company', 'Estimated', 'Actual']
    columns = ['Project', 'Company']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Project.objects.all().values_list('title', 'company',)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response