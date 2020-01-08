class BaseFilterBackend:

    def __init__(self, request, view):
        self._request = request
        self._view = view

    def filter_queryset(self, queryset):
        raise NotImplementedError
