from functools import wraps

from rest_framework import status
from rest_framework.response import Response


def required_params(request_attr='query_params', params=None):
    if params is None:
        params = []

    def decorator(view_func):
        """
        decorator use wraps to get parameter from view_func
        and pass to  _wrapped_view
        instance is self in view_func
        """
        @wraps(view_func)
        def _wrapped_view(instance, request, *args, **kwargs):
            data = getattr(request, request_attr)
            missing_params = [
                param
                for param in params
                if param not in data
            ]
            if missing_params:
                missing_params_str = ','.join(missing_params)
                return Response(
                    {
                        'message': 'missing {} in request'.format(missing_params_str),
                        'success': False,
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            return view_func(instance, request, *args, **kwargs)
        return _wrapped_view
    return decorator



