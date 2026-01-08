"""
Management command to generate username, password and key_digest for all students.
Usage: python manage.py generate_key_digests [--password PASSWORD]
If no password is provided, defaults to 'password123' (10+ characters) for testing.
"""
from django.core.management.base import BaseCommand
from estudiantes.models import Student
import hashlib
import random
import string


class Command(BaseCommand):
    help = 'Generate username, password and key_digest for all students using username@password format with SHA256'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            type=str,
            default='password123',
            help='Password to use for all students (default: password123, must be 10+ characters)'
        )

    def generate_username(self, student):
        """Generate a unique username based on student data"""
        # Try to create username from name and enrollment number
        base_username = f"{student.name.lower().replace(' ', '')}{student.enrollment_number}"
        # Remove special characters and keep only alphanumeric
        base_username = ''.join(c for c in base_username if c.isalnum())
        
        # Ensure uniqueness
        username = base_username
        counter = 1
        while Student.objects.filter(username=username).exclude(pk=student.pk).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        return username

    def handle(self, *args, **options):
        password = options['password']
        
        if len(password) < 10:
            self.stdout.write(
                self.style.ERROR('Password must be at least 10 characters long.')
            )
            return
        
        students = Student.objects.all()
        
        if not students.exists():
            self.stdout.write(self.style.WARNING('No students found in database.'))
            return
        
        updated_count = 0
        for student in students:
            # Generate username if it doesn't exist
            if not student.username:
                student.username = self.generate_username(student)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Generated username for student {student.enrollment_number}: {student.username}'
                    )
                )
            
            # Set password (same for all students)
            student.password = password
            
            # Generate hash: SHA256(username@password)
            combined = f"{student.username}@{password}"
            key_digest = hashlib.sha256(combined.encode('utf-8')).hexdigest()
            student.key_digest = key_digest
            
            # Save all changes
            student.save(update_fields=['username', 'password', 'key_digest'])
            updated_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Updated student {student.enrollment_number} - Username: {student.username}, Key Digest: {key_digest[:16]}...'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully updated {updated_count} student(s) with username, password and key_digest.'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'All students use password: {password}'
            )
        )
