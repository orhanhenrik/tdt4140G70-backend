from django.contrib.auth import get_user
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register

from files.models import File
from search.elasticsearch import elasticsearch
from search.models import SearchLog


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@login_required
def search(request):
    query = request.GET.get('query')
    if query:
        try:
            res = elasticsearch.search(query)
            print(res)
            duration = res['took']
            hits = res['hits']['hits']
            file_ids = list(map(lambda r: int(r['_id']), hits))
            files = File.objects.filter(pk__in=file_ids).all()

            all_highlights = {}

            for hit in hits:
                file = None
                for _file in files:
                    if _file.id == int(hit['_id']):
                        file = _file
                if file is None:
                    continue
                all_highlights[file] = hit['highlight']['attachment.content']

            SearchLog.objects.create(
                search_term=query,
                user=get_user(request),
                number_of_results=len(all_highlights)
            )

            error = None
        except Exception as e:
            print('exception', e)
            all_highlights = {}
            files = []
            error = 'Search failed'
            duration = 0
    else:
        all_highlights = {}
        files = []
        error = None
        duration = 0

    if len(all_highlights) == 0 and duration > 0:
        error = "No results found"

    return render(request, 'search/results.html', {
        'all_highlights': all_highlights,
        'files': files,
        'error': error,
        'duration': duration,
        'query': query
    })


@login_required()
def searchLogs(request):
    logs = SearchLog.objects.order_by('-timestamp').all()
    return render(request, 'search/searchLog.html', {
        'logs': logs
    })