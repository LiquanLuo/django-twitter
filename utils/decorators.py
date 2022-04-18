from rest_framework import status
from rest_framework.response import Response


def required_params(request_attr='query_params', params=None):
    if params is None:
        params = []

    def decorator(view_func):
        def _wrappered_view(instance, request, *args, **kwargs):
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
        return _wrappered_view
    return decorator



