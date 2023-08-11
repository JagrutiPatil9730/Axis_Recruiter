# Import the UserProfile model
from .models import UserProfile

# Delete rows with NULL pdf_file values
UserProfile.objects.filter(pdf_file__isnull=True).delete()
