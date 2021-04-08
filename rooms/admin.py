from django.contrib import admin
from django.utils.html import (
    mark_safe,
)  # 내가 쓴 html 포멧을 보이게하려고 / 기본적으로는 장고가 다 막는다. 사용자들이 태그 넣으면 곤란해
from . import models


@admin.register(models.RoomType, models.Facility, models.HouseRule, models.Amenity)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = (  # rooms 에서 amenity 나 facility 들어갔을 때 보이는 화면의 리스트 명
        "name",
        "used_by",
    )

    def used_by(self, obj):
        return obj.rooms.count()


# admin 안에 admin 넣기 - 여기서 class 로 만들어서 밑에 있는 Room Admin에 넣을거
class PhotoInline(admin.TabularInline):

    model = (
        models.Photo
    )  # room admin에 photo admin 넣는거 / 장고가 자동으로 room의 foreign key 가지고 있는 이미지를 넣는다


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")},
        ),
        (
            "Times",
            {"fields": ("check_in", "check_out", "instant_book")},
        ),
        (
            "Spaces",
            {"fields": ("guests", "beds", "bedrooms", "baths")},
        ),
        (
            "More About the Space",
            {
                "classes": ("collapse",),  # 목록 길때 접을 수 있게해주는 기능!
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        (
            "Last Detail",
            {"fields": ("host",)},
        ),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    ordering = ("name", "price")  # 리스트 정렬 순서

    list_filter = (
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    raw_id_fields = (
        "host",
    )  # room에서 host(위에 있는 field set에서 있는 host) 찾을때 너무많으면 셀렉트박스로하면 불편, user-admin불러와서 검색가능하게해줌

    search_fields = ("city", "^host__username")  # forignkey 처럼 host에서 username 연결해서 찾아줌

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )  # filter_horizontal works in ManyToMany field

    # def save_model(self, request, obj, form, change): #admin을 다루는 save_model / medel에서 쓰이는 save랑 용도가 달라
    #     obj.user = request.user
    #     super().save_model(request, obj, form, change)

    def count_amenities(
        self, obj
    ):  # 여기서 self는 RoomAdmin class, object는 현재 row(room 객실)
        return obj.amenities.count()

    # count_amenities.short_description = "Hello" #정렬 리스트에서 보이는 이름을 변경하는 것, 클릭은 안됨, 함수니까

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"
