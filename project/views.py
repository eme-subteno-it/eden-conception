""" All views for the user application """
from datetime import datetime
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from django.views import View
from django.views.generic.edit import UpdateView
from django.http import JsonResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from .forms import CreateProjectForm, CreateListForm, CreateTaskForm, UpdateTaskForm
from .models import Project, List, Task
from user.models import User


class ProjectView(View):

    template_name = 'project/projects/projects.html'
    form = CreateProjectForm

    def get(self, request):
        context = {}
        context['form'] = self.form

        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            projects = user.main_user.all()
            context['projects'] = projects

        return render(request, self.template_name, context)

    @staticmethod
    def create_project(request):
        res = {}
        context = {}
        if request.user.is_authenticated:
            if request.method == 'POST':
                query = request.POST.get('project_name')
                user = User.objects.get(id=request.user.id)
                Project.objects.create(
                    name=query,
                    user=user,
                )
                project = Project.objects.get(name=query)
                project.user_ids.add(user.id)
                projects = user.main_user.all()

                context['projects'] = projects

                res['project_name'] = query
                res['project_id'] = project.id
                res['template'] = render_to_string('project/projects/project_detail.html', context, request=request)
            else:
                res['error'] = _('No project name received.')

        return JsonResponse(res)

    @staticmethod
    def delete_project(request):
        res = {}
        if request.user.is_authenticated:
            if request.method == 'POST':
                project_id = request.POST.get('project_id')
                print(project_id)
                project_to_delete = Project.objects.get(id=project_id)
                project_to_delete.delete()

                res['project_id'] = project_id
                res['success'] = _('The project has deleted')
            else:
                res['error'] = _('The project doesn\'t have deleted')
        else:
            res['error'] = _('Please, connect you.')

        return JsonResponse(res)


class ListView(View):

    template_name = 'project/lists/lists.html'
    form = CreateListForm

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        lists = project.list_set.all()

        context = {
            'project': project,
            'lists': lists,
            'create_list_form': self.form,
            'create_task_form': CreateTaskForm
        }
        return render(request, self.template_name, context)

    @staticmethod
    def create_list(request):
        res = {}
        context = {}
        if request.user.is_authenticated:
            if request.method == 'POST':
                name = request.POST.get('list_name')
                project_id = request.POST.get('project_id')
                project = Project.objects.get(id=project_id)

                new_list = List.objects.create(
                    name=name,
                    project=project,
                )
                project.save()

                context['new_list'] = new_list
                context['create_task_form'] = CreateTaskForm

                res['list_name'] = name
                res['list_id'] = new_list.id
                res['template'] = render_to_string('project/lists/new_list.html', context, request=request)
            else:
                res['error'] = _('Please, write a list name.')
        else:
            res['error'] = _('Connect before create a list')

        return JsonResponse(res)

    @staticmethod
    def delete_list(request):
        res = {}
        if request.user.is_authenticated:
            if request.method == 'POST':
                list_id = request.POST.get('list_id')
                list_to_delete = List.objects.get(id=list_id)
                project = Project.objects.get(id=list_to_delete.project_id)

                list_to_delete.delete()
                project.save()

                res['list_id'] = list_id
                res['success'] = _('The list has deleted')
            else:
                res['error'] = _('The list doesn\'t have deleted')
        else:
            res['error'] = _('Please, connect you.')

        return JsonResponse(res)

    @staticmethod
    def create_task(request):
        res = {}
        if request.user.is_authenticated:
            if request.method == 'POST':
                user = User.objects.get(id=request.user.id)
                name = request.POST.get('task_name')
                list_id = request.POST.get('list_id')
                current_list = List.objects.get(id=int(list_id))
                project = Project.objects.get(id=current_list.project_id)

                # Manage the task's index
                index = 0
                if current_list.task_set.all().count() > 0:
                    index = current_list.task_set.all().reverse()[0].index + 1

                next_tasks = Task.objects.filter(index__gte=index)
                next_tasks.update(index=F('index') + 1)


                new_task = Task.objects.create(
                    name=name,
                    project_list=current_list,
                    assigned_to=user,
                    deadline=None,
                    index=index,
                )
                project.save()

                context = {'task': new_task, 'project': project}

                res['task_name'] = name
                res['task_id'] = new_task.id
                res['list_id'] = list_id
                res['template'] = render_to_string('project/tasks/new_task.html', context)

        return JsonResponse(res)

    @staticmethod
    def update_order_task(request):
        res = {}
        if request.user.is_authenticated:
            if request.method == 'POST':
                datas = json.loads(request.POST.get('datas'))

                for data in datas:
                    current_task = Task.objects.get(id=data['task_id'])
                    current_task.project_list = List.objects.get(id=data['list_id'])
                    current_task.index = data['index']
                    current_task.save()

        return JsonResponse(res)


class TaskView(View):

    template_name = 'project/tasks/tasks.html'

    def get(self, request, project_id, task_id):
        project = get_object_or_404(Project, pk=project_id)
        task = get_object_or_404(Task, pk=task_id)

        context = {'project': project, 'task': task}

        return render(request, self.template_name, context)

    def post(self, request, task_id):
        res = {}
        if request.user.is_authenticated:
            if request.method == 'POST':
                task_id = request.POST.get('task_id')
                current_task = Task.objects.get(id=int(task_id))
                datas = {}
                datas['assigned_to'] = current_task.assigned_to
                datas['description'] = current_task.description

                form = UpdateTaskForm(instance=current_task, initial=datas)
                context = {'form': form, 'task': current_task}

                res['task_id'] = task_id
                res['template'] = render_to_string('project/tasks/update_task.html', context, request=request)

        return JsonResponse(res)

    @staticmethod
    def update_task(request):
        res = {}
        if request.user.is_authenticated:
            if request.method == 'POST':
                user = User.objects.get(id=request.POST.get('assigned_to'))
                date_object = datetime.strptime(request.POST.get('deadline'), "%d/%m/%Y")
                current_task = Task.objects.get(id=request.POST.get('task_id'))

                current_task.name = request.POST.get('name')
                current_task.assigned_to = user
                current_task.deadline = date_object
                current_task.description = request.POST.get('description')
                current_task.save()

                context = {'task': current_task}

                res['task_id'] = current_task.id
                res['template'] = render_to_string('project/tasks/task_detail.html', context)

        return JsonResponse(res)
