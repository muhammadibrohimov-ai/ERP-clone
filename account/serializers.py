from rest_framework import serializers
from .models import CustomUser, Course, CourseType, AdminTeacher, Student


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
    )

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['id', 'xp', 'coins', 'level', 'is_active']


class AdminTeacherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
    )


    class Meta:
        model = AdminTeacher
        fields = '__all__'
        read_only_fields = ['id', 'is_active',]




from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    profession = serializers.CharField(max_length=100, required=False)
    image = serializers.ImageField(required=False)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'first_name', 'last_name', 'profession',
            'phone', 'email', 'image', 'password'
        ]
        read_only_fields = ['id']


    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError("Password must contain at least 8 characters.")

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        if not (has_upper and has_lower and has_digit and has_special):
            raise serializers.ValidationError(
                "Password must include uppercase, lowercase, digit, and special character."
            )

        if self.instance and self.instance.check_password(password):
            raise serializers.ValidationError("New password cannot be same as old password.")

        return password


    def validate_phone(self, phone):
        if not (phone.startswith('+998') or phone.startswith('998')):
            raise serializers.ValidationError("Phone must start with +998 or 998.")

        if phone.startswith('+998'):
            if len(phone) != 13 or not phone[1:].isdigit():
                raise serializers.ValidationError("Invalid phone format.")
            phone = phone

        if phone.startswith('998'):
            if len(phone) != 12 or not phone.isdigit():
                raise serializers.ValidationError("Invalid phone format.")

        qs = CustomUser.objects.exclude(id=self.instance.id if self.instance else None)
        if qs.filter(phone=phone).exists():
            raise serializers.ValidationError("This phone number is already registered.")

        return phone

    def validate_email(self, email):
        allowed_domains = ('gmail.com', 'yahoo.com', 'yandex.ru', 'mail.ru')
        if not email.endswith(allowed_domains):
            raise serializers.ValidationError(
                "Email must end with gmail.com, yahoo.com, yandex.ru or mail.ru."
            )

        try:
            username, domain = email.split('@')
        except ValueError:
            raise serializers.ValidationError("Invalid email format.")

        if len(username) < 5:
            raise serializers.ValidationError("Email username must be at least 5 characters.")

        if not username[0].isalpha():
            raise serializers.ValidationError("Email must start with a letter.")

        allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-")
        if any(c not in allowed_chars for c in username):
            raise serializers.ValidationError(
                "Email username can contain only letters, digits, dot, underscore or dash."
            )

        qs = CustomUser.objects.exclude(id=self.instance.id if self.instance else None)
        if qs.filter(email=email).exists():
            raise serializers.ValidationError("This email is already registered.")

        return email


    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("First name cannot be empty.")

        cleaned = value.replace("'", "").replace("’", "")
        if not cleaned.isalpha():
            raise serializers.ValidationError("First name must contain only letters.")

        return value


    def validate_last_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Last name cannot be empty.")

        cleaned = value.replace("'", "").replace("’", "")
        if not cleaned.isalpha():
            raise serializers.ValidationError("Last name must contain only letters.")

        return value


    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class CourseSerializer(serializers.ModelSerializer):
    course_type = serializers.PrimaryKeyRelatedField(
        queryset=CourseType.objects.all()
    )

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['id', 'is_active']


class CourseTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseType
        fields = ['name']