from django.contrib import admin
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


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    fieldsets = (
        (
            "Spaces",
            {"fields": ("guests", "beds", "bedrooms", "baths")},
        ),
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        (
            "Times",
            {"fields": ("check_in", "check_out", "instant_book")},
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

    search_fields = ("city", "^host__username")  # forignkey 처럼 host에서 username 연결해서 찾아줌

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )  # filter_horizontal works in ManyToMany field

    def count_amenities(
        self, obj
    ):  # 여기서 self는 RoomAdmin class, object는 현재 row(room 객실)
        return obj.amenities.count()

    # count_amenities.short_description = "Hello" #정렬 리스트에서 보이는 이름을 변경하는 것, 클릭은 안됨, 함수니까

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    pass