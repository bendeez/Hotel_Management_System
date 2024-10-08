from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


class HotelEntity(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int


class HotelReviewOut(HotelEntity):
    rating_out_of_10: Optional[float] = None
    staff_rating_out_of_10: Optional[float] = None
    facilities_rating_out_of_10: Optional[float] = None
    cleanliness_rating_out_of_10: Optional[float] = None
    comfort_rating_out_of_10: Optional[float] = None
    value_for_money_rating_out_of_10: Optional[float] = None
    location_rating_out_of_10: Optional[float] = None
    free_wifi_rating_out_of_10: Optional[float] = None
    num_of_reviews: Optional[int] = None
    subjective_rating: Optional[str] = None
    hotel_id: int


class HotelRoomsOut(HotelEntity):
    room_type: Optional[List[str]] = Field(default_factory=list)
    guest_count: Optional[List[str]] = Field(default_factory=list)
    price: Optional[List[str]] = Field(default_factory=list)
    guest_count_numeric: Optional[int]
    price_numeric: Optional[float]
    tax_and_fee_numeric: Optional[float]
    hotel_id: int


class HotelHouseRulesOut(HotelEntity):
    check_in: Optional[str] = None
    check_out: Optional[str] = None
    cancellation_payment: Optional[str] = None
    children_beds: Optional[str] = None
    age_restriction: Optional[str] = None
    pets: Optional[str] = None
    groups: Optional[str] = None
    refundable_damage_deposit: Optional[str] = None
    smoking: Optional[str] = None
    cards_accepted: Optional[str] = None
    hotel_id: int


class HotelLocationOut(HotelEntity):
    city: Optional[str] = None
    address: Optional[str] = None
    hotel_id: int


class HotelGuestReviewsOut(HotelEntity):
    date: Optional[str] = None
    title: Optional[str] = None
    positive: Optional[str] = None
    negative: Optional[str] = None
    hotel_id: int


class HotelsOut(HotelEntity):
    title: Optional[str] = None
    image_link: Optional[str] = None
    description: Optional[str] = None
    amenities: List[str] = Field(default_factory=list)
    hotel_review: Optional[HotelReviewOut] = None
    hotel_rooms: List[HotelRoomsOut] = Field(default_factory=list)
    hotel_house_rules: Optional[HotelHouseRulesOut] = None
    hotel_location: Optional[HotelLocationOut] = None
    hotel_guest_reviews: List[HotelGuestReviewsOut] = Field(default_factory=list)
