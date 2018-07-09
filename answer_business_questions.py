
# coding: utf-8

# In[1]:


import pandas as pd
import sqlite3
import matplotlib as plt
get_ipython().magic('matplotlib inline')


# In[2]:


def run_query(q):
    conn = sqlite3.connect("chinook.db")
    return pd.read_sql(q, conn)


# In[3]:


def run_command(c):
    conn = sqlite3.connect("chinook.db")
    conn.execute(c)


# In[4]:


def show_tables():
    q = "select name, type from sqlite_master where type in ('table','view');"
    return run_query(q)    


# In[5]:


show_tables()


# In[6]:


run_query("select * from customer limit 5")


# In[7]:


#customer_purchase = run_query(
    #"create view customer_purchase as select c.customer_id,c.country,i.invoice_id,i.total from customer c left join invoice i on i.customer_id = c.customer_id"
#)
#normal to be error cause I already created for the first time
#the table already exist
#to avoid error >>  "#" it


# In[8]:


#run_query("create view usa as select * from customer_purchase where country = 'USA'")
#normal to be error cause I already created for the first time
#the table already exist
#to avoid error >>  "#" it


# In[9]:


run_query("select * from usa")


# In[11]:


#run_query(
#"create view invoice_genre as select il.invoice_id,il.track_id,t.genre_id,g.name genre from invoice_line il left join track t on t.track_id = il.track_id left join genre g on g.genre_id = t.genre_id")


# In[12]:


run_query("select * from invoice_genre")


# In[13]:


#info of all tracks bought in USA
run_query(
"select usa.*,ig.* from usa left join invoice_genre ig on ig.invoice_id = usa.invoice_id")


# In[14]:


#getting the data we wanted
#run_query(
#" create view usa_tracks_sold as select usa.*,ig.*,count(ig.track_id) tracks_sold from usa left join invoice_genre ig on ig.invoice_id = usa.invoice_id group by ig.genre order by tracks_sold desc")


# In[15]:


run_query("select * from usa_tracks_sold")


# In[16]:


#all genres in the data
run_query("select distinct genre from invoice_genre")


# In[17]:


#all genres that are sold in usa
run_query(
"select distinct ig.genre from usa left join invoice_genre ig on ig.invoice_id = usa.invoice_id group by ig.genre")


# In[18]:


#calculate the percentage with known value of total tracks sold in USA
run_query("select genre, tracks_sold,round((cast(tracks_sold as float)/1051)*100,2) percent from usa_tracks_sold")


# In[19]:


run_query("select genre,ROUND((CAST(count(track_id) AS FLOAT)/CAST((select count(track_id)) AS FLOAT))*100,2) percent_track from usa_tracks_sold")


# In[20]:


run_query("select sum(tracks_sold)from usa_tracks_sold")


# In[21]:


run_query("select (cast(tracks_sold as float)/cast(sum(tracks_sold) as float))from usa_tracks_sold")


# In[23]:


run_query("select cast(sum(tracks_sold) as float) from usa_tracks_sold")


# In[24]:


#try group by genre >> fail
run_query("select genre, (cast(tracks_sold as float)/cast(sum(tracks_sold) as float)) percent from usa_tracks_sold group by genre")


# In[30]:


genre_sales_usa = run_query("select genre, tracks_sold,round((cast(tracks_sold as float)/1051)*100,2) percent from usa_tracks_sold")


# In[27]:


type(genre_sales_usa)


# In[28]:


genre_sales_usa.plot.bar(x = "genre")


# In[29]:


run_query("SELECT genre,CAST(tracks_sold as float)/(SELECT SUM(tracks_sold) from usa_tracks_sold) as percent FROM usa_tracks_sold")

