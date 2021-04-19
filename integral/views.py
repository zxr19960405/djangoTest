from django.conf import settings
from django_redis import get_redis_connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def get_rank_list(request):
    """
    获取排名列表
    """
    client = request.GET.get('client')
    if not client:
        return JsonResponse('请传递客户端信息！')
    start = request.GET.get('start', 1)
    end = request.GET.get('end', 0)
    try:
        start = int(start)
        end = int(end)
    except (TypeError, ValueError):
        return JsonResponse('请传递正确的排名参数！')
    start -= 1
    end -= 1
    # print(start, end)
    redis_key = settings.REDIS_SCORE
    redis_conn = get_redis_connection('default')
    if start and end:
        rank_list = redis_conn.zrevrange(redis_key, start=start, end=end, withscores=True)
    else:
        rank_list = redis_conn.zrevrange(redis_key, start=start, end=end, withscores=True)
    # print(rank_list)
    # 整理排序数据
    rank_dict_list = [
        {
            'client': element[0].decode('utf-8'),
            'score': element[1],
            'rank': index + start
        }
        for index, element in enumerate(rank_list)
    ]
    client_score = redis_conn.zscore(redis_key, client)
    client_rank = redis_conn.zrank(redis_key, client)
    # print(client_score, client_rank)
    client_dict = {'client': client, 'score': client_score, 'rank': client_rank}
    rank_dict_list.append(client_dict)
    return JsonResponse(rank_dict_list, safe=False)


@csrf_exempt
def update_rank(request):
    """
    更新排名
    """
    client = request.POST.get('client')
    score = request.POST.get('score')
    if not client or not score:
        return JsonResponse('请传递客户端信息和分数信息！')
    redis_key = settings.REDIS_SCORE
    redis_conn = get_redis_connection('default')
    redis_conn.zadd(redis_key, {client: score})
    return JsonResponse({'status': 'success!'})
