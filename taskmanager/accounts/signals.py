from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_roles(sender, **kwargs):
    superadmin_group, _ = Group.objects.get_or_create(name="SuperAdmin")
    admin_group, _ = Group.objects.get_or_create(name="Admin")
    user_group, _ = Group.objects.get_or_create(name="User")
    all_permissions = Permission.objects.all()
    superadmin_group.permissions.set(all_permissions)

    admin_permissions = Permission.objects.filter(
        codename__in=[
            "add_task",
            "change_task",
            "delete_task",
            "view_task",
            "can_assign_task",
            "can_view_reports",
        ]
    )
    admin_group.permissions.set(admin_permissions)
    user_permissions = Permission.objects.filter(
        codename__in=[
            "view_task",
            "change_task",
        ]
    )
    user_group.permissions.set(user_permissions)
