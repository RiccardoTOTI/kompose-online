# Kompose Online

A web application that provides an online interface for converting Docker Compose files to Kubernetes/Helm charts using [Kompose](https://kompose.io/).

## Features

- Upload Docker Compose files or paste YAML content directly
- Real-time YAML validation
- Convert Docker Compose to Kubernetes/Helm charts
- Download generated Kubernetes manifests
- Modern, responsive UI
- Secure file handling and conversion

## Development

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Kompose

### Running Locally

1. Clone the repository:
```bash
git clone https://github.com/RiccardoTOTI/kompose-online.git
cd kompose-online
```

2. Run with Docker Compose:
```bash
docker-compose up --build
```

The application will be available at http://localhost:5000

### Environment Variables

- `FLASK_ENV`: Set to 'development' or 'production'
- `SECRET_KEY`: Flask secret key for session management
- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 16MB)
- `RATE_LIMIT`: API rate limit per minute (default: 30)

## Deployment

The application is configured for deployment on Heroku:

1. Install Heroku CLI
2. Login to Heroku
3. Create a new app and set it to container stack
4. Push the code to Heroku

## Security

- HTTPS enforcement in production
- CSRF protection
- Rate limiting
- Content Security Policy
- File size restrictions
- Input validation

## License

MIT

## Author

[Riccardo TOTI](https://github.com/RiccardoTOTI)
