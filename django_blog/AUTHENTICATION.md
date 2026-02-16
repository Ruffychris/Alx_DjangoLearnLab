# Django Blog Authentication System

## Features
- User Registration
- Login and Logout
- Profile Editing
- Secure Password Hashing
- CSRF Protection

## Registration
Users can register using /register.
The form extends Django UserCreationForm and collects email.

## Login
Users login at /login using username and password.

## Logout
Users logout via /logout.

## Profile
Authenticated users can edit username and email at /profile.

## Security
- CSRF tokens enabled
- Django password hashing
- Login required decorator used

## Testing
1. Create account
2. Login
3. Edit profile
4. Logout
