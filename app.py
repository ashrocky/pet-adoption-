import streamlit as st 
import pandas as pd
import os
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="Pet Adoption Center",
    page_icon="🐾",
    layout="wide"
)

# Ensure an 'uploads' directory exists for storing images
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize session state for pets if it doesn't exist
if 'pets' not in st.session_state:
    st.session_state.pets = pd.DataFrame({
        'name': ['Max', 'Luna', 'Charlie', 'Bella'],
        'type': ['Dog', 'Cat', 'Dog', 'Cat'],
        'breed': ['Golden Retriever', 'Persian', 'Labrador', 'Siamese'],
        'age': [2, 1, 3, 2],
        'gender': ['Male', 'Female', 'Male', 'Female'],
        'size': ['Large', 'Small', 'Large', 'Medium'],
        'weight': [30, 5, 32, 6],
        'color': ['Golden', 'White', 'yellow', 'Cream'],
        'vaccinated': ['Yes', 'Yes', 'No', 'Yes'],
        'personality': ['Friendly', 'Shy', 'Playful', 'Affectionate'],
        'training': ['Basic commands', 'Litter trained', 'House trained', 'Litter trained'],
        'compatibility_pets': ['Yes', 'No', 'Yes', 'Yes'],
        'compatibility_kids': ['Yes', 'Yes', 'No', 'Yes'],
        'special_needs': ['None', 'Blind in one eye', 'None', 'Allergy to grains'],
        'status': ['Available', 'Available', 'Available', 'Available'],
        'image': [
            "uploads/max.jpg",
            "uploads/luna.jpg",
            "uploads/charlie.jpg",
            "uploads/bella.jpg"
        ]
    })

# Navigation
def navigation():
    st.sidebar.title("Navigation")
    return st.sidebar.radio(
        "Go to",
        ["Home", "Available Pets", "Adopt a Pet", "Admin Dashboard","Pet Care Guide","Add a new pet"]
    )

# Home page
def home():
    st.title("🏠 Welcome to Our Pet Adoption Center")
    st.markdown("""
    ## Find Your Perfect Companion
    We believe every pet deserves a loving home. Our adoption center helps connect 
    wonderful animals with caring families.
    
    ### Why Adopt?
    - Save a life
    - Get a loyal companion
    - Support animal welfare
    - Experience unconditional love
    - Encourage an Active Lifestyle
    - Give a Home to the Homeless
    - Teach Responsibility & Empathy
    """)

    # Ensure the pets list exists
    if 'pets' not in st.session_state or st.session_state.pets.empty:
        st.error("No pets found!")
        return

    pets = st.session_state.pets.to_dict(orient="records")  # Convert DataFrame to list of dictionaries

    for pet in pets:
        image_path = pet['image']  # Use the stored image path

        if os.path.exists(image_path):  # Ensure file exists
            st.image(image_path, caption=pet['name'])
        else:
            st.error(f"Image not found: {image_path}")

    # Display some featured pets
    st.subheader("Featured Pets")
    cols = st.columns(4)
    for idx, col in enumerate(cols):
        with col:
            if idx < len(st.session_state.pets):
                pet = st.session_state.pets.iloc[idx]
                st.image(pet['image'], caption=pet['name'])
                st.write(f"**{pet['name']}**")
                st.write(f"{pet['breed']} ")
                st.write(f"{pet['age']} years old")


# Available pets page
def available_pets():
    st.title("🐾 Available Pets")

    pets_df = st.session_state.pets.copy()

    cols = st.columns(3)
    for idx, pet in pets_df.iterrows():
        with cols[idx % 3]:
            image_path = pet['image']
            if not os.path.exists(image_path):
                image_path = "https://via.placeholder.com/200"

            st.image(image_path, caption=pet['name'])
            st.write(f"**{pet['name']}** - {pet['breed']}")
            st.write(f"Age: {pet['age']} years")
            st.write(f"Gender: {pet['gender']}")
            st.write(f"Size: {pet['size']}")
            st.write(f"Weight: {pet['weight']} kg")
            st.write(f"Color: {pet['color']}")
            st.write(f"Vaccinated: {pet['vaccinated']}")
            st.write(f"Personality: {pet['personality']}")
            st.write(f"Training: {pet['training']}")
            st.write(f"Good with other pets: {pet['compatibility_pets']}")
            st.write(f"Good with kids: {pet['compatibility_kids']}")
            st.write(f"Special Needs: {pet['special_needs']}")
            if pet['status'] == 'Available':
                if st.button(f"Adopt {pet['name']}", key=f"adopt_{idx}"):
                    pet['status'] = 'Adopted'
                    st.session_state.pets.at[idx, 'status'] = 'Adopted'
                    st.success(f"{pet['name']} has been adopted!")

# Adoption form
def adopt_pet():
    st.title("🤝 Adopt a Pet")
    st.write("Please fill out this form to begin the adoption process.")

    with st.form("adoption_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        address = st.text_area("Address")
        pet_preference = st.multiselect("Preferred Pet Type", ["Dog", "Cat"], ["Dog", "Cat"])
        experience = st.radio("Do you have previous pet experience?", ["Yes", "No"])
        living_situation = st.selectbox("Living Situation", ["House with yard", "House without yard", "Apartment", "Other"])
        additional_info = st.text_area("Additional Information")
        submitted = st.form_submit_button("Submit Application")
        if submitted:
            st.success("Thank you for submitting your adoption application! We will contact you soon.")


# Admin Dashboard
def admin_dashboard():
    st.title("👨‍💼 Admin Dashboard")
    st.write("Manage pets and adoption details here.")
    st.dataframe(st.session_state.pets)

    # Pet Care Guide Page
def pet_care_guide():
    st.title("🐶🐱 Pet Care Guide")
    print("Pet Care Guide function is being executed!")  # Console check
    st.markdown("### Learn how to take care of your furry friends!")

    pet_type = st.selectbox("Select a Pet Type", ["Dog", "Cat"])

    if pet_type == "Dog":
        st.subheader("🐶 Dog Care Guide")
        st.write("""
        **Feeding:**  
        - Provide high-quality dog food with balanced nutrients.  
        - Fresh water should always be available.  
        - Avoid feeding chocolate, grapes, onions, and other toxic foods.  

        **Exercise:**  
        - Regular walks (at least 30 minutes daily).  
        - Playtime with toys to stimulate their mind.  

        **Health & Grooming:**  
        - Regular vet checkups and vaccinations.  
        - Brush their coat weekly.  
        - Trim nails every 3-4 weeks.  

        **Training & Socialization:**  
        - Start basic obedience training early.  
        - Expose them to different environments for socialization.  
        """)

    elif pet_type == "Cat":
        st.subheader("🐱 Cat Care Guide")
        st.write("""
        **Feeding:**  
        - Provide a mix of wet and dry cat food.  
        - Ensure fresh water is always available.  
        - Avoid feeding onions, garlic, chocolate, and dairy products.  

        **Exercise:**  
        - Cats love interactive toys like feather wands.  
        - Provide scratching posts to keep them active.  

        **Health & Grooming:**  
        - Vet checkups at least once a year.  
        - Brush their coat regularly to reduce shedding.  
        - Clean the litter box daily.  

        **Training & Socialization:**  
        - Use positive reinforcement for training.  
        - Give them safe spaces for hiding and resting.  
        """)

    st.success("🐾 Taking care of your pet ensures they live a happy and healthy life!")

# Add a new pet function
def add_new_pet():
    st.title("➕ Add a New Pet")
    
    with st.form("add_pet_form", clear_on_submit=True):
        name = st.text_input("Pet Name")
        pet_type = st.selectbox("Type", ["Dog", "Cat"])
        breed = st.text_input("Breed")
        age = st.number_input("Age (in years)", min_value=0, max_value=20, step=1)
        gender = st.selectbox("Gender", ["Male", "Female"])
        size = st.selectbox("Size", ["Small", "Medium", "Large"])
        weight = st.number_input("Weight (in kg)", min_value=0, step=1)
        color = st.text_input("Color")
        vaccinated = st.selectbox("Vaccinated", ["Yes", "No"])
        personality = st.text_area("Personality")
        training = st.text_area("Training")
        compatibility_pets = st.selectbox("Good with other pets?", ["Yes", "No"])
        compatibility_kids = st.selectbox("Good with kids?", ["Yes", "No"])
        special_needs = st.text_area("Special Needs (if any)")
        status = "Available"  # Default status

        image_file = st.file_uploader("Upload Pet Image", type=["jpg", "png", "jpeg"])

        submitted = st.form_submit_button("Add Pet")
        
        if submitted:
            if name and breed and image_file:
                image_path = os.path.join(UPLOAD_FOLDER, image_file.name)
                with open(image_path, "wb") as f:
                    f.write(image_file.getbuffer())
                
                new_pet = pd.DataFrame([{
                    'name': name,
                    'type': pet_type,
                    'breed': breed,
                    'age': age,
                    'gender': gender,
                    'size': size,
                    'weight': weight,
                    'color': color,
                    'vaccinated': vaccinated,
                    'personality': personality,
                    'training': training,
                    'compatibility_pets': compatibility_pets,
                    'compatibility_kids': compatibility_kids,
                    'special_needs': special_needs,
                    'status': status,
                    'image': image_path
                }])

                st.session_state.pets = pd.concat([st.session_state.pets, new_pet], ignore_index=True)
                st.success(f"{name} has been added successfully!")
            else:
                st.error("Please fill in all required fields and upload an image.")


def main():
    page = navigation()
    if page == "Home":
        home()
    elif page == "Available Pets":
        available_pets()
    elif page == "Adopt a Pet":
        adopt_pet()
    elif page == "Admin Dashboard":
        admin_dashboard()
    elif page == "Pet Care Guide":
        pet_care_guide()
    elif page == "Add a new pet":
        add_new_pet()

if __name__ == "__main__":
    main() 
