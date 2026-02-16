# Blog Post Management System

## Features
- List all posts
- View single post
- Create post (auth only)
- Edit post (author only)
- Delete post (author only)

## Permissions
- LoginRequiredMixin for create/update/delete
- UserPassesTestMixin to restrict ownership

## URLs
/posts/
/posts/new/
/posts/<id>/
/posts/<id>/edit/
/posts/<id>/delete/

## Testing
1. Login
2. Create post
3. Edit post
4. Try editing with another account (denied)
5. Delete post
