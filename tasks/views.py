from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.urls import reverse
from tasks.forms import AddTaskForm, TodoItemForm, TodoItemExportForm, TodoImport
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from taggit.models import Tag
from trello import TrelloClient
from django.db.models import Count
# from taggit.managers import TaggableManager
from tasks.models import TagCount, TodoItem
from tasks.signals import task_tags_updated


@login_required
def index(request):
    ### import random
    ### counts = {t.name: random.randint(1, 100) for t in Tag.objects.all()}
    ## counts = {
    ##     t.name: t.taggit_taggeditem_items.count()
    ##     for t in Tag.objects.all()
    ## }
    counts = Tag.objects.annotate(
        total_tasks=Count('todoitem')
    ).order_by("-total_tasks")

    counts = {
        c.name: c.total_tasks
        for c in counts
    }
    # counts= TagCount.objects.all()
    # counts = {
    #     c.tag_name: c.tag_count
    #     for c in counts
    # }
    return render(request, "tasks/index.html", {"counts": counts})


def complete_task(request, uid):
    print("Enter")
    t = TodoItem.objects.get(id=uid)
    t.is_completed = True
    t.save()
    print("Save")
    # Trello
    print(t.id_trello)
    client = TrelloClient(api_key=request.user.profile.api_key, api_secret=request.user.profile.api_secret)
    print(client)
    card = client.get_card(t.id_trello)
    print(card.id,card.idList,card.idBoard)
    # Board = client.get_board(card.idBoard)
    list = client.get_board(card.idBoard).list_lists()[-1]
    # list = client.get_board(card.idBoard)
    card.change_list(list.id)


    # card.change_list(untitled_board.list_lists()[1].id)

    return HttpResponse("OK")

def add_task(request):
    if request.method == "POST":
        desc = request.POST["description"]
        t = TodoItem(description=desc)
        t.save()
    return redirect(reverse("tasks:list"))
    # return redirect("/tasks/list")

def delete_task(request, uid, tag_slug=None):
    t = TodoItem.objects.get(id=uid)
    t.delete()
    messages.success(request, "Задача удалена")
    if tag_slug:
        print("list_by_tag",tag_slug)
        return redirect(reverse("tasks:list_by_tag", args = [tag_slug]))
    else:
        print("list slug_none")
        return redirect(reverse("tasks:list"))

def filter_tags(tags_by_task):
    tags=[]
    for i in tags_by_task:
        for tag in i:
            if tag not in tags:
                tags.append(tag)
    return tags

class TaskListView(LoginRequiredMixin,ListView):
    model = TodoItem
    # queryset = TodoItem.objects.all()
    context_object_name = "tasks"
    template_name = "tasks/list.html"

    def get_queryset(self):
        u=self.request.user
        return u.tasks.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_tasks = self.get_queryset()
        tags = []
        for t in user_tasks:
            tags.append(list(t.tags.all()))

        context['tags'] = filter_tags(tags)
        return context

class TaskCreateView(View):
    def post(self, request, *args, **kwargs):
        form = TodoItemForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            form.save_m2m()
            messages.success(request, new_task.description + " Задача добавлена")
            return redirect(reverse("tasks:list"))
            # return redirect("/tasks/list")
        return render(request, "tasks/create.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = TodoItemForm()
        return render(request, "tasks/create.html", {"form": form})

class TaskDetailsView(DetailView):
    model = TodoItem
    template_name = 'tasks/details.html'

class TaskEditView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        print("******save**")
        t = TodoItem.objects.get(id=pk)
        form = TodoItemForm(request.POST, instance=t)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            form.save_m2m()
            messages.success(request, "Задача обновлена")
            return redirect(reverse("tasks:list"))

        return render(request, "tasks/edit.html", {"form": form, "task": t})

    def get(self, request, pk, *args, **kwargs):
        t = TodoItem.objects.get(id=pk)
        form = TodoItemForm(instance=t)
        return render(request, "tasks/edit.html", {"form": form, "task": t})

class TaskExportView(LoginRequiredMixin, View):
    def generate_body(self, user, priorities, tag=None):
        q = Q()
        print("*****Export*****",q)
        print(tag)
        if priorities["prio_high"]:
            q = q | Q(priority=TodoItem.PRIORITY_HIGH)
        if priorities["prio_med"]:
            q = q | Q(priority=TodoItem.PRIORITY_MEDIUM)
        if priorities["prio_low"]:
            q = q | Q(priority=TodoItem.PRIORITY_LOW)

        tasks = TodoItem.objects.filter(owner=user).filter(q).all()
        if tag:
            tag2 = get_object_or_404(Tag, slug=tag)
            tasks = tasks.filter(tags=tag2).all()

        body = "Ваши задачи и приоритеты:\n"
        for t in list(tasks):
            if t.is_completed:
                body += f"[x] {t.description} ({t.get_priority_display()})\n"
            else:
                body += f"[ ] {t.description} ({t.get_priority_display()})\n"
        return body

    def post(self, request, *args, **kwargs):
        form = TodoItemExportForm(request.POST)
        if form.is_valid():
            email = request.user.email
            if 'tag_slug' in kwargs:
                body = self.generate_body(request.user, form.cleaned_data, kwargs['tag_slug'])
            else:
                body = self.generate_body(request.user, form.cleaned_data)
            send_mail("Задачи", body, settings.EMAIL_HOST_USER, [email])
            messages.success(
                request, "Задачи были отправлены на почту %s" % email)
        else:
            messages.error(request, "Что-то пошло не так, попробуйте ещё раз")
        if 'tag_slug' in kwargs:
            print("post tag_slug",kwargs['tag_slug'])
            return redirect(reverse("tasks:list_by_tag", args = [kwargs['tag_slug']]))
        else:
            print("post tag_slug=none")
            return redirect(reverse("tasks:list"))

    def get(self, request, *args, **kwargs):
        form = TodoItemExportForm()
        print(kwargs)
        if 'tag_slug' in kwargs:
            return render(request, "tasks/export.html", {"form": form, "slug":kwargs["tag_slug"]})
        else:
            return render(request, "tasks/export.html", {"form": form})

def filter_tasks(tasks, tag):
    t =[]
    for task in tasks:
        if tag in task["tags"]:
         t.append(task["task_id"])
    return t


def tasks_by_tag(request, tag_slug=None):
    u = request.user
    tasks = TodoItem.objects.filter(owner=u).all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        tasks = tasks.filter(tags__in=[tag])

    all_tags = []
    for t in tasks:
        all_tags.append(list(t.tags.all()))
    all_tags = filter_tags(all_tags)

    return render(
        request,
        "tasks/list_by_tag.html",
        {"tag": tag, "tasks": tasks, "all_tags": all_tags},)


class TaskImport(LoginRequiredMixin, View):
    def import_task_trello(self, user,id):
        client = TrelloClient(api_key = user.profile.api_key, api_secret = user.profile.api_secret)
        tasks_Trello = client.list_boards()[id["id_board"]]
        to_do = tasks_Trello.list_lists()[0]
        cards = to_do.list_cards()
        card = to_do.list_cards()[0]
        tasks = TodoItem.objects.filter(owner=user).all()
        tag=[]
        for t in tasks:
            # tag.append(t.tags)
            t.delete()
        # for ta in tag:
        #     count = TodoItem.tags.through.objects.filter(tag_id=ta).aggregate(total_tasks=Count('id'))
        r = 0
        for i in cards:
            t = TodoItem(description=i.name,id_trello=i.id,owner=user)
            t.save()
            r+=1
        return r

    def post(self, request, *args, **kwargs):
        form = TodoImport(request.POST)
        if form.is_valid():
            cnt =self.import_task_trello(request.user, form.cleaned_data)
            r = f"Импротировано {self.import_task_trello(request.user, form.cleaned_data)} зад."

            messages.success(request, r)
            return redirect(reverse("tasks:list"))

    def get(self, request, *args, **kwargs):
        form = TodoImport()
        return render(request, "tasks/import.html", {"form": form})

def trigger_error(request):
    division_by_zero = 1 / 0