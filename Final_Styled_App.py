import streamlit as st
st.markdown('''
    <style>
/* Background Styling */
.stApp {
    background-color:#c7c7ff ;
    padding: 20px;
}

/* Title and Headers */
h1, h2, h3, h4 {
    color: #2E86C1;
    font-family: 'Arial', sans-serif;
    font-weight: bold;
    text-align: center;
}

/* Customize Buttons */
div.stButton > button {
    background-color: #2E86C1;
    color: white;
    border-radius: 10px;
    font-size: 18px;
    padding: 10px 20px;
    transition: 0.3s;
    border: none;
    display: block;
    margin: 0 auto;
}

div.stButton > button:hover {
    background-color: #1B4F72;
}

/* Customize Input Fields */
.stTextInput, .stSelectbox, .stSlider, .stNumberInput {
    border: 2px solid #2E86C1 ;
    border-radius: 5px ;
    padding: 8px ;
    font-size: 16px ;
}

/* Prediction Output Styling */
div.stMarkdown {
    font-size: 20px;
    color: #117A65;
    font-weight: bold;
    text-align: center;
}

/* Negotiation Insight Box */
div.stMarkdown:last-child {
    background-color: #D5F5E3;
    padding: 15px;
    border-radius: 10px;
    font-size: 18px;
    font-weight: bold;
    text-align: center;
}

/* Footer Styling */
footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    text-align: center;
    padding: 10px;
    background-color: #2E86C1;
    color: white;
    font-size: 14px;
    font-weight: bold;
}
</style>''', unsafe_allow_html=True)

import pandas as pd
import numpy as np
import pickle as pk
import streamlit as st   #to run the streamlit used python -m streamlit run app.py
#deploy the model
@st.cache_resource
def load_model():
    return pk.load(open('model.pkl', 'rb'))

model = load_model()

st.header('Car Price Prediction')
st.markdown("**This app predicts the price of the car based on your requirements and gives you the negotiation insight.**")

cars_data=pd.read_csv('Cardetails.csv')

#to get the brand name
def get_brand_name(car_name):
    car_name=car_name.split(' ')[0]
    return car_name.strip()
cars_data['name']=cars_data['name'].apply(get_brand_name)

name=st.selectbox('Select the Brand Name', cars_data['name'].unique())
year=st.slider('Car Manufactured Year', 1994,2024)
km_driven=st.slider('No. of Kilometer Driven', 1,200000)
fuel=st.selectbox('Fuel Type', cars_data['fuel'].unique())
seller_type=st.selectbox('Seller Type', cars_data['seller_type'].unique())
transmission=st.selectbox('Transmission Type', cars_data['transmission'].unique())
owner=st.selectbox('Owner Type', cars_data['owner'].unique())
mileage	=st.slider('Car Mileage ', 10,45)
engine=st.slider('Engine CC',700,5500)
max_power=st.slider('Max Power',0,250)
seats=st.slider('Seating Capacity',3,10)


# Function to Provide Price Negotiation Insights
def negotiation_insight(listing_price, predicted_price):
    price_diff = ((listing_price - predicted_price) / predicted_price) * 100
    
    if price_diff > 15:
        return f'Overpriced by {price_diff:.2f}%. Consider negotiating ₹{listing_price - predicted_price:.0f} lower.'
    elif -10 <= price_diff <= 15:
        return 'Fair Price. The price is reasonable.'
    else:
        return f'Underpriced by {-price_diff:.2f}%. This is a great deal!'

listing_price = st.number_input("Enter the Listed Price of the Car", min_value=10000, max_value=10000000, step=5000)
    
if st.button("Predict"):
    input_data_model = pd.DataFrame(
    [[name,year, km_driven, fuel, seller_type, transmission,owner, 
      mileage, engine, max_power, seats]],
    columns=['name', 'year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'owner', 'mileage', 'engine', 'max_power', 'seats'])
    
    input_data_model['fuel'].replace(['Diesel', 'Petrol', 'LPG', 'CNG'], [1,2,3,4],
                                 inplace=True)
    input_data_model['seller_type'].replace(['Individual', 'Dealer', 'Trustmark Dealer'], [1,2,3],
                                 inplace=True)
    input_data_model['transmission'].replace(['Manual', 'Automatic'], [1,2],inplace=True)
    input_data_model['name'].replace(['Maruti', 'Skoda', 'Honda', 'Hyundai', 'Toyota', 'Ford', 'Renault',
       'Mahindra', 'Tata', 'Chevrolet', 'Datsun', 'Jeep', 'Mercedes-Benz',
       'Mitsubishi', 'Audi', 'Volkswagen', 'BMW', 'Nissan', 'Lexus',
       'Jaguar', 'Land', 'MG', 'Volvo', 'Daewoo', 'Kia', 'Fiat', 'Force',
       'Ambassador', 'Ashok', 'Isuzu', 'Opel'],
                          [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
                          inplace=True)
    input_data_model['owner'].replace(['First Owner', 'Second Owner', 'Third Owner',
       'Fourth & Above Owner', 'Test Drive Car'], [1,2,3,4,5],
                                 inplace=True)
    #st.write(input_data_model)

    #passing the numerical values to the model
    car_price=model.predict(input_data_model)
    st.markdown(f'Car price predicted is ₹ {car_price[0]:.2f}')
    
    # Get negotiation insights
    #listing_price = st.number_input("Enter the Listed Price of the Car", min_value=10000, max_value=10000000, step=5000)
    negotiation_message = negotiation_insight(listing_price, car_price[0])
    st.subheader("Negotiation Insight:")
    st.write(negotiation_message)
    

