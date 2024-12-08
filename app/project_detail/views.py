from django.views.generic import DetailView

from projects.models import Project


class ProjectDetailMain(DetailView):
    model = Project
    template_name = "project_detail/project_detail_main.html"
    context_object_name = 'project'