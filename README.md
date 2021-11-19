A Django web-app written for recruitation purposes at Mirumee Software.

## Setup
Start a django project, move the `mirumee_webapp` directory to the project root, then install dependencies:
```shell
pip install -r mirumee_webapp/requirements.txt
```
Add the app and DRF to `INSTALLED_APPS` in the project's ``settings.py``:
```python
INSTALLED_APPS = [
    ...
    'mirumee_webapp',
    'rest_framework'
]
```
Paste the following to the bottom of the project's `settings.py`:
```python
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
```
And this, as to replace the django authentication user model with the one defined in the app:
```python
AUTH_USER_MODEL = 'mirumee_webapp.User'
```
The app uses HTTP BA and django's authentication on the back-end.

So, after making migrations and migrating, create a superuser for your first request:
```shell
python manage.py createsuperuser
```
and afterwards use that username and password to authenticate to the API with HTTP BA ( basic authentication ) for every
request.
## Usage
Cores are available under the `/api/cores/` endpoint. 

Use this command to create three sample users:
```shell
python manage.py create_sample_users
```
The command creates `sample_user_0`, `sample_user_1` ... each with passwords `0`,`1`,`2` respectively.

In order to choose your favorite rocket, while authenticated, perform a `POST` request to the `/api/choose-favorite/` endpoint, and in the
payload represent your favorite rocket using it's `core_id`:
```json
{
  "core_id": "B1048"
}
```

In order to view your current favorite core, send a `GET` request to `/api/view-favorite/`.