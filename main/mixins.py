from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render


class SuperAdminLoginRequiredMixin(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied("You must be a superuser to access this page.")
        else:
            # Custom handling for displaying a 403 Forbidden template
            return render(self.request, 'web/403.html', status=403)