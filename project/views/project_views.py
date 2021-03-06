""" All views for the model project """
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from project.forms.project_forms import CreateProjectForm, AddMember, UpdateProjectForm
from project.models.project import Project
from project.models.list import List
from project.models.task import Task
from timesheet.models.timesheet import Timesheet
from user.models import User


class ProjectView(View):
    ''' Class to manage all interactions and views with the projects
        and the dashboard.
    '''

    template_name = 'project/projects/projects.html'
    form = CreateProjectForm

    def get(self, request):
        ''' Method to view the dashboard. '''
        context = {}
        context['form'] = self.form
        context['form_add_member'] = AddMember(request)

        context['projects'] = Project.objects_project.get_projects(request.user)
        context['user'] = request.user
        context['members'] = Project.objects_project.get_members(request.user)

        return render(request, self.template_name, context)

    def post(self, request, project_id):
        ''' Method to display the form to update a project '''
        res = {}
        if request.method == 'POST':
            current_project = Project.objects.get(id=project_id)
            datas = {'name': current_project.name}

            form_update = UpdateProjectForm(instance=current_project, initial=datas)
            context = {'form_update': form_update, 'project': current_project}
            res['project_id'] = project_id
            res['template'] = render_to_string(
                template_name='project/projects/forms/update_project.html',
                context=context,
                request=request
            )

        return JsonResponse(res)

    @staticmethod
    def add_member(request):
        ''' Method called when the user add a member into a project. '''
        res = {}
        if request.method == 'POST':
            query = request.POST.get('member_email')
            if not Project.objects.filter(pk=request.POST.get('project_name')).exists():
                res['error'] = _('You must add a project before.')
                return JsonResponse(res)

            project = Project.objects.get(pk=request.POST.get('project_name'))
            new_user = Project.objects_project.add_member(query, project)
            if new_user:
                res['user_name'] = new_user.get().first_name
                res['user_id'] = new_user.get().id
                context = {
                    'projects': Project.objects_project.get_projects(request.user),
                    'members': Project.objects_project.get_members(request.user)
                }
                res['template'] = render_to_string(
                    template_name='user/personal_space_member.html',
                    context=context,
                    request=request
                )
                res['success'] = _(
                    f'The member {new_user.get().first_name} has been add into the project : {project}.')
            else:
                res['error'] = _(
                    'No user email saved in database or the user is already in the project.')

        return JsonResponse(res)

    @staticmethod
    def create_project(request):
        ''' Method called when the user create a project. '''
        res = {}
        context = {}
        if request.user.is_authenticated:
            if request.method == 'POST':
                query = request.POST.get('project_name')
                user = User.objects.get(id=request.user.id)
                project = Project.objects.filter(name=query)

                if project.exists():
                    res['error'] = _('This project already exists.')
                else:
                    project = Project.objects.create(name=query, user=user)
                    project.user_ids.add(user.id)
                    projects = user.main_user.all()

                    context['projects'] = projects
                    context['form_add_member'] = AddMember(request)
                    res['template_add_member'] = render_to_string(
                        template_name='project/projects/forms/add_member.html',
                        context=context,
                        request=request
                    )

                    res['project_name'] = query
                    res['project_id'] = project.id
                    res['template'] = render_to_string(
                        template_name='project/projects/project_detail.html',
                        context=context,
                        request=request
                    )
            else:
                res['error'] = _('No project name received.')

        return JsonResponse(res)

    @staticmethod
    def delete_project(request):
        ''' Method called when the user delete a project. '''
        res = {}
        if request.method == 'POST':
            project_id = request.POST.get('project_id')
            project_to_delete = Project.objects.get(id=project_id)

            members = project_to_delete.user_ids.all().exclude(id=request.user.id)
            res['member_to_remove'] = []
            for member in members:
                projects_member = member.member.all().filter(user_id=request.user.id)
                if len(projects_member) == 1:
                    if projects_member[0] == project_to_delete:
                        res['member_to_remove'].append(member.id)

            project_to_delete.delete()
            context = {}
            context['projects'] = Project.objects_project.get_projects(request.user)
            context['form_add_member'] = AddMember(request)
            context['members'] = Project.objects_project.get_members(request.user)
            if not context['members']:
                res['remove_all_members'] = True

            res['template'] = render_to_string(
                template_name='user/personal_space_member.html',
                context=context,
                request=request
            )
            res['template_add_member'] = render_to_string(
                template_name='project/projects/forms/add_member.html',
                context=context,
                request=request
            )
            res['project_id'] = project_id
            res['success'] = _('The project has been deleted.')
        else:
            res['error'] = _('The project doesn\'t have deleted.')

        return JsonResponse(res)

    @staticmethod
    def update_project(request):
        ''' Method called when the user delete a project. '''
        res = {}
        if request.method == 'POST':
            current_project = Project.objects.get(id=request.POST.get('project_id'))
            current_project.name = request.POST.get('name')
            current_project.save()

            context = {}
            context['projects'] = Project.objects_project.get_projects(request.user)
            context['form_add_member'] = AddMember(request)
            context['members'] = Project.objects_project.get_members(request.user)

            res['template'] = render_to_string(
                template_name='user/personal_space_member.html',
                context=context,
                request=request
            )
            res['template_add_member'] = render_to_string(
                template_name='project/projects/forms/add_member.html',
                context=context,
                request=request
            )
            res['project_id'] = current_project.id
            res['project_name'] = current_project.name

        return JsonResponse(res)

    @staticmethod
    def get_statistics(request):
        ''' Method called into the dashboard when you select a project
            to display the statistics of him.
        '''
        res = {}
        if request.method == 'POST':
            project = Project.objects.get(id=request.POST.get('project_id'))
            datas = Project.objects_project.get_number_task_by_list(project)
            time = Project.objects_project.get_total_planned_hours(project)
            history = Project.objects_project.get_history_time_work(project, List, Task, Timesheet)

            res['nb_task'] = datas
            res['time'] = time
            res['history'] = history

        return JsonResponse(res)
