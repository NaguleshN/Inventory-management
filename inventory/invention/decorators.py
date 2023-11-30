from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **Kwargs):
        if request.user.is_authenticated:
            return redirect('Home')
        else:
            return view_func(request, *args, **Kwargs)

    return wrapper_func

def allowed_user(allowed_roles = []):
    def decorator(view_func):
        def wrapper_func(request, *args, **Kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
              return view_func(request, *args, **Kwargs)
            else:
                return render(request, 'no_permission.html')
        return wrapper_func
    return decorator

