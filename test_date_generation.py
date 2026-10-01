import random
import psycopg2
import uuid
from psycopg2.extras import execute_values
from faker import Faker

fake = Faker()


conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="",
    dbname="as4",
    port="5432"
)

cur = conn.cursor()

def insert_customers():
    data = []

    for _ in range(10000):
        data.append((
            random.randint(13, 80),
            fake.email().split("@")[0] + str(uuid.uuid4())[:8] + "@mail.com"
        ))

    execute_values(
        cur,
        "INSERT INTO customers (customer_age, customer_email) VALUES %s",
        data
    )

    cur.execute("SELECT customer_id FROM customers")
    return [row[0] for row in cur.fetchall()]


def insert_customer_profiles(customer_ids):
    data = []

    for cid in customer_ids:
        data.append((
            cid,
            fake.name(),
            fake.phone_number(),
            random.choice(["Male", "Female"])
        ))

    execute_values(
        cur,
        "INSERT INTO customer_profiles (customer_id, full_name, phone, gender) VALUES %s",
        data
    )


def insert_genres():
    genres = ["Action", "Drama", "Comedy", "Horror", "Sci-Fi"]

    execute_values(
        cur,
        "INSERT INTO genres (genre_name) VALUES %s",
        [(g,) for g in genres]
    )

    cur.execute("SELECT genre_id FROM genres")
    return [row[0] for row in cur.fetchall()]

def insert_movies(genre_ids):
    data = []

    for _ in range(5000):
        data.append((
            fake.sentence(nb_words=3),
            random.choice(genre_ids),
            random.choice(["0+", "12+", "16+", "18+"]),
            round(random.uniform(1, 5), 1)
        ))

    execute_values(
        cur,
        "INSERT INTO movies (title, genre_id, movie_age_rating, movie_rating) VALUES %s",
        data
    )

    cur.execute("SELECT movie_id FROM movies")
    return [row[0] for row in cur.fetchall()]



def insert_cinemas():
    data = []

    for _ in range(10):
        data.append((
            fake.company(),
            fake.city(),
            random.randint(5, 50)
        ))

    execute_values(
        cur,
        "INSERT INTO cinemas (cinema_name, cinema_city, employees_count) VALUES %s",
        data
    )

    cur.execute("SELECT cinema_id FROM cinemas")
    return [row[0] for row in cur.fetchall()]

def insert_halls(cinema_ids):
    data = []

    for cinema_id in cinema_ids:
        for i in range(1, 4):
            data.append((
                cinema_id,
                i,
                random.randint(50, 200)
            ))

    execute_values(
        cur,
        "INSERT INTO halls (cinema_id, hall_number, capacity) VALUES %s",
        data
    )

    cur.execute("SELECT hall_id FROM halls")
    return [row[0] for row in cur.fetchall()]


def insert_sessions(movie_ids, hall_ids):
    data = []

    for _ in range(20000):
        data.append((
            random.choice(movie_ids),
            random.choice(hall_ids),
            fake.date_time_this_year(),
            round(random.uniform(5, 20), 2)
        ))

    execute_values(
        cur,
        "INSERT INTO sessions (movie_id, hall_id, session_time, price) VALUES %s",
        data
    )

    cur.execute("SELECT session_id FROM sessions")
    return [row[0] for row in cur.fetchall()]


def insert_tickets(customer_ids, session_ids):
    data = []

    for _ in range(700000):
        data.append((
            random.choice(customer_ids),
            random.choice(session_ids),
            random.randint(1, 5)
        ))

    execute_values(
        cur,
        "INSERT INTO tickets (customer_id, session_id, quantity) VALUES %s",
        data
    )

    cur.execute("SELECT ticket_id FROM tickets")
    return [row[0] for row in cur.fetchall()]


def insert_payments(ticket_ids):
    data = []

    for t in ticket_ids:
        data.append((
            t,
            round(random.uniform(100, 1000), 2),
            random.choice(["Cash", "Card"]),
            random.choice(["Paid", "Pending"]),
            fake.date_time_this_year()
        ))

    execute_values(
        cur,
        "INSERT INTO payments (ticket_id, amount, payment_method, payment_status, payment_last_apdate_time) VALUES %s",
        data
    )


def insert_discounts():
    data = [
        ("Student", 10, "student discount"),
        ("Weekend", 15, "weekend discount"),
        ("Promo", 20, "promo discount"),
        ("VIP", 25, "vip discount")
    ]

    execute_values(
        cur,
        "INSERT INTO discounts (discount_name, discount_percent, description) VALUES %s",
        data
    )

    cur.execute("SELECT discount_id FROM discounts")
    return [row[0] for row in cur.fetchall()]


def insert_ticket_discounts(ticket_ids, discount_ids):
    data = []

    for t in ticket_ids:
        if random.random() < 0.4:
            data.append((
                t,
                random.choice(discount_ids)
            ))

    execute_values(
        cur,
        "INSERT INTO ticket_discounts (ticket_id, discount_id) VALUES %s",
        data
    )


def insert_reviews(customer_ids, movie_ids):
    data = []

    for _ in range(5000):
        data.append((
            random.choice(customer_ids),
            random.choice(movie_ids),
            round(random.uniform(1, 5), 1),
            fake.text(max_nb_chars=100),
            fake.date_time_this_year()
        ))

    execute_values(
        cur,
        "INSERT INTO reviews (customer_id, movie_id, rating, review_text, created_at) VALUES %s",
        data
    )


def main():

    customer_ids = insert_customers()
    insert_customer_profiles(customer_ids)

    genre_ids = insert_genres()
    movie_ids = insert_movies(genre_ids)

    cinema_ids = insert_cinemas()
    hall_ids = insert_halls(cinema_ids)

    session_ids = insert_sessions(movie_ids, hall_ids)
    ticket_ids = insert_tickets(customer_ids, session_ids)

    insert_payments(ticket_ids)

    discount_ids = insert_discounts()
    insert_ticket_discounts(ticket_ids, discount_ids)

    insert_reviews(customer_ids, movie_ids)

    conn.commit()
    cur.close()
    conn.close()

    print("DONE ✔")


if __name__ == "__main__":
    main()