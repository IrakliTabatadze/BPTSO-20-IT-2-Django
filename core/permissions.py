from django.http import HttpResponseForbidden, HttpResponse

def event_manager_permission(function):
    def wrapper(request, *args, **kwargs):
        if request.user.has_perm('core.add_event'):
            return function(request, *args, **kwargs)

        return HttpResponseForbidden('You do not have permission to perform this action.')

    return wrapper


def delete_event_permission(function):
    def wrapper(request, *args, **kwargs):
        if request.user.has_perm('core.delete_event'):
            return function(request, *args, **kwargs)

        return HttpResponseForbidden('You do not have permission to perform this action.')

    return wrapper

def change_event_permission(function):
    def wrapper(request, *args, **kwargs):
        if request.user.has_perm('core.change_event'):
            return function(request, *args, **kwargs)

        return HttpResponseForbidden('You do not have permission to perform this action.')

    return wrapper