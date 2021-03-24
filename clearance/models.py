from django.core.validators import MaxValueValidator, MinValueValidator
from .validators import validate_file_extension
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    USER_TYPE = ((1, "Admin"), (2, "Officer"), (3, "Student"))
    first_name = None
    last_name = None
    username = None  # Removed username, using email instead
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Department(models.Model):
    name = models.CharField(max_length=70, unique=True)

    def __str__(self):
        return self.name


class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return "Admin : " + str(self.admin)


class Officer(models.Model):
    name = models.CharField(max_length=70)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    GENDER = [("M", "Male"), ("F", "Female")]
    fullname = models.CharField(max_length=70)
    phone = models.CharField(max_length=11, unique=True)
    regno = models.CharField(max_length=10, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)
    picture = models.ImageField(upload_to="students/")
    direct_entry = models.BooleanField(default=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    cleared = models.BooleanField(default=False)

    def __str__(self):
        return self.fullname

    @property
    def department_name(self):
        return self.category.name


class Document(models.Model):
    USERS = [('1', "UTME"), ('2', "DE"), ('3', "UTME/DE")]
    name = models.CharField(max_length=60, unique=True)
    category = models.CharField(max_length=1, choices=USERS, default=1)

    def __str__(self):
        return self.name


class Upload(models.Model):
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE)
    file = models.FileField(upload_to="documents",  validators=[
                            validate_file_extension])
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    remark = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('document', 'student'),)

    def __str__(self):
        return str(self.student) + " uploaded " + str(self.document)
