from django import forms

from tasks.models import TodoItem


class AddTaskForm(forms.Form):
    description = forms.CharField(max_length=64, label="")


class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ('description',"priority","tags")
        labels = {"description": "Описание","priority":"приоритет","tags":"теги"}


class TodoItemExportForm(forms.Form):
    prio_high = forms.BooleanField(
        label="высокая важность", initial=True, required=False
    )
    prio_med = forms.BooleanField(
        label="средней важности", initial=True, required=False
    )
    prio_low = forms.BooleanField(
        label="низкой важности", initial=False, required=False
    )

class TodoImport(forms.Form):
        id_board =forms.IntegerField(
            label="ID BOARD", initial=True, required=True
        )