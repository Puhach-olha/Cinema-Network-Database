-- Cinema network database:  users, view, procedure, trigger, index



--      INDEX
CREATE INDEX idx_ticket_discounts_composite ON ticket_discounts(discount_id, ticket_id);

--          USERS
-- passwords are just for local testing

-- cashier
create role shop_assistant login password 'cashier123';
grant select on movies to shop_assistant;
grant select on sessions to shop_assistant;
grant select on halls to shop_assistant;
grant select on discounts to shop_assistant;
grant select, insert, update on tickets to shop_assistant;
grant select, insert, update on payments to shop_assistant;

-- local cinema manager
create role local_manager login password 'local123';
grant select on genres, movies, cinemas, halls, sessions, tickets, payments, discounts, ticket_discounts, reviews to local_manager;
grant update (employees_count) on cinemas to local_manager;

-- global manager
create role global_manager login password 'global123';
grant select on customer_profiles, genres, movies, cinemas, halls, sessions, tickets, payments, discounts, ticket_discounts, reviews to global_manager;
grant select, insert, update on genres, movies, cinemas, halls, sessions, discounts, reviews to global_manager;


--        VIEW
-- reviews with rating greater than 4
create view reviews_view
as
select rating, movie_id
from reviews
where rating > 4;

-- check
select * from reviews_view;


--       PROCEDURE
-- change the price of a session
create or replace procedure change_price (new_session_id int, new_price numeric)
language plpgsql
as
$$
begin
    update sessions
    set price = new_price
    where session_id = new_session_id;
end;
$$;

call change_price(1, 12.50);

-- check that the price changed
select session_id, price
from sessions
where session_id = 1;


--        TRIGGER
-- updates movie_count in genres when a new movie is added
create or replace function fnc_genre_movie_count()
returns trigger
language plpgsql
as
$$
begin
    update genres
    set movie_count = (select count(*)
        from movies
        where genre_id = new.genre_id)
    where genre_id = new.genre_id;
    return new;
end;
$$;

create trigger trg_update_genre_count
after insert on movies
for each row
execute function fnc_genre_movie_count();

-- the movies were added before the trigger existed, so count them once
update genres
set movie_count = (select count(*) from movies where movies.genre_id = genres.genre_id);

-- check
insert into movies (title, genre_id, movie_age_rating, movie_rating)
values ('Test movie', 1, '16+', 4.5);

-- movie_count should be bigger now
select * from genres;