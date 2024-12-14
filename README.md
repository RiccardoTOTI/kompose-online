# Kompose Online 🚀

[![Deploy to Heroku](https://github.com/RiccardoTOTI/kompose-online/actions/workflows/deploy.yml/badge.svg)](https://github.com/RiccardoTOTI/kompose-online/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/)
[![Heroku](https://img.shields.io/badge/Heroku-Deployed-430098.svg)](https://kompose-online-d6bdfcec7843.herokuapp.com)

> A modern web interface for converting Docker Compose files to Kubernetes/Helm charts using [Kompose](https://kompose.io/)

![Kompose Logo](https://kompose.io/assets/images/logo.png)

## 🌟 Features

- 📤 Upload Docker Compose files or paste YAML content directly
- ✨ Real-time YAML validation
- 🔄 Convert Docker Compose to Kubernetes/Helm charts
- ⬇️ Download generated Kubernetes manifests
- 🎨 Modern, responsive UI
- 🔒 Secure file handling and conversion
- 🚦 Rate limiting and CSRF protection
- 📱 Mobile-friendly design

## 🚀 Live Demo

Try it out: [Kompose Online](https://kompose-online-d6bdfcec7843.herokuapp.com)

## 🛠️ Technology Stack

- **Backend**: Python 3.9, Flask
- **Security**: Flask-Talisman, Flask-SeaSurf
- **Container**: Docker, Gunicorn
- **CI/CD**: GitHub Actions
- **Deployment**: Heroku
- **Converter**: Kompose

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Kompose CLI (installed automatically in container)

## 🏃‍♂️ Quick Start

### Local Development

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

### Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
cp config.env.example config.env
# Edit config.env with your settings
```

3. Run the application:
```bash
python app.py
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| FLASK_ENV | Environment (development/production) | development |
| MAX_CONTENT_LENGTH | Maximum file upload size | 16MB |
| RATE_LIMIT | API rate limit per minute | 30 |
| SECRET_KEY | Flask secret key | Auto-generated |

## 🔐 Security Features

- HTTPS enforcement in production
- CSRF protection
- Rate limiting
- Content Security Policy
- File size restrictions
- Input validation
- Non-root container user

## 🚀 Deployment

### Automatic Deployment

The application automatically deploys to Heroku via GitHub Actions when pushing to the main branch.

### Manual Deployment

1. Install Heroku CLI
2. Login to Heroku:
```bash
heroku login
heroku container:login
```

3. Create a new app:
```bash
heroku create your-app-name
heroku stack:set container
```

4. Set environment variables:
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key
```

5. Deploy:
```bash
git push heroku main
```

## 📦 Release Process

New releases are automatically created via GitHub Actions when pushing to main:
- Version format: YYYY.MM.DD-commit_hash
- Release notes from commit messages
- Automatic deployment to Heroku

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Riccardo TOTI**
- GitHub: [@RiccardoTOTI](https://github.com/RiccardoTOTI)

## 🙏 Acknowledgments

- [Kompose](https://kompose.io/) team for the amazing conversion tool
- [Flask](https://flask.palletsprojects.com/) framework
- [Heroku](https://www.heroku.com/) for hosting
