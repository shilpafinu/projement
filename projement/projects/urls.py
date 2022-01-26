from django.conf.urls import url

from projects.views import AssignmentView, DashboardView, ProjectUpdateView, export_project_xls


urlpatterns = [
    url(r'^$', AssignmentView.as_view(), name='assignment'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^projects/(?P<pk>[0-9]+)-(?P<slug>[-\w]*)/$', ProjectUpdateView.as_view(), name='project-update'),
    url(r'^export/$', export_project_xls, name='export_project_xls'),
]
