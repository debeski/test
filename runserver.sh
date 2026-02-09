#!/bin/bash

# Kill process on port 8000
fuser -k 8000/tcp 2>/dev/null || true

# Activate virtual environment
source venv/bin/activate

# Uninstall microsys if it exists
echo "Checking for existing microsys installation..."
if pip show microsys 2>/dev/null | grep -q "Name:"; then
    echo "Uninstalling microsys..."
    pip uninstall -y microsys 2>/dev/null || true
fi

# Also check for any residual files
echo "Cleaning up residual files..."
find venv/lib/python*/site-packages -name "*microsys*" -type d -exec rm -rf {} + 2>/dev/null || true
find venv/lib/python*/site-packages -name "*microsys*" -type f -delete 2>/dev/null || true

# Reinstall the package
echo "Reinstalling microsys..."
pip install --upgrade --no-deps --force-reinstall /home/debeski/xPy/microsys-pkg

# Run Django migrations
echo "Running makemigrations..."
python manage.py makemigrations

echo "Running migrate..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser..."
DJANGO_SUPERUSER_PASSWORD=db123123 python manage.py createsuperuser --noinput --username admin --email admin@example.com 2>/dev/null || echo "Superuser already exists or creation failed"

# Run the server
echo "Starting development server..."
python manage.py runserver 0.0.0.0:8000