Property Management System
Property Management System (PMS), a Django-based REST API for managing hotel bookings. The application uses Django REST Framework, PostgreSQL, and JWT authentication, with endpoints for user registration, login, room creation, check-in, and checkout. It is containerized using Docker and docker-compose for production environment.
Project Structure

Prerequisites

- Python 3.10+
- Postman: For testing API endpoints.
- psql: For interacting with PostgreSQL (optional).

Setup for Local Development
1. Create ```.env.dev```
Create a file named .env.dev in the root of the repository with the following content:
```env
DJANGO_ENV=dev
POSTGRES_DB=pms
POSTGRES_USER=pms_user
POSTGRES_PASSWORD=pms_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
SECRET_KEY=your-dev-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

2. Ensure ```requirements.txt```
Verify that requirements.txt contains:

```text
django>=4.0
djangorestframework>=3.13
djangorestframework-simplejwt>=5.2
psycopg2-binary>=2.9 # only for postgres, 
python-dotenv>=0.19
```
3. Run migrations
```text
python manage.py migrate
```
4. Run Tests
verify the application:
'''text
pytest
```

5. Test API with Postman

```text   
Use Postman to test the API endpoints:
Register

URL: POST http://127.0.0.1:8000/api/auth/register/
Headers: Content-Type: application/json
Body:{
  "username": "user",
  "email": "user@example.com",
  "password": "User1234!"
}


Expected: 201 Created

Login

URL: POST http://127.0.0.1:8000/api/auth/login/
Headers: Content-Type: application/json
Body:{
  "username": "user",
  "password": "User1234!"
}


Expected: 200 OK, save access_token.

Create Room

URL: POST http://127.0.0.1:8000/api/rooms/
Headers:
Content-Type: application/json
Authorization: Bearer <access_token>


Body:{
  "number": "101",
  "price": "100.00",
  "is_available": true
}


Expected: 201 Created

Check-in

URL: POST http://127.0.0.1:8000/api/bookings/
Headers:
Content-Type: application/json
Authorization: Bearer <access_token>


Body:{
  "room_number": "101"
}


Expected: 201 Created, status: "CHECKED_IN", is_available: false

Checkout

URL: POST http://127.0.0.1:8000/api/bookings/checkout/
Headers:
Content-Type: application/json
Authorization: Bearer <access_token>


Body:{
  "room_number": "101"
}


Expected: 200 OK, status: "CHECKED_OUT", full_price: "100.00", is_available: true, total_price: "100.00"
```

Setup for Production

```text
1. Create .env.prod
Create a file named .env.prod in the root of the repository with the following content:
DJANGO_ENV=prod
POSTGRES_DB=pms
POSTGRES_USER=pms_user
POSTGRES_PASSWORD=pms_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
SECRET_KEY=your-prod-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,127.0.0.1


Generate a secure SECRET_KEY:python -c "import secrets; print(secrets.token_urlsafe(50))"

Replace your-prod-secret-key with the generated key.
Replace yourdomain.com with your production domain.

2. Update settings.py
Ensure settings.py includes your production domain in ALLOWED_HOSTS:
ALLOWED_HOSTS = ['127.0.0.1', 'localhost'] if os.getenv('DJANGO_ENV', 'dev') == 'dev' else ['yourdomain.com', '127.0.0.1']

3. Build and Run Containers
docker-compose build
docker-compose up -d

4. Apply Migrations
docker-compose exec web python manage.py migrate

5. Test API with Postman.
```
