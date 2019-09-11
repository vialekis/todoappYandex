from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.index, name="index"),
    # path("list/", views.TaskListView.as_view(), name="list"),
    path("list/",views.tasks_by_tag, name="list"),
    path("list/tag/<slug:tag_slug>", views.tasks_by_tag, name="list_by_tag"),
    path("create/", views.TaskCreateView.as_view(), name="create"),
    path("add-task/", views.add_task, name="api-add-task"),
    path("complete/<int:uid>", views.complete_task, name="complete"),
    path("delete/<int:uid>", views.delete_task, name="delete"),
    path("delete/<int:uid>/tag/<slug:tag_slug>", views.delete_task, name="delete"),
    path("details/<int:pk>",views.TaskDetailsView.as_view(), name="details"),
    path("edit/<int:pk>",views.TaskEditView.as_view(), name="edit"),
    path("export/", views.TaskExportView.as_view(), name="export"),
    path("import/", views.TaskImport.as_view(), name="import"),
    # path("export/tag/", views.TaskExportView.as_view(), name="export_tag"),
    path('sentry-debug/', views.trigger_error, name="error_sentry"),
    path("export/tag/<slug:tag_slug>", views.TaskExportView.as_view(), name="export_slug"),
]
