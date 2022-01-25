from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from projects.models import Company, Project
#company name filter
class CompanyFilter(admin.SimpleListFilter):
    title = _('Company')
    parameter_name = 'company'

    def lookups(self, request, model_admin):
        companies = []
        qs = Company.objects.filter(id__in = model_admin.model.objects.all().values_list('company_id', flat = True).distinct())
        for c in qs:
            companies.append([c.id, c.name])
        return companies

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(company__id__exact=self.value())
        else:
            return queryset

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'start_date', 'end_date')
    list_filter = (CompanyFilter,)
    ordering = ('-start_date',)

    fieldsets = (
        (None, {'fields': ['company', 'title', 'start_date', 'end_date']}),
        ('Estimated hours', {'fields': ['estimated_design', 'estimated_development', 'estimated_testing']}),
        ('Actual hours', {'fields': ['actual_design', 'actual_development', 'actual_testing']}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()

        return 'company',


admin.site.register(Company)
admin.site.register(Project, ProjectAdmin)
