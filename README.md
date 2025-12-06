# Libro - Book Management System

A Django-based web application for managing books and authors. Libro provides a platform for users to browse, create, and manage books and their authors with features including user authentication, book reviews, and batch uploads.

## Features

- **Book Management**: Create, read, update, and delete books with detailed information
- **Author Management**: Manage author profiles with biographies, photos, and birth/death dates
- **User Authentication**: Custom user model with profile management
- **Reviews & Comments**: Users can add reviews and comments to books
- **Batch Uploads**: Import multiple books and authors via file uploads
- **User Profiles**: Customizable user profiles with contact information
- **Image Processing**: Automatic image processing for book covers and author photos
- **Search & Filtering**: Browse and filter books by various criteria
- **Responsive Design**: Mobile-friendly interface
- **Pagination**: Efficient browsing with paginated lists

## Tech Stack

- **Framework**: Django 5.1.6
- **Database**: SQLite (default)
- **Template Engine**: Django Templates
- **Image Processing**: Pillow
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Django's built-in authentication system

## Project Structure

```
libro/
├── accounts/              # User account management app
│   ├── models.py         # Custom user model
│   ├── forms.py          # User forms (signup, password change)
│   ├── views.py          # User views
│   ├── urls.py           # User-related URLs
│   └── templates/        # User templates
├── libro/                # Main app for books and authors
│   ├── models.py         # Book, Author, Genre, Review, Comment models
│   ├── views.py          # CRUD views for books and authors
│   ├── forms.py          # Book and author forms
│   ├── urls.py           # App URLs
│   ├── utils.py          # Utility functions for image processing
│   └── templates/        # Book and author templates
├── website/              # Public website pages
│   ├── views.py          # Home, About, Contact, Privacy, Terms views
│   ├── urls.py           # Website URLs
│   └── templates/        # Public page templates
├── django_project/       # Django project settings
│   ├── settings.py       # Project configuration
│   ├── urls.py           # URL routing
│   ├── wsgi.py           # WSGI configuration
│   └── asgi.py           # ASGI configuration
├── templates/            # Base templates
│   ├── base.html         # Base template
│   ├── includes/         # Template includes (navbar, footer, messages)
│   └── accounts/         # Account-related templates
├── static/               # Static files (CSS, JS, images)
├── media/                # User-uploaded files
│   ├── author_photos/    # Author profile photos
│   └── book_covers/      # Book cover images
├── data/                 # Sample data files (JSON, TXT)
├── scripts/              # Utility scripts
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## Installation

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd libro
   ```

2. **Create and activate virtual environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Create superuser** (admin account):

   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**:

   ```bash
   python manage.py runserver
   ```

The application will be available at `http://localhost:8000/`

## Usage

### Admin Interface

Access the Django admin panel at `/admin/` with your superuser credentials to:

- Manage users, books, authors, and genres
- Review user submissions
- Moderate reviews and comments

### Main Features

#### Books

- View all available books with pagination
- Filter and search books
- View detailed book information including cover, description, genres, and reviews
- Create/edit/delete your own books (authenticated users)
- Add reviews and comments to books

#### Authors

- Browse all authors
- View author profiles with biography and photo
- See all books by an author
- Create/edit/delete author entries
- Batch upload authors

#### User Accounts

- Sign up for a new account
- Update profile information (phone number, address, date of birth)
- Change password
- View public and private profiles

#### Website Pages

- **Home**: Featured books and navigation
- **About**: Information about Libro
- **Contact**: Contact information and form
- **Privacy**: Privacy policy
- **Terms**: Terms of service

## API & Views

### Book Views

- `BookListView`: List all books (with pagination)
- `BookDetailView`: View book details with reviews
- `BookCreateView`: Create a new book
- `BookUpdateView`: Edit a book
- `BookDeleteView`: Delete a book

### Author Views

- `AuthorListView`: List all authors
- `AuthorDetailView`: View author details and their books
- `AuthorCreateView`: Create a new author
- `AuthorUpdateView`: Edit author information
- `AuthorDeleteView`: Delete an author

### Batch Uploads

- `BookBatchUploadView`: Upload multiple books via file
- `AuthorBatchUploadView`: Upload multiple authors via file

## Database Models

### Book

- Title, slug, description
- Author and genres (many-to-many)
- ISBN, publication date
- Cover image
- Review count and average rating
- Creation metadata

### Author

- Name, slug, biography
- Birth/death dates
- Photo
- Created by (user)
- Creation and update timestamps

### Review

- Rating (1-5 stars)
- Review text
- Book and user association

### Comment

- Comment text
- User and review association

### CustomUser

- Extends Django's AbstractUser
- Phone number, date of birth, address
- Additional profile fields

### Genre

- Name and description
- Used to categorize books

## Configuration

### Settings (`django_project/settings.py`)

Key settings:

- `DEBUG = True` (development only)
- `INSTALLED_APPS`: Includes Django apps and custom apps
- `DATABASES`: SQLite configuration
- `MEDIA_URL` and `MEDIA_ROOT`: User uploads configuration
- `STATIC_URL` and `STATIC_ROOT`: Static files configuration

### Environment Variables

For production, consider using environment variables for:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode flag
- `ALLOWED_HOSTS`: Allowed domain names
- Database credentials (if using production DB)

## Development

### Running Tests

```bash
python manage.py test
```

### Making Database Changes

1. Create migrations:

   ```bash
   python manage.py makemigrations
   ```

2. Apply migrations:

   ```bash
   python manage.py migrate
   ```

### Creating Sample Data

Load sample data from included JSON files:

```bash
python manage.py loaddata data/authors.json
python manage.py loaddata data/jane-austen-books.json
```

## To-Do

- [ ] Implement image cropping and thumbnailing after upload
- [ ] Enhance batch upload functionality
- [ ] Add web scraping for authors and books from online sources
- [ ] Implement advanced search filters
- [ ] Add rating system improvements

## Dependencies

See `requirements.txt` for a complete list. Main dependencies:

- **Django**: Web framework
- **Pillow**: Image processing
- **django-cleanup**: Automatic file cleanup
- **django-widget-tweaks**: Template utilities
- **requests**: HTTP library (for potential API integration)

## Security Considerations

⚠️ **For Production**:

- Set `DEBUG = False`
- Use a strong, unique `SECRET_KEY`
- Configure `ALLOWED_HOSTS` properly
- Use environment variables for sensitive settings
- Set up HTTPS/SSL
- Use a production-grade database (PostgreSQL, MySQL)
- Configure CORS if needed
- Set proper file upload restrictions

## License

[Add appropriate license information]

## Contributing

[Add contribution guidelines if applicable]

## Support

For issues, questions, or feature requests, please [add contact method or issue tracker link].
