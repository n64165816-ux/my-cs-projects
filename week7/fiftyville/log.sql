-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Step 1: Scan the database schema to understand available tables and columns
-- Purpose: Identify which tables store location data (like streets) and date/time info to map out intersections.
.schema

-- Step 2: Filter crime scene reports for the specific date and location of the theft
-- Purpose: Get the exact description of the crime, the precise time it occurred, and mentions of any witnesses.
SELECT description
FROM crime_scene_reports
WHERE year = 2025 AND month = 7 AND day = 28
AND street = 'Humphrey Street';

--Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
--Interviews were conducted today with three witnesses who were present at
--the time – each of their interview transcripts mentions the bakery.

--The Exact Time (10:15 AM)
--The Location (Humphrey Street Bakery)

-- Step 3: Query the interviews table to read the transcripts of the three witnesses
-- Purpose: Extract specific clues from the 3 witnesses who were at the bakery around 10:15 AM.
SELECT name, transcript
FROM interviews
WHERE year = 2025 AND month = 7 AND day = 28;
--Analysis of the 3 Critical Witnesses:
--Sometime within ten minutes of the theft, I saw the thief get into a car in the
--bakery parking lot and drive away. If you have security footage from the bakery
--parking lot, you might want to look for cars that left the parking lot in that time frame.

-- Step 5: Check bakery parking logs between 10:15 AM and 10:25 AM (10 minutes within the theft)
-- Purpose: Filter license plates of cars exiting the bakery parking lot immediately after the crime.
SELECT license_plate, hour, minute
FROM bakery_security_logs
WHERE year = 2025 AND month = 7 AND day = 28
AND hour = 10 AND minute >= 15 AND minute <= 25
AND activity = 'exit';

--license_plate | hour | minute |
--+---------------+------+--------+
--| 5P2BI95       |   10 |     16 |
--| 94KL13X       |   10 |     18 |
--| 6P58WS2       |   10 |     18 |
--| 4328GD8       |   10 |     19 |
--| G412CB7       |   10 |     20 |
--| L93JTIZ       |   10 |     21 |
--| 322W7JE       |   10 |     23 |
--| 0NTHK55       |   10 |     23 |

-- Step 6: Check ATM transactions on Leggett Street for withdrawals on the day of the theft
-- Purpose: Find account numbers of people who withdrew cash that morning, as witnessed by Eugene.
SELECT account_number, amount
FROM atm_transactions
WHERE year = 2025 AND month = 7 AND day = 28
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw';

--+----------------+--------+
--| account_number | amount |
--+----------------+--------+
--|       28500762 |     48 |
--|       28296815 |     20 |
--|       76054385 |     60 |
--|       49610011 |     50 |
--|       16153065 |     80 |
--|       25506511 |     20 |
--|       81061156 |     30 |
--|       26013199 |     35 |
--+----------------+--------+

-- Step 7: Check short phone calls (less than a minute) made around the time of the theft
-- Purpose: Find the caller (thief) and receiver (accomplice) phone numbers from Raymond's statement.
SELECT caller, receiver, duration
FROM phone_calls
WHERE year = 2025 AND month = 7 AND day = 28
AND duration < 60;

--+----------------+----------------+----------+
--|     caller     |    receiver    | duration |
--+----------------+----------------+----------+
--| (130) 555-0289 | (996) 555-8899 |       51 |
--| (499) 555-9472 | (892) 555-8872 |       36 |
--| (367) 555-5533 | (375) 555-8161 |       45 |
--| (499) 555-9472 | (717) 555-1342 |       50 |
--| (286) 555-6063 | (676) 555-6554 |       43 |
--| (770) 555-1861 | (725) 555-3243 |       49 |
--| (031) 555-6622 | (910) 555-3251 |       38 |
--| (826) 555-1652 | (066) 555-9701 |       55 |
--| (338) 555-6650 | (704) 555-2131 |       54 |
--+----------------+----------------+----------+

-- Step 8: Identify the earliest flight leaving Fiftyville on July 29, 2025
-- Purpose: Find the flight ID and destination city to track where the thief escaped.
SELECT flights.id, airports.city, flights.hour, flights.minute
FROM flights
JOIN airports ON flights.destination_airport_id = airports.id
WHERE flights.year = 2025 AND flights.month = 7 AND flights.day = 29
ORDER BY flights.hour, flights.minute
LIMIT 1;

--flight the thief took
--+----+---------------+------+--------+
--| id |     city      | hour | minute |
--+----+---------------+------+--------+
--| 36 | New York City |    8 |     20 |
--+----+---------------+------+--------+

-- Step 9: Get the list of passport numbers and seat assignments for Flight 36
-- Purpose: Identify the individuals who escaped to New York City on the earliest morning flight.
SELECT passport_number, seat
FROM passengers
WHERE flight_id = 36;

--+-----------------+------+
--| passport_number | seat |
--+-----------------+------+
--|      7214083635 | 2A   |
--|      1695452385 | 3B   |
--|      5773159633 | 4A   |
--|      1540955065 | 5C   |
--|      8294398571 | 6C   |
--|      1988161715 | 6D   |
--|      9878712108 | 7A   |
--|      8496433585 | 7B   |
--+-----------------+------+

-- Step 10: Intersect all clues to unmask the thief and accomplice
-- Purpose: Match the suspects from the flight list with bank accounts, phone logs, and license plates.
SELECT name, people.passport_number, people.phone_number, people.license_plate
FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
WHERE people.license_plate IN (
    SELECT license_plate FROM bakery_security_logs
    WHERE year = 2025 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = 'exit'
)
AND bank_accounts.account_number IN (
    SELECT account_number FROM atm_transactions
    WHERE year = 2025 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
)
AND people.phone_number IN (
    SELECT caller FROM phone_calls
    WHERE year = 2025 AND month = 7 AND day = 28 AND duration < 60
)
AND people.passport_number IN (
    SELECT passport_number FROM passengers WHERE flight_id = 36
);

--The name of the thief:
--+-------+-----------------+----------------+---------------+
--| name  | passport_number |  phone_number  | license_plate |
--+-------+-----------------+----------------+---------------+
--| Bruce |      5773159633 | (367) 555-5533 | 94KL13X       |
--+-------+-----------------+----------------+---------------+

-- Step 11: Identify the accomplice by tracing the phone call receiver
-- Purpose: Find the name of the person who received the call from the thief right after the crime.
SELECT name
FROM people
WHERE phone_number = (
    SELECT receiver
    FROM phone_calls
    WHERE year = 2025 AND month = 7 AND day = 28
    AND duration < 60
    AND caller = (
        -- This subquery identifies the thief's phone number automatically
        SELECT people.phone_number
        FROM people
        JOIN bank_accounts ON people.id = bank_accounts.person_id
        WHERE people.license_plate IN (
            SELECT license_plate FROM bakery_security_logs
            WHERE year = 2025 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = 'exit'
        )
        AND bank_accounts.account_number IN (
            SELECT account_number FROM atm_transactions
            WHERE year = 2025 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
        )
        AND people.phone_number IN (
            SELECT caller FROM phone_calls
            WHERE year = 2025 AND month = 7 AND day = 28 AND duration < 60
        )
        AND people.passport_number IN (
            SELECT passport_number FROM passengers WHERE flight_id = 36
        )
    )
);

--The accomplice name:
--+-------+
--| name  |
--+-------+
--| Robin |
--+-------+
