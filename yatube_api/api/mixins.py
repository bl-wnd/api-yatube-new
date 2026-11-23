from rest_framework.exceptions import PermissionDenied


class AuthorPermissionMixin:
    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionDenied('Редактирование чужих записей запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied('Удаление чужих записей запрещено!')
        super().perform_destroy(instance)
