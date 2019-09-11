from django.db.models.signals import m2m_changed,pre_delete
from django.dispatch import receiver
from tasks.models import TagCount, TodoItem
from todoapp.ru_taggit import RuTaggedItem
from django.db.models import Count

@receiver(m2m_changed, sender=TodoItem.tags.through)
def task_tags_updated(sender, instance, action, model, **kwargs):
    if action == "post_add" or action == "post_remove":
        for id in kwargs["pk_set"]:
            count = sender.objects.filter(tag_id=id).aggregate(total_tasks=Count('id'))
            model_ob = model.objects.get(id=id)
            t = TagCount.objects.filter(tag_id=id).first()
            print("***********", t)
            if t is None:
                t = TagCount.objects.get_or_create(tag_slug=model_ob.slug,tag_name=model_ob.name,tag_id=model_ob.id, tag_count=count["total_tasks"])
            else:
                t = TagCount.objects.get(id = t.id)
                t.tag_count=count["total_tasks"]
                t.save()

@receiver(pre_delete, sender=TodoItem.tags.through)
def task_tags_delete(sender, instance, **kwargs):
    print(sender, instance, kwargs)


