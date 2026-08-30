from django.contrib.auth.decorators import user_passes_test
from django.core. exceptions import PermissionDenied

def author_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.groups.filter(name='Authors').exists():
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper