from django.contrib.auth import get_user
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from files.models import File
from search.elasticsearch import elasticsearch
from search.models import SearchLog


@login_required
def search(request):
    query = request.GET.get('query')
    if query:
        try:
            res = elasticsearch.search(query)
            duration = res['took']
            hits = res['hits']['hits']
            file_ids = list(map(lambda r: int(r['_id']), hits))
            files = File.objects.filter(pk__in=file_ids).all()

            results = []

            for hit in hits:
                file = None
                for _file in files:
                    if _file.id == int(hit['_id']):
                        file = _file
                if file is None:
                    continue
                results.append((
                    file,
                    hit['highlight']['attachment.content']
                ))

            SearchLog.objects.create(
                search_term=query,
                user=get_user(request),
                number_of_results=len(results)
            )

            error = None
        except Exception as e:
            print(e)
            results = None
            error = 'Search failed'
            duration = 0
    else:
        results = []
        error = None
        duration = 0

    if len(results) == 0 and duration > 0:
        error = "No results found"

    return render(request, 'search/results.html', {
        'results': results,
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