from django.http import JsonResponse

def estudantes(request):
    if request.method == 'GET':
        estudantes = [
            {'nome': 'John Doe', 'idade': 25},
            {'nome': 'Jane Smith', 'idade': 22},
            {'nome': 'Alice Johnson', 'idade': 27}
        ]
        return JsonResponse(estudantes, safe=False)