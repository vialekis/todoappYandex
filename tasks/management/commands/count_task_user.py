from django.core.management import BaseCommand
from tasks.models import TodoItem
from django.contrib.auth.models import User

class Command(BaseCommand):
    help =u"Count all tasks from users"

    def handle(self, *args, **options):
        i = 0
        freq_dict = {}
        for u in User.objects.all():
            for t in u.tasks.all():
                if not t.is_completed:
                    if t.owner_id in freq_dict:
                        freq_dict[t.owner_id] = freq_dict[t.owner_id] + 1
                    else:
                        freq_dict[t.owner_id]=1
        aa = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
        print(aa[1][0])
        aaa = User.objects.get(id=aa[1][0])
        print(aaa)
        # k=0
        # for j in aa:
        #     if j[1]<20:
        #         print(j)
        #         k+=1
        # print(k)