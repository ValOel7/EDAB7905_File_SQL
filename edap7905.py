import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect('Chinook_SqliteGit.sqlite')

st.title("Overview of the Chinook Database based on 3 Queries")
st.header("Question 1 Revenue by Country + share of total")
q1 = pd.read_sql("""
SELECT
  i.BillingCountry,
  SUM(i.Total) AS TotalRevenue,
  SUM(I.Total) / (SELECT SUM(Total) FROM Invoice)*100 AS RevenueSharePercent

FROM Invoice AS i

GROUP BY BillingCountry

ORDER BY TotalRevenue DESC;""",conn)
print(q1)

st.write("My insight: The top markets are the USA, Canada, France, Brazil and Germany. From which USA has a revenue share percentage of 22.46% and Canada 13.05%.")

st.header("Question 2 Top 10 artists by sales")

q2 = pd.read_sql("""
SELECT
  a.Name AS ArtistName,
  SUM(i.Total) AS TotalSales,
  SUM(IL.Quantity) AS TracksSold

FROM Artist as a

JOIN Album AS al ON a.ArtistId = al.ArtistId
JOIN Track AS t ON al.AlbumId = t.AlbumId
JOIN InvoiceLine AS IL ON t.TrackId = IL.TrackId
JOIN Invoice AS i ON IL.InvoiceId = i.InvoiceId

GROUP BY ArtistName

ORDER BY TotalSales DESC

LIMIT 10;""",conn)
print(q2)

st.write("My insight: The most popular artist is Iron Maiden taking the first position with the highest sales in terms of Money earned. The second highest earning artist is U2.")

st.header("Question 3 Customer life time value + last purchase")
#Finalq3

q3 = pd.read_sql("""
SELECT
  c.CustomerId, c.FirstName||' '||c.LastName AS FullName, c.Country, SUM(i.Total) AS LifetimeValue, MAX(i.InvoiceDate) AS LastPurchaseDate

FROM Customer as c

JOIN Invoice AS i ON c.CustomerId = i.CustomerId

GROUP BY FullName

ORDER BY LifetimeValue DESC


;""",conn)
print(q3)

st.write("My insight: The highest paying customer is Helena Holý and the last date of purchase was 2025-11-13 meaning that the customer is still active. In contrast the second highest paying customer is Richard Cunningham yet the last date of purchas was 2025-04-05 which is not that recent.")
