from sqlalchemy.exc import SQLAlchemyError
from ckanext.pages.db import MainPage  # Replace with the actual module containing your MainPage class
from ckan import model

def insert_main_page_rows():
    rows = [
        MainPage(
            id=1,

        ),
        MainPage(
            id=2,

        ),
        MainPage(
            id=3,

        ),
        MainPage(
            id=4,

        ),
        MainPage(
            id=5,

        ),
    ]

    # Insert the data into the database
    try:
        for row in rows:
            model.Session.add(row)
        model.Session.commit()
        print("Rows inserted successfully!")
    except SQLAlchemyError as e:
        model.Session.rollback()
        print(f"Error inserting rows: {e}")

