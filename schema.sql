-- Cinema network database: tables

create table customers (
    customer_id int generated always as identity primary key,
    customer_age int not null,
    customer_email varchar(100) unique not null,
    created_at timestamp default now()
);

-- one-to-one with customers
create table customer_profiles (
    customer_id int primary key,
    full_name varchar(100) not null,
    phone varchar(30),
    gender varchar(10),

    foreign key (customer_id) references customers(customer_id)
);

create table genres (
    genre_id int generated always as identity primary key,
    genre_name varchar(50) unique not null,
    movie_count int default 0   -- updated by a trigger
);

create table movies (
    movie_id int generated always as identity primary key,
    title varchar(150) not null,
    genre_id int,
    movie_age_rating varchar(10),
    movie_rating numeric(2,1),

    foreign key (genre_id) references genres(genre_id)
);

create table cinemas (
    cinema_id int generated always as identity primary key,
    cinema_name varchar(100),
    cinema_city varchar(50),
    employees_count int
);

create table halls (
    hall_id int generated always as identity primary key,
    cinema_id int not null,
    hall_number int not null,
    capacity int not null check (capacity > 0),

    foreign key (cinema_id) references cinemas(cinema_id)
);

create table sessions (
    session_id int generated always as identity primary key,
    movie_id int not null,
    hall_id int not null,
    session_time timestamp not null,
    price numeric(6,2) not null check (price >= 0),

    foreign key (movie_id) references movies(movie_id),
    foreign key (hall_id) references halls(hall_id)
);

create table tickets (
    ticket_id int generated always as identity primary key,
    customer_id int not null,
    session_id int not null,
    quantity int not null default 1 check (quantity > 0),

    foreign key (customer_id) references customers(customer_id),
    foreign key (session_id) references sessions(session_id)
);

create table payments (
    payment_id int generated always as identity primary key,
    ticket_id int unique not null,
    amount numeric(8,2) not null,
    payment_method varchar(20) not null,
    payment_status varchar(20) not null,
    payment_last_update_time timestamp not null,

    foreign key (ticket_id) references tickets(ticket_id)
);

create table discounts (
    discount_id int generated always as identity primary key,
    discount_name varchar(100),
    discount_percent numeric(5,2) not null,
    description text
);





-- many-to-many: one discount can be used in many tickets
-- and one ticket can have several discounts
create table ticket_discounts (
    ticket_id int not null,
    discount_id int not null,

    primary key (ticket_id, discount_id),

    foreign key (ticket_id) references tickets(ticket_id),
    foreign key (discount_id) references discounts(discount_id)
);

create table reviews (
    review_id int generated always as identity primary key,
    customer_id int not null,
    movie_id int not null,
    rating numeric(2,1) check (rating >= 0 and rating <= 5),
    review_text text,
    created_at timestamp,

    foreign key (customer_id) references customers(customer_id),
    foreign key (movie_id) references movies(movie_id)
);