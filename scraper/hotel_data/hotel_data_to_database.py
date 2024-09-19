import pandas as pd
from hotel_data.database import SessionLocal
from hotel_data.models import (
    Hotels,
    Hotel_Rooms,
    Hotel_Location,
    Hotel_Review,
    Hotel_Guest_Reviews,
    Hotel_House_Rules,
)
import asyncio
import numpy as np


async def sync_hotel_data_to_database(df):
    df = df.replace({np.nan: None})
    async with SessionLocal() as db:
        for index, hotel in df.iterrows():
            rooms_to_price = hotel["rooms_to_price"]
            hotel_rooms = (
                [
                    Hotel_Rooms(
                        room_type=room.get("room_type"),
                        price=room.get("price"),
                        guest_count=room.get("guest_count"),
                    )
                    for room in rooms_to_price
                    if isinstance(room, dict)
                ]
                if isinstance(rooms_to_price, list)
                else []
            )
            hotel_review = Hotel_Review(
                subjective_rating=hotel["subjective_rating"],
                num_of_reviews=hotel["num_of_reviews"],
                staff_rating_out_of_10=hotel["staff_rating_out_of_10"],
                facilities_rating_out_of_10=hotel["facilities_rating_out_of_10"],
                cleanliness_rating_out_of_10=hotel["cleanliness_rating_out_of_10"],
                comfort_rating_out_of_10=hotel["comfort_rating_out_of_10"],
                value_for_money_rating_out_of_10=hotel[
                    "value_for_money_rating_out_of_10"
                ],
                rating_out_of_10=hotel["rating_out_of_10"],
                location_rating_out_of_10=hotel["location_rating_out_of_10"],
                free_wifi_rating_out_of_10=hotel["free_wifi_rating_out_of_10"],
            )
            house_rules = hotel["house_rules"]
            hotel_house_rules = (
                Hotel_House_Rules(
                    check_in=house_rules.get("Check-in"),
                    check_out=house_rules.get("Check-out"),
                    cancellation_payment=house_rules.get("Cancellation/ prepayment"),
                    children_beds=house_rules.get("Children & Beds"),
                    age_restriction=house_rules.get("Age restriction"),
                    groups=house_rules.get("Groups"),
                    pets=house_rules.get("Pets"),
                    smoking=house_rules.get("Smoking"),
                    cards_accepted=house_rules.get("Cards accepted at this hotel"),
                    refundable_damage_deposit=house_rules.get(
                        "Refundable damage deposit"
                    ),
                )
                if isinstance(house_rules, dict)
                else None
            )
            guest_reviews = hotel["guest_reviews"]
            hotel_guest_reviews = (
                [
                    Hotel_Guest_Reviews(
                        date=review.get("review_date"),
                        title=review.get("review_title"),
                        positive=review.get("positive"),
                        negative=review.get("negative"),
                    )
                    for review in guest_reviews
                    if review is not None
                ]
                if isinstance(guest_reviews, list)
                else []
            )
            hotel_location = Hotel_Location(
                city=hotel["city"], address=hotel["address"]
            )
            hotel_data = Hotels(
                title=hotel["title"],
                image_link=hotel["image_link"],
                description=hotel["description"],
                amenities=hotel["amenities"],
                hotel_rooms=hotel_rooms,
                hotel_review=hotel_review,
                hotel_location=hotel_location,
                hotel_house_rules=hotel_house_rules,
                hotel_guest_reviews=hotel_guest_reviews,
            )
            db.add(hotel_data)
        await db.commit()


if __name__ == "__main__":
    conformation = input(
        "Are you sure you want to sync the hotel csv file to the database? (y/n): "
    )
    if conformation.lower() == "y":
        df = pd.read_csv("./hotel_data/data/hotels_cleaned_sample.csv")
        asyncio.run(sync_hotel_data_to_database(df=df))
