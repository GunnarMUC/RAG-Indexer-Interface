# Technical Documentation

## API Reference

### Authentication
The API uses OAuth 2.0 for authentication. Users must provide valid credentials to access protected endpoints.

### Endpoints
- GET /api/users - Retrieve user list
- POST /api/users - Create new user
- PUT /api/users/{id} - Update user
- DELETE /api/users/{id} - Delete user

## Configuration

### Database Settings
- Host: localhost
- Port: 5432
- Database: myapp_prod

### Security
- JWT tokens expire after 24 hours
- Rate limiting: 100 requests per minute 