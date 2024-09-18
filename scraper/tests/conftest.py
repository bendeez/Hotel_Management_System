import pytest
import pandas as pd
from hotel_data.data_cleaner.hotel_data_cleaner_tool import ht
from hotel_data.database import SessionLocal
from hotel_data.hotel_data_deleter import delete_hotel_data


@pytest.fixture(scope="session")
async def db():
    async with SessionLocal() as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
async def delete_data(db):
    await delete_hotel_data()


@pytest.fixture()
def create_df():
    def _create_df(csv_filename):
        df = pd.read_csv(csv_filename)
        return df

    return _create_df


@pytest.fixture()
def sort_guest_reviews():
    def _sort_guest_reviews(guest_reviews):
        return sorted(
            guest_reviews,
            key=lambda v: (
                v["positive"] or "",
                v["negative"] or "",
                v["review_title"] or "",
                v["review_date"] or "",
            ),
        )

    return _sort_guest_reviews


@pytest.fixture()
def hotel_cleaned_df(create_df, sort_guest_reviews):
    df = create_df(csv_filename="./tests/data/hotels_cleaned_sample.csv")
    df["amenities"] = df["amenities"].apply(ht.safe_literal_eval).apply(sorted)
    df["house_rules"] = (
        df["house_rules"]
        .apply(ht.safe_literal_eval)
        .apply(lambda v: dict(sorted(v.items())))
    )
    df["guest_reviews"] = (
        df["guest_reviews"]
        .apply(ht.safe_literal_eval)
        .apply(lambda values: [dict(sorted(v.items())) for v in values])
        .apply(sort_guest_reviews)
    )
    df["rooms_to_price"] = df["rooms_to_price"].apply(ht.safe_literal_eval)
    return df


@pytest.fixture()
def hotel_uncleaned_df(create_df):
    df = create_df(csv_filename="./tests/data/hotels_uncleaned_sample.csv")
    return df


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"
