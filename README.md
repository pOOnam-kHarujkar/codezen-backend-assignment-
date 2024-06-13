# codezen-backend-assignment-
This project is a Django application that includes CRUD operations for orders and products, a Celery background task, and several other features as specified in the assignment.
## Project Setup
### Prerequisites
- Python 3.8
- Django 4.2.11
- Django REST Framework
- MySql (or another database of your choice)
- Git

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>](https://github.com/pOOnam-kHarujkar/codezen-backend-assignment-.git
   cd django_assignment

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. **Generate the requirements.txt file**

   ```bash
   pip freeze > requirements.txt

4. **Install the dependencies**

   ```bash
   pip install -r requirements.txt

5. **Configure the database**

   
   ```bash
   DATABASES = {
    'default': {
        'ENGINE': ''django.db.backends.mysql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '',
    }
   }

6. **Run migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate

7. **Create a superuser**

   ```bash
   python manage.py createsuperuser

8. **Running the Management Command :-** 
To import products from an Excel file, run the following command:

   ```bash
   python manage.py import_products path/to/your/excel/file.xlsx

9. **Start the development server**

 ```bash
python manage.py runserver


   


