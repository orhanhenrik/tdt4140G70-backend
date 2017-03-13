from django.shortcuts import render

# Create your views here.
from files.models import File
from search.elasticsearch import elasticsearch
from search.models import SearchLog


def search(request):
    query = request.GET.get('query')
    if query:
        try:
            SearchLog.objects.create(
                search_term=query
            )
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
    return render(request, 'search/results.html', {
        'results': results,
        'error': error,
        'duration': duration,
        'query': query
    })