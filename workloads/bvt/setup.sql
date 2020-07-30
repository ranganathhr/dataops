CREATE TABLE IF NOT EXISTS shipping
(
  origin_state varchar,
  origin_zip bigint,
  destination_state varchar,
  destination_zip bigint,
  package_weight bigint
  )
WITH (format='orc');
insert into shipping values('California', 94131, 'New Jersey', 8648, 13);
insert into shipping values('California', 94131, 'New Jersey', 8540, 42);
insert into shipping values('New Jersey', 7081, 'Connecticut', 6708, 225);
insert into shipping values('California', 90210, 'Connecticut', 6927, 1337);
insert into shipping values('California', 94131, 'Colorado', 80308, 5);
insert into shipping values('New York', 10002, 'New Jersey', 8540, 3);