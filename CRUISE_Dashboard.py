import streamlit as st
import pandas as pd
import plotly.express as px
import pymongo
from dotenv import dotenv_values
import os

# secrets = dotenv_values("C:\\Users\\alihi\\Desktop\\Programming\\Advanced Database\\cruise-dashboard\\.env")

# connection = f"mongodb+srv://cruise0_ali:{st.secrets["DB_password"]}@cluster0.wjrco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


connection = f"mongodb+srv://cruise0_ali:{os.environ.get("DB_password")}@cluster0.wjrco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = pymongo.MongoClient(connection, connectTimeoutMS=60000, socketTimeoutMS=60000)

db = client["operational"]
user_collection = db["user"]
car_collection = db["car"]
trip_collection = db["trip"]

users_raw = list(user_collection.find())
users = pd.json_normalize(users_raw, 'user')

cars_raw = list(car_collection.find())
cars = pd.json_normalize(cars_raw, 'car')

trips_raw = list(trip_collection.find())
trips = pd.json_normalize(trips_raw, 'trip')

def cleaning(df):
    if "_id" in df:
        df.drop(columns=["_id"], inplace=True)
    df = df.dropna().reset_index(drop=True).drop_duplicates()
    for col in df.select_dtypes(include='object').columns:
        if col != 'userName':
            df[col] = df[col].str.lower()
    return df

users = cleaning(users)
cars = cleaning(cars)
trips = cleaning(trips)

gender_count = users['gender'].value_counts().reset_index()
gender_count.columns = ['gender', 'count']

merged_df = pd.merge(trips, users, on='userName')
fees_by_gender = merged_df.groupby('gender')['fee'].sum().reset_index()
fees_by_gender['gender'] = fees_by_gender['gender'].astype('category')

st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to bottom, #4a90e2, #d9e8ff);
            min-height: 100vh;
        }
        .header {
            color: white;
            font-size: 50px;
            text-align: center;
            margin-bottom: 70px;
        }
        .card {
            background-color: #E5ECF6;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            margin-top: 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .card h3 {
            color: #2A3F5F;
            font-size: 20px;
            margin-bottom: 5px;
        }
        .card h1 {
            color: #4493F8;
            font-size: 30px;
        }
        .card-container {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            justify-content: space-between;
            margin-bottom: 20px;
        }
        .graph-container {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            justify-content: center;
            margin-bottom: 20px;
        }
    </style>
    <div class="header">
        CRUISE Dashboard
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown(f"<div class='card'><h3>Users registered</h3><h1>{len(users)}</h1></div>", unsafe_allow_html=True)
with col2: st.markdown(f"<div class='card'><h3>Trips Done</h3><h1>{len(trips)}</h1></div>", unsafe_allow_html=True)
with col3: st.markdown(f"<div class='card'><h3>Cars registered</h3><h1>{len(cars)}</h1></div>", unsafe_allow_html=True)
with col4: st.markdown(f"<div class='card'><h3>Total fees</h3><h1>{sum(trips['fee'])}</h1></div>", unsafe_allow_html=True)

st.markdown("<div class='graph-container'>", unsafe_allow_html=True)

fig1 = px.bar(users.loc[0:2, :], x="userName", y="rate", title="Top 3 Users in CRUISE", labels={"userName": "User Name", "rate": "Rating"})
fig1.update_layout(
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family='Arial', size=18, color='black'),
    title_font=dict(size=24, color='black'),
    xaxis=dict(title_font=dict(size=18, color='black'), tickfont=dict(size=14, color='black')),
    yaxis=dict(title_font=dict(size=18, color='black'), tickfont=dict(size=14, color='black')),
    legend=dict(font=dict(size=16, color='black'))
)
st.markdown("<div class='graph'>", unsafe_allow_html=True)
st.plotly_chart(fig1)
st.markdown("</div>", unsafe_allow_html=True)

fig2 = px.pie(gender_count, names='gender', values='count', title="Gender Distribution in CRUISE", color='gender', color_discrete_sequence=["#FF69B4", "#636EFA"])
fig2.update_layout(
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family='Arial', size=18, color='black'),
    title_font=dict(size=24, color='black'),
    xaxis=dict(title_font=dict(size=18, color='black'), tickfont=dict(size=14, color='black')),
    yaxis=dict(title_font=dict(size=18, color='black'), tickfont=dict(size=14, color='black')),
    legend=dict(font=dict(size=16, color='black'))
)
st.markdown("<div class='graph'>", unsafe_allow_html=True)
st.plotly_chart(fig2)
st.markdown("</div>", unsafe_allow_html=True)

fig3 = px.bar(fees_by_gender, x="gender", y="fee", title="Trip Fees Done by Each Gender", labels={"gender": "Gender", "fee": "Fee"}, color="gender", color_discrete_sequence=["#FF69B4", "#636EFA"])
fig3.update_layout(
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family='Arial', size=18, color='black'),
    title_font=dict(size=24, color='black'),
    xaxis=dict(title_font=dict(size=18, color='black'), tickfont=dict(size=14, color='black')),
    yaxis=dict(title_font=dict(size=18, color='black'), tickfont=dict(size=14, color='black')),
    legend=dict(font=dict(size=16, color='black'))
)
st.markdown("<div class='graph'>", unsafe_allow_html=True)
st.plotly_chart(fig3)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

client.close()

# streamlit run "CRUISE_Dashboard.py"