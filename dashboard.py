import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st



def create_daily_bikesharing_df(df):
    daily_bikesharing_df=df[['dteday','cnt']].copy()
    daily_bikesharing_df.rename(columns={
        "cnt" : "rental_count"
    },inplace=True)

    return daily_bikesharing_df

def create_byseason_df(df):
    seasonal_rent_df = df.groupby('season').agg({
        'cnt': 'sum'
    }).reset_index()
    seasonal_rent_df.rename(columns={
        'season': 'Musim',
        'cnt': 'Jumlah Sewa'
    }, inplace=True)
    
    return seasonal_rent_df

def create_byworkingday_df (df):
    working_day = df.groupby(by='workingday').agg({
    'cnt': 'sum'}).reset_index()
    working_day.rename(columns={
    "cnt": "jumlah_sewa"}, inplace=True)
    return working_day

#dataset
day_df = pd.read_csv('data/cleaned_day.csv')
hour_df = pd.read_csv('data/cleaned_hour.csv')

datetime_columns=["dteday"]
day_df.sort_values(by="dteday",inplace=True)
day_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])


min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()




with st.sidebar:
   
    st.image("https://miro.medium.com/v2/resize:fit:1100/format:webp/1*ATlagc9XVjU6wu9z7CIVTQ.jpeg")

    #Mengambil start_date & end_date dari data input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"]>= str(start_date))&
                 (day_df["dteday"] <= str (end_date))]

daily_bikesharing_df = create_daily_bikesharing_df(main_df)
byseason_df = create_byseason_df(main_df)
byworkingday_df = create_byworkingday_df(main_df)
# Dashboard
st.header("Bike-Sharing Rental Dashboard")

# Daily Bike Rental Trends
st.subheader("Daily Bike Rental Trends")
total_rental = daily_bikesharing_df.rental_count.sum()
st.metric("Total Rental", value = total_rental)

fig, ax = plt.subplots(figsize=(16,8))

ax.plot(
    daily_bikesharing_df["dteday"],
    daily_bikesharing_df["rental_count"],
    marker='o',
    linewidth=2,
    color ="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader('Evaluating Best and Worst Seasons for Bike Rentals')

colors_ = []
max_value = byseason_df['Jumlah Sewa'].max() 

for index, row in byseason_df.iterrows():
    if row['Jumlah Sewa'] == max_value:
        colors_.append("#72BCD4")  
    else:
        colors_.append("#D3D3D3")

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x="Jumlah Sewa",
    y="Musim", 
    data=byseason_df,
    palette=colors_,
    ax=ax  # Pastikan visualisasi ditambahkan ke fig
)

ax.set_title("Total Bike Rentals by Season", fontsize=15)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=12)

st.pyplot(fig)  # Menampilkan grafik di Streamlit


st.subheader("Bike Rental Trends: Weekdays vs. Weekends")

# Membuat figure baru
fig, ax = plt.subplots(figsize=(10, 5))

# Warna untuk workingday (0 = weekend, 1 = weekday)
colors_ = [ "#72BCD4","#D3D3D3"]

# Membuat barplot
sns.barplot(
    y="jumlah_sewa",  
    x="workingday", 
    data=byworkingday_df.sort_values(by="jumlah_sewa", ascending=False), 
    palette=colors_,
    ax=ax  # Menambahkan grafik ke figure
)

# Menambahkan judul dan kustomisasi tampilan
ax.set_title("Jumlah sewa sepeda berdasarkan hari libur dan hari kerja", loc="center", fontsize=15)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=12)

# Menampilkan grafik di Streamlit
st.pyplot(fig)
