import streamlit as st
import pickle

df= pickle.load(open('data.pkl','rb'))

st.title("Recommend the Travel Location")


similarity = pickle.load(open('similarity.pkl','rb'))


def recommend(destination):
    destination = destination.lower()
    try:
        id = df[df['Destination'].str.lower() == destination].index[0]
    except IndexError:
        return "Destination Not found in dataset"
    
    distances = list(enumerate(similarity[id]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

    recommended = [df.iloc[i[0]]['Destination'] for i in distances]
    return recommended

Destination= st.selectbox("Destination",df['Destination'])

if st.button('show recommendation'):
    result = recommend(Destination)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(result[0])
    with col2:
        st.text(result[1])
    with col3:
        st.text(result[2])
    with col4:
        st.text(result[3])
    with col5:
        st.text(result[4])


