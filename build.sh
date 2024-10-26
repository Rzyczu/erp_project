#!/usr/bin/env bash
# Exit on error
set -o errexit

er (pip, poetry, etc.)
pip install -r # Modify this line as needed for your package managrequirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate