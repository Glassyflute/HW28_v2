from rest_framework import serializers

from ads.models import AdUser, Location, Ad, Selection, Category


class LocationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


#### AdUser
class AdUserListSerializer(serializers.ModelSerializer):
    location_names = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    total_ads = serializers.IntegerField()

    class Meta:
        model = AdUser
        exclude = ['password']


class AdUserDetailSerializer(serializers.ModelSerializer):
    location_names = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    total_ads = serializers.IntegerField()

    class Meta:
        model = AdUser
        exclude = ['password']


class AdUserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    location_names = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = AdUser
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self._location_names = self.initial_data.pop("location_names", [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        new_user = AdUser.objects.create(**validated_data)

        for loc_item in self._location_names:
            loc_obj, _ = Location.objects.get_or_create(name=loc_item)
            new_user.location_names.add(loc_obj)

        new_user.set_password(new_user.password)
        new_user.save()

        return new_user


class AdUserUpdateSerializer(serializers.ModelSerializer):
    location_names = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = AdUser
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self._location_names = self.initial_data.pop("location_names")
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        user_upd = super().save()

        for loc_item in self._location_names:
            loc_obj, _ = Location.objects.get_or_create(name=loc_item)
            user_upd.location_names.add(loc_obj)

        user_upd.save()
        return user_upd


class AdUserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdUser
        fields = ["id"]


######  Ad
class AdListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        queryset=AdUser.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Category.objects.all()
    )

    location_names = serializers.CharField()

    class Meta:
        model = Ad
        fields = ["id", "name", "price", "description", "image", "is_published", "author", "category", "location_names"]


class AdDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name"
    )

    location_names = serializers.SerializerMethodField()

    def get_location_names(self, ad):
        return [location_elem.name for location_elem in ad.author.location_names.all()]

    class Meta:
        model = Ad
        fields = '__all__'


class AdCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ["id"]



######## Selection serializers
class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id", "name"]


class SelectionDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    location_names = serializers.CharField()
    # items = AdListSerializer(many=True)

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["owner"] = request.user
        return super().create(validated_data)

    class Meta:
        model = Selection
        exclude = ['owner']


class SelectionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'


class SelectionDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id"]

