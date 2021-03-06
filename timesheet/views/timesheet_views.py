""" All views for the timesheet application """
from django.forms import inlineformset_factory
from django.views import View

from project.models.list import List
from project.models.task import Task
from timesheet.models.timesheet import Timesheet
from timesheet.forms.timesheet_forms import UpdateTimesheetForm


class TimesheetView(View):

    @classmethod
    def update_timesheet(cls, request):
        ''' When we update a task, this method is called
            to update too the timesheets associed at her
            and saved the changes.
        '''
        current_task = Task.objects.get(id=request.POST.get('task_id'))
        TimeFormSet = inlineformset_factory(
            parent_model=Task,
            model=Timesheet,
            form=UpdateTimesheetForm,
            can_delete=False,
        )
        formset = TimeFormSet(request.POST, instance=current_task, form_kwargs={'current_task': current_task})
        if formset.is_valid():
            formset.save()
        else:
            return formset.errors

        return True

    @classmethod
    def create_formset(cls, current_task):
        ''' To display the form to update the task,
            this method is called for can update too
            the timesheet.
        '''
        TimeFormSet = inlineformset_factory(
            parent_model=Task,
            model=Timesheet,
            form=UpdateTimesheetForm,
            can_delete=False,
            extra=1,
            fields=('created_at', 'user', 'description', 'unit_hour')
        )
        formset = TimeFormSet(instance=current_task, form_kwargs={'current_task': current_task})
        return formset
