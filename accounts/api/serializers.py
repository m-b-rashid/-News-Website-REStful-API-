from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField, CharField, ValidationError
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()

class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name',
            'password',
            'email',
            'phoneNum'
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        name = validated_data['name']
        password = validated_data['password']
        email = validated_data['email']
        phoneNum = validated_data['phoneNum']
        user_obj = User(name=name,email=email, phoneNum=phoneNum)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True) #placeholder for token
    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'token'
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        user_obj = None
        email = data.get("email", None)
        password = data["password"]
        if not email:
            raise ValidationError("An email is required to login")
        user = User.objects.filter(
        Q(email=email)
        ).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("email not valid")
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("incorrect credentials")
        data["token"] = "sopmvjhvjhb"
        return data

class UserDetailSerializer(ModelSerializer):
    avatar = SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'phoneNum',
            'date_joined',
            'is_staff',
            'avatar'
        ]

    def get_avatar(self, obj):
        try:
            avatar = obj.avatar.url
        except:
            avatar = None
        return avatar
