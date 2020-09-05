import logging
from rest_framework.permissions import BasePermission

logger = logging.getLogger('logger')


class BoardManagementPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user is None or request.user.is_anonymous:
            logger.warning(f'User{request.user} is not authenticated')

            return False

        if not request.user.is_group_admin() and not request.user.is_group_staff():
            logger.warning(f'User{request.user} does not have board management permission')

            return False

        return True
