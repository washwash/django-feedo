from applications.base.filters import BaseFilterBackend


class UserTenantFilterBackend(BaseFilterBackend):

    def filter_queryset(self, queryset):
        if self._request.user:
            return queryset.filter(user=self._request.user)
        return queryset.none()
