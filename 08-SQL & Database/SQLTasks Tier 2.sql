/*
 * Project  : Natural Language Recommendation
 * Version  : 0.1.0
 * File     : \SQLTasks Tier 2.sql
 * Language : Python 3.7.11
 * ------------------------------------------------------------------------------------------------------------------------
 * Author   : John James
 * Company  : nov8.ai
 * Email    : john.james.sf@gmail.com
 * URL      : https://github.com/john-james-sf/nlr
 * ------------------------------------------------------------------------------------------------------------------------
 * Created  : Wednesday, November 20th 2019, 6:23:26 am
 * Modified :
 * Modifier : John James (john.james.sf@gmail.com)
 * ------------------------------------------------------------------------------------------------------------------------
 * License  : BSD 3-clause "New" or "Revised" License
 * Copyright: (c) 2021 nov8.ai
 */
/* Welcome to the SQL mini project. You will carry out this project partly in
the PHPMyAdmin interface, and partly in Jupyter via a Python connection.

This is Tier 2 of the case study, which means that there'll be less guidance for you about how to setup
your local SQLite connection in PART 2 of the case study. This will make the case study more challenging for you:
you might need to do some digging, aand revise the Working with Relational Databases in Python chapter in the previous resource.

Otherwise, the questions in the case study are exactly the same as with Tier 1.

PART 1: PHPMyAdmin
You will complete questions 1-9 below in the PHPMyAdmin interface.
Log in by pasting the following URL into your browser, and
using the following Username and Password:

URL: https://sql.springboard.com/
Username: student
Password: learn_sql@springboard

The data you need is in the "country_club" database. This database
contains 3 tables:
    i) the "Bookings" table,
    ii) the "Facilities" table, and
    iii) the "Members" table.

In this case study, you'll be asked a series of questions. You can
solve them using the platform, but for the final deliverable,
paste the code for each solution into this script, and upload it
to your GitHub.

Before starting with the questions, feel free to take your time,
exploring the data, and getting acquainted with the 3 tables. */



/* QUESTIONS
/* Q1: Some of the facilities charge a fee to members, but some do not.
Write a SQL query to produce a list of the names of the facilities that do. */

SELECT DISTINCT name FROM Facilities WHERE membercost > 0


/* Q2: How many facilities do not charge a fee to members? */

SELECT COUNT(DISTINCT NAME) FROM Facilities WHERE membercost = 0


/* Q3: Write an SQL query to show a list of facilities that charge a fee to members,
where the fee is less than 20% of the facility's monthly maintenance cost.
Return the facid, facility name, member cost, and monthly maintenance of the
facilities in question. */

SELECT facid,
name,
membercost,
monthlymaintenance
FROM Facilities
WHERE membercost > 0 AND
membercost < .2 * monthlymaintenance


/* Q4: Write an SQL query to retrieve the details of facilities with ID 1 and 5.
Try writing the query without using the OR operator. */

SELECT * FROM Facilities WHERE facid IN (1,5)


/* Q5: Produce a list of facilities, with each labelled as
'cheap' or 'expensive', depending on if their monthly maintenance cost is
more than $100. Return the name and monthly maintenance of the facilities
in question. */
SELECT
name,
CASE WHEN monthlymaintenance <= 100 THEN "cheap"
     ELSE "expensive" END AS cost,
monthlymaintenance
FROM Facilities

/* Q6: You'd like to get the first and last name of the last member(s)
who signed up. Try not to use the LIMIT clause for your solution. */
SELECT firstname, surname
FROM Members WHERE joindate =
    (SELECT MAX(joindate) FROM Members);


/* Q7: Produce a list of all members who have used a tennis court.
Include in your output the name of the court, and the name of the member
formatted as a single column. Ensure no duplicate data, and order by
the member name. */
SELECT DISTINCT f.name, CONCAT_WS(' ',m.surname, m.firstname) AS memname
FROM Facilities f
INNER JOIN Bookings b ON f.facid = b.facid
INNER JOIN Members m ON m.memid = b.memid
WHERE f.name LIKE "%Tennis Court%" AND
f.facid = b.facid AND
m.surname != 'GUEST'
ORDER BY memname

/* Q8: Produce a list of bookings on the day of 2012-09-14 which
will cost the member (or guest) more than $30. Remember that guests have
different costs to members (the listed costs are per half-hour 'slot'), and
the guest user's ID is always 0. Include in your output the name of the
facility, the name of the member formatted as a single column, and the cost.
Order by descending cost, and do not use any subqueries. */

SELECT 	f.name AS Facility,
		CONCAT_WS(', ',m.surname, m.firstname) AS Name,
		gb.slots * f.guestcost AS Cost
FROM Bookings gb
INNER JOIN Members m ON m.memid = gb.memid
INNER JOIN Facilities f ON f.facid = gb.facid
WHERE gb.slots * f.guestcost > 30 AND
    gb.starttime LIKE '2012-09-14%'AND
    gb.memid = 0
UNION ALL
SELECT 	f.name AS Facility,
		CONCAT_WS(' ',m.surname, m.firstname) AS Name,
		mb.slots * f.membercost AS Cost
FROM Bookings mb
INNER JOIN Members m ON m.memid = mb.memid
INNER JOIN Facilities f ON f.facid = mb.facid
WHERE mb.slots * f.membercost > 30 AND
    mb.starttime LIKE '2012-09-14%'AND
    mb.memid != 0
ORDER BY Cost DESC



/* Q9: This time, produce the same result as in Q8, but using a subquery. */
SELECT
	Facility,
	Name,
	Cost
FROM
	(SELECT
		rates.memid as memid,
		rates.facid as facid,
		rates.Facility AS Facility,
		rates.Name AS Name,
		b.slots * rates.cost AS Cost
	FROM
		(SELECT m.memid, CONCAT_WS(', ',m.surname, m.firstname) AS Name,f.facid,f.name AS Facility, f.guestcost AS cost
			FROM Facilities AS f
    		CROSS JOIN Members as m
    		WHERE m.memid = 0
		UNION
		SELECT m.memid, CONCAT_WS(', ',m.surname, m.firstname) AS Name,f.facid,f.name AS Facility, f.membercost AS cost
		FROM Facilities AS f
			CROSS JOIN Members as m
    		WHERE m.memid != 0) AS rates
	INNER JOIN Bookings b ON rates.memid = b.memid AND rates.facid = b.facid
	WHERE b.starttime LIKE '2012-09-14%') as bookings
WHERE Cost > 30
ORDER BY Cost DESC



/* PART 2: SQLite

Export the country club data from PHPMyAdmin, and connect to a local SQLite instance from Jupyter notebook
for the following questions.

QUESTIONS:
/* Q10: Produce a list of facilities with a total revenue less than 1000.
The output of facility name and total revenue, sorted by revenue. Remember
that there's a different cost for guests and members! */

/* Q11: Produce a report of members and who recommended them in alphabetic surname,firstname order */


/* Q12: Find the facilities with their usage by member, but not guests */


/* Q13: Find the facilities usage by month, but not guests */

