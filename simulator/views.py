from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from simulator.models import State


# Методы идентификации
@csrf_exempt
def all_requests(request, method):
    current_case = State.get_case()
    project = current_case.project

    result = None
    if project.in_request_modifiers:
        for modifier in project.in_request_modifiers:
            mod = __import__(modifier, fromlist=[''])
            result = mod.Process(request, current_case)(result)


    result = current_case.in_response_body.copy()
    # Apply modifiers
    if project.in_response_modifiers:
        for modifier in project.in_response_modifiers:
            mod = __import__(modifier, fromlist=[''])
            result = mod.Process(request, current_case)(result)

    return JsonResponse(result, status=current_case.in_response_code)
