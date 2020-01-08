class FilterBackendViewMixin:
    filter_backends = None

    def get_queryset(self):
        result = super(FilterBackendViewMixin, self).get_queryset()
        for filter_backend in self.filter_backends:
            filter_instance = filter_backend(request=self.request, view=self)
            result = filter_instance.filter_queryset(result)
        return result
