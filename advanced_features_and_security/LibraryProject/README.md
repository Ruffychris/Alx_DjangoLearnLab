# Advanced Features and Security - Django Project

## Custom User Model
This project uses a custom user model (`CustomUser`) that extends Django's `AbstractUser`, with additional fields:
- `date_of_birth` (DateField)
- `profile_photo` (ImageField)

## Permissions and Groups

### Custom Permissions on the `Book` Model
The `Book` model includes the following custom permissions:
- `can_view` - allows viewing books
- `can_create` - allows creating books
- `can_edit` - allows editing books
- `can_delete` - allows deleting books

### User Groups
The following groups have been created with corresponding permissions:

| Group Name | Permissions |
|------------|-------------|
| Viewers    | `can_view` |
| Editors    | `can_create`, `can_edit` |
| Admins     | `can_view`, `can_create`, `can_edit`, `can_delete` |

### How Permissions Are Enforced
- Views are protected using Django’s `@permission_required` decorator.
- Example: `@permission_required('bookshelf.can_edit', raise_exception=True)` ensures that only users with the `can_edit` permission can access the edit view.
- Users are assigned to groups via Django admin or shell to control access.

### Notes
- All user references in models use `settings.AUTH_USER_MODEL` for compatibility with the custom user.
- This setup ensures role-based access control and enforces security best practices.
