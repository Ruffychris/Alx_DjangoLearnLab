from django.apps import AppConfig

class BookshelfConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookshelf'

    def ready(self):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from .models import Book

        content_type = ContentType.objects.get_for_model(Book)

        perms = {
            "can_view": "View Book",
            "can_create": "Create Book",
            "can_edit": "Edit Book",
            "can_delete": "Delete Book",
        }

        # Ensure permissions exist
        for codename, name in perms.items():
            Permission.objects.get_or_create(
                codename=codename,
                content_type=content_type,
                name=f"Can {name.lower()}"
            )

        # Create groups if not exist
        editors, _ = Group.objects.get_or_create(name="Editors")
        viewers, _ = Group.objects.get_or_create(name="Viewers")
        admins, _ = Group.objects.get_or_create(name="Admins")

        editors.permissions.set(Permission.objects.filter(codename__in=["can_create", "can_edit"]))
        viewers.permissions.set(Permission.objects.filter(codename__in=["can_view"]))
        admins.permissions.set(Permission.objects.filter(codename__in=["can_view", "can_create", "can_edit", "can_delete"]))
