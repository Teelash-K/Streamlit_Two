import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib as plt
# %matplotlib inline
import warnings
warnings.filterwarnings('ignore')
import joblib
import pickle
import time


#load the model
model = pickle.load(open('financial_Inc_model.pkl', 'rb'))

#add picture from local computer
import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('image1.webp') 

# to import css file into streamlit
with open('financial Inclusion.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)


st.markdown("<h4>FININACIAL INCLUSION IN EAST AFRICA PREDICTION</h4>", unsafe_allow_html=True)
st.markdown("<p style = 'font-weight: bold; font-style: italic; font-family: Optima;  color: #FF9B82'>built by TAIWO K. LASH</h1>", unsafe_allow_html = True)
st.markdown("<br><br>", unsafe_allow_html = True) 


st.markdown("<h6>Overview</h6>", unsafe_allow_html = True)

st.markdown("<p style = 'color : #191717'>One of the prominent issues confronting Africa, with profound implications for both human development and the economy, pertains to the accessibility of banking services, whether for personal or business use. Creative solutions have been devised to extend financial services to populations that were previously overlooked. The East African region, encompassing nations like Kenya, Tanzania, Uganda, and Rwanda, has experienced noteworthy advancements in this regard.</p>", unsafe_allow_html=True)

st.write("Therefore, this application is developed to forecast the probability of individuals possessing or utilizing a bank account.")


data = pd.read_csv('dataset\Financial_inclusion_dataset.csv')
df = pd.read_csv('Feature_Definitions.csv')
df.reset_index(drop=True, inplace=True)
# df.drop('Unnamed: 1', inplace = True, axis = 1)


custom_css = """
<style>
    .st-af {
        color: black !important; 
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


with st.form('my_form', clear_on_submit=True):
    st.header("BANK ACCOUNT PREDICTION")
    with st.expander("Variable Definitions"):
        st.table(df)
    Gender = st.selectbox('Gender',['','Female','Male'])    
    Age_of_respondent = int(st.number_input('Age', value = 30))
    Country = st.selectbox('Country', ['','Kenya', 'Rwanda', 'Tanzania', 'Uganda'])
    Job_type = st.selectbox('Occupation',['','Self employed', 'Government Dependent',
       'Formally employed Private', 'Informally employed',
       'Formally employed Government', 'Farming and Fishing',
       'Remittance Dependent', 'Other Income',
       'Dont Know/Refuse to answer', 'No Income'])
    Education_level = st.selectbox('Education',['',
                                           'Primary education',
                                           'Secondary education',
                                           'Tertiary education',
                                           'Vocational/Specialised training',
                                           'No formal education',
                                           'Other/Dont know/RTA'])
    Location_type = st.selectbox('Area', ['', 'Rural', 'Urban'])
    Cellphone_access = st.selectbox('Cellphone Access',['', 'Yes', 'No'])

    
    submitted = st.form_submit_button("SUBMIT")   
    if (Gender and Age_of_respondent and Country and Job_type and Education_level and Location_type and Cellphone_access):
        if submitted:
            with st.spinner(text='Loading..'):
                time.sleep(1)
                st.write("Your Inputted Data:")           

                input_var = pd.DataFrame([{'gender_of_respondent' : Gender, 'age_of_respondent' : Age_of_respondent, 'country' : Country, 'job_type' : Job_type, 'education_level' : Education_level, 'location_type' : Location_type,  'cellphone_access' : Cellphone_access,}])
                st.write(input_var) 
                
                from sklearn.preprocessing import LabelEncoder, StandardScaler
                lb = LabelEncoder()
                scaler = StandardScaler()
                for i in input_var:
                    if input_var[i].dtypes == 'int' or input_var[i].dtypes == 'float':
                        input_var[[i]] = scaler.fit_transform(input_var[[i]])
                    else:
                        input_var[i] = lb.fit_transform(input_var[i])
                        
                # time.sleep(2)
                prediction = model.predict(input_var)
                if prediction == 0:
                    st.error('You are not qualified to have a bank account')
                else:
                    st.balloons
                    st.success('You are qualified to have a bank account')
                # st.write(prediction)
