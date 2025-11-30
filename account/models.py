from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password = None, **extra_fields):
        if not phone:
            raise ValueError("Foydalanuvchi telefon raqamini kiritshi muajburiy")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, phone, password = None, **extra_fields): 
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not password:
            raise ValueError("Superuser uchun parol majburiy")

        return self.create_user(phone, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    profession = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='users', blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    @property
    def fullname(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.phone

    def __str__(self):
        return self.fullname

class CourseType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'course_type'
        verbose_name_plural = 'course_types'
        db_table = 'course_type'


class Course(models.Model):
    name = models.CharField(max_length=70)
    price = models.PositiveIntegerField()
    course_type = models.ForeignKey('CourseType', on_delete=models.SET_NULL, related_name='courses', null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - {self.price}'

    class Meta:
        verbose_name = 'course'
        verbose_name_plural = 'courses'
        db_table = 'course'

class AdminTeacher(models.Model):
    ROLE = (
        ('admin', 'Admin'),
        ('main_teacher', 'Main teacher'),
        ('assistant_teacher', 'Assistant teacher'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin_teachers')
    role = models.CharField(max_length=20, choices=ROLE)
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.fullname} - {self.role}"


    class Meta:
        verbose_name = 'admin_teacher'
        verbose_name_plural = 'admin_teachers'
        db_table = 'admin_teacher'


class Student(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='students')
    gender = models.CharField(max_length=1, choices=GENDER)
    year = models.PositiveIntegerField(validators=[MinValueValidator(2000)])
    level = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(11)])
    xp = models.PositiveBigIntegerField(default=0)
    coins = models.PositiveBigIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.fullname


    class Meta:
        verbose_name = 'student'
        verbose_name_plural = 'students'
        db_table = 'student'

