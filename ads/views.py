import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Avg, Max, Min, Count, Q, F
from django.http import JsonResponse
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, UpdateView, ListView, CreateView, DeleteView

from rest_framework.generics import RetrieveAPIView, ListAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ad, AdUser, Location, Selection
from ads.permissions import IsSelectionOwner, IsAdAuthorOrStaff
from ads.serializers import AdUserDetailSerializer, AdUserListSerializer, AdUserDestroySerializer, \
    AdUserCreateSerializer, AdUserUpdateSerializer, AdDetailSerializer, LocationModelSerializer, \
    SelectionListSerializer, SelectionDetailSerializer, SelectionCreateSerializer, \
    SelectionUpdateSerializer, SelectionDestroySerializer, AdListSerializer, AdDestroySerializer, AdUpdateSerializer, \
    AdCreateSerializer
from avito import settings


def root(request):
    return JsonResponse({
        "status": "ok"
    })


# Category
class CategoryListView(ListView):
    """
    Список категорий, с сортировкой по названию категории, с пагинатором и
    итоговой информацией
    """
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("name")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        categories = []
        for category in page_obj:
            categories.append(
                {
                    "id": category.pk,
                    "name": category.name
                }
            )

        response = {
            "items": categories,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)


class CategoryDetailView(DetailView):
    """
    Детальная информация по выбранной категории
    """
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.pk,
            "name": category.name
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    """
    Создание новой категории
    """
    model = Category
    # fields здесь и далее не критичен, т.к. не используем templates.
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)
        category_new = Category.objects.create(**category_data)

        return JsonResponse({
            "id": category_new.pk,
            "name": category_new.name
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    """
    Обновление данных по категории
    """
    model = Category
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)

        self.object.name = category_data["name"]
        self.object.is_active = category_data["is_active"]

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name,
            "is_active": self.object.is_active
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    """
    Удаление объявления
    """
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        categ = self.get_object()
        categ_pk = categ.pk
        super().delete(request, *args, **kwargs)
        return JsonResponse({"id deleted": categ_pk}, status=200)


#########################################
# Ad


class AdDetailView(RetrieveAPIView):
    """
    Детальная информация по выбранному объявлению, доступна при аутентификации пользователя по токену.
    """
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [IsAuthenticated]


class AdListView(ListAPIView):
    """
    Список всех объявлений
    """
    queryset = Ad.objects.annotate(
        location_names=F('author__location_names__name')
    ).order_by("-price")
    serializer_class = AdListSerializer
    permission_classes = [AllowAny]


class AdCreateView(CreateAPIView):
    """
    Создание нового объявления
    """
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer
    permission_classes = [IsAuthenticated]


class AdUpdateView(UpdateAPIView):
    """
    Обновление данных по объявлению
    """
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdAuthorOrStaff]


@method_decorator(csrf_exempt, name="dispatch")
class AdImageView(UpdateView):
    """
    Добавление/обновление картинки в объявлении
    """
    model = Ad
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get("image")
        self.object.save()

        return JsonResponse({
                    "id": self.object.pk,
                    "name": self.object.name,
                    "image": self.object.image.url if self.object.image else None
                })


class AdDeleteView(DestroyAPIView):
    """
    Удаление объявления
    """
    queryset = Ad.objects.all()
    serializer_class = AdDestroySerializer
    permission_classes = [IsAuthenticated, IsAdAuthorOrStaff]


####################
# User

class LocationViewSet(ModelViewSet):
    """
    Класс с адресами на основе ViewSet с использованием Router и сериализатора
    """
    queryset = Location.objects.all()
    serializer_class = LocationModelSerializer


class AdUserListView(ListAPIView):
    """
    Список пользователей, с сортировкой по username. Queryset выводит дополнительно кол-во
    объявлений со статусом is_published по каждому из списка пользователей.
    """
    queryset = AdUser.objects.annotate(
        total_ads=Count("ads", filter=Q(ads__is_published=True))
    ).order_by("username")
    serializer_class = AdUserListSerializer


class AdUserDetailView(RetrieveAPIView):
    """
    Детальная информация по выбранному пользователю
    """
    queryset = AdUser.objects.annotate(
        total_ads=Count("ads", filter=Q(ads__is_published=True))
    )
    serializer_class = AdUserDetailSerializer


class AdUserCreateView(CreateAPIView):
    """
    Создание нового пользователя
    """
    queryset = AdUser.objects.all()
    serializer_class = AdUserCreateSerializer


class AdUserUpdateView(UpdateAPIView):
    """
    Обновление данных по пользователю
    """
    queryset = AdUser.objects.all()
    serializer_class = AdUserUpdateSerializer


class AdUserDeleteView(DestroyAPIView):
    """
    Удаление пользователя
    """
    queryset = AdUser.objects.all()
    serializer_class = AdUserDestroySerializer


#######################
class SelectionListView(ListAPIView):
    """
    Класс для списка подборок
    """
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer


class SelectionDetailView(RetrieveAPIView):
    """
    Детальная информация по подборкам выбранного пользователя
    """
    queryset = Selection.objects.annotate(
        location_names=F('owner__location_names__name')
    )
    serializer_class = SelectionDetailSerializer


class SelectionCreateView(CreateAPIView):
    """
    Создание новой подборки
    """
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated]


class SelectionUpdateView(UpdateAPIView):
    """
    Обновление данных по подборке
    """
    queryset = Selection.objects.all()
    serializer_class = SelectionUpdateSerializer
    permission_classes = [IsAuthenticated, IsSelectionOwner]


class SelectionDeleteView(DestroyAPIView):
    """
    Удаление подборки
    """
    queryset = Selection.objects.all()
    serializer_class = SelectionDestroySerializer
    permission_classes = [IsAuthenticated, IsSelectionOwner]

