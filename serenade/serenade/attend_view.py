# -*- coding: utf-8 -*-
from django.views import generic
from datetime import datetime, timedelta
from .models import Attend, User


class AttendView(generic.ListView):
    '''
    all blog list
    '''
    # paginate_by = PAGE_NUM
    template_name = 'attend_list.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super(AttendView, self).get_context_data(**kwargs)

        # task_date_set = set()
        # object_list = Attend.objects.all()
        # for obj in object_list:
        #     date_str = obj.task_date[:10]
        #     _date = datetime.strptime(date_str.strip(), '%Y-%m-%d')
        #     task_date_set.add(_date)  # 拿到所有活动时间
        #
        # task_date_str_set = []
        # task_date_set = sorted(task_date_set)
        # for task_date in task_date_set:
        #     task_date_str_set.append(task_date.strftime('%Y-%m-%d'))

        localhost_list, localhost_user_dict, week = self.get_acctivity_localhost()
        print(localhost_list)
        context['week'] = week
        context['localhost_list'] = localhost_list
        context['user_list'] = self.get_user_list(localhost_user_dict)
        return context

    def get_queryset(self):
        object_list = Attend.objects.all() #.order_by('-published_date')
        return object_list

    def get_acctivity_localhost(self):
        '''
        获取本周所有活动地
        :return:
        '''
        localhost_set = set()
        current_now = datetime.now()
        current_now_info = current_now.isocalendar()

        week = current_now_info[1]
        day = current_now_info[2]
        start_date = current_now - timedelta(days=day, hours=current_now.hour, minutes=current_now.minute, seconds=current_now.second)
        end_date = current_now + timedelta(days=(7-day), hours=current_now.hour, minutes=current_now.minute, seconds=current_now.second)
        object_list = Attend.objects.filter(task_date__gte=start_date, task_date__lte=end_date).order_by('task_date')

        localhost_user_dict = {}
        for obj in object_list:
            localhost_set.add(obj.localhost)

            detail = {
                'category': obj.category,
                'attend_status': obj.attend_status,
            }

            if obj.username in localhost_user_dict:

                localhost_user_dict[obj.username].update({obj.localhost:detail})
            else:
                localhost_user_dict[obj.username] = {obj.localhost:detail}

        # print(localhost_user_dict)
        localhost_list = list(localhost_set)

        res_dict = {}
        for username, value in localhost_user_dict.items():
            for localhost in localhost_list: # 每个人按照 活动地 给出相关信息， 已经排好序了

                if username not in res_dict:
                    res_dict[username] = []

                dp_str = '-2'
                if localhost in value:
                    detail = value[localhost]
                    if detail.get('attend_status') == -1:
                        dp_str = '-1'
                    elif detail.get('attend_status') == 1:
                        dp_str = '1'
                        # 如果正常出勤，看是否上榜
                        if detail.get('category') == 1:
                            dp_str += '+1.5'
                        elif detail.get('category') == 2:
                            dp_str += '+2'
                        elif detail.get('category') == 3:
                            dp_str += '+3.5'

                res_dict[username].append(dp_str)

        print(res_dict)
        return localhost_list, res_dict, week

    def get_user_list(self, res_dict):
        '''
        获取所有用户列表
        :return:
        '''
        user_list = User.objects.filter(status=1)
        object_list = []

        for user in user_list:
            user_dict = {
                'id': user.id,
                'username': user.username,
                'localhost_list': res_dict.get(user.username, []),
                # 'localhost_list': res_dict.get(user.username, []),
                'status': user.status,
                'group': user.group
            }
            object_list.append(user_dict)
        # print(object_list)
        return object_list

