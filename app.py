import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
import random
from PIL import Image
import io

# Set page config
st.set_page_config(
    page_title="Memory Palace Builder",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .header-style {
        font-size: 42px;
        font-weight: bold;
        color: #4a6fe3;
        margin-bottom: 20px;
    }
    .subheader-style {
        font-size: 24px;
        font-weight: 600;
        color: #4a6fe3;
        margin-top: 30px;
        margin-bottom: 10px;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .keyword-box {
        background-color: #e6f3ff;
        padding: 10px 15px;
        border-radius: 5px;
        margin-bottom: 10px;
        border-left: 4px solid #4a6fe3;
    }
    .memory-image {
        border: 2px solid #ddd;
        border-radius: 5px;
        padding: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state variables
if 'keywords' not in st.session_state:
    st.session_state.keywords = []
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = {}
if 'palace_locations' not in st.session_state:
    st.session_state.palace_locations = []
if 'memories_created' not in st.session_state:
    st.session_state.memories_created = False

# Header with logo
col1, col2 = st.columns([1, 5])
with col1:
    # Using an emoji as a placeholder for a logo
    st.markdown('<div style="font-size:60px; text-align:center;">🧠</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="header-style">Memory Palace Builder</div>', unsafe_allow_html=True)
    st.markdown("Transform your learning material into an unforgettable memory palace")

# Main layout
tab1, tab2, tab3 = st.tabs(["Create Memory Palace", "View My Palaces", "Memory Techniques"])

with tab1:
    # Left column for inputs
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<div class="subheader-style">Step 1: What do you want to memorize?</div>', unsafe_allow_html=True)
        
        # Example button
        if st.button("Load Example"):
            example_text = """Neural networks are computing systems with interconnected nodes that work similar to neurons in the human brain. Using algorithms, they can recognize hidden patterns and correlations in raw data, cluster and classify it, and continuously learn and improve over time."""
            st.session_state.example_loaded = True
        else:
            example_text = ""
        
        # Text input area
        study_material = st.text_area(
            "Enter the text you want to memorize:",
            value=example_text if 'example_loaded' in st.session_state and st.session_state.example_loaded else "",
            height=200
        )
        
        # Language selection
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            user_language = st.selectbox(
                "Learning language:",
                ["English", "Spanish", "French", "German", "Chinese", "Other"]
            )
        with col1_2:
            native_language = st.selectbox(
                "Your native language:",
                ["English", "Spanish", "French", "German", "Chinese", "Other"]
            )
        
        # Personal context
        user_context = st.text_area(
            "Personal context (helps create more memorable associations):",
            placeholder="E.g., I'm a visual learner and connect well with space/sci-fi imagery",
            height=100
        )
    
    with col2:
        st.markdown('<div class="subheader-style">Step 2: Choose your memory palace</div>', unsafe_allow_html=True)
        
        place_option = st.radio(
            "Memory palace location:",
            ["Upload your own place image", "Use a pre-built memory palace", "Generate AI place"]
        )
        
        if place_option == "Upload your own place image":
            uploaded_file = st.file_uploader("Upload an image (home, office, etc.)", type=["png", "jpg", "jpeg"])
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Your Memory Palace", width=300)
        
        elif place_option == "Use a pre-built memory palace":
            palace_template = st.selectbox(
                "Select a template:",
                ["Modern House", "Library", "Garden", "Museum", "Castle"]
            )
            # Placeholder for template images
            st.image("https://via.placeholder.com/300x200?text=Memory+Palace+Template", width=300)
        
        else:  # Generate AI place
            place_description = st.text_input(
                "Describe the place you want to generate:",
                placeholder="E.g., A cozy library with tall bookshelves and a fireplace"
            )
            if place_description:
                st.info("In the full version, an AI-generated image would appear here")
                # Placeholder for AI generated image
                st.image("https://via.placeholder.com/300x200?text=AI+Generated+Palace", width=300)

    # Horizontal separator
    st.markdown("---")
    
    # Process text and extract keywords
    if st.button("Extract Keywords and Build Memory Palace") and study_material:
        with st.spinner("Processing your text..."):
            # Download NLTK data if needed
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt')
            
            # Simple keyword extraction
            tokens = word_tokenize(study_material)
            # For this demo, filter for words longer than 4 chars
            keywords = [word for word in tokens if len(word) > 4 and word.isalpha()]
            # Remove duplicates and limit to 10 keywords
            st.session_state.keywords = list(dict.fromkeys(keywords))[:10]
            
            # Simulate generating images
            for keyword in st.session_state.keywords:
                # In a real app, you'd call an AI image generation API here
                st.session_state.generated_images[keyword] = f"https://via.placeholder.com/200x200?text={keyword}"
            
            # Simulate palace locations
            st.session_state.palace_locations = ["Living Room", "Kitchen", "Bedroom", "Bathroom", "Hallway"][:len(st.session_state.keywords)]
            
            st.session_state.memories_created = True
    
    # Display results if keywords were extracted
    if st.session_state.memories_created:
        st.markdown('<div class="subheader-style">Your Memory Palace is Ready!</div>', unsafe_allow_html=True)
        
        # Display the memory palace with items
        st.image("https://via.placeholder.com/800x400?text=Your+Interactive+Memory+Palace", use_column_width=True)
        
        st.markdown('<div class="subheader-style">Your Memory Images</div>', unsafe_allow_html=True)
        
        # Display keywords and generated images in a grid
        cols = st.columns(5)
        for i, keyword in enumerate(st.session_state.keywords):
            with cols[i % 5]:
                st.markdown(f"<div class='keyword-box'><b>{keyword}</b> - {st.session_state.palace_locations[i]}</div>", unsafe_allow_html=True)
                st.image(st.session_state.generated_images[keyword], width=150)
        
        # Practice button
        st.button("Start Practice Session", type="primary")
        
        # Save button
        st.download_button(
            label="Save Memory Palace",
            data="memory_palace_data",  # This would contain actual data in a real app
            file_name="my_memory_palace.mp",
            mime="application/octet-stream"
        )

with tab2:
    st.markdown('<div class="subheader-style">My Saved Memory Palaces</div>', unsafe_allow_html=True)
    
    # Placeholder for saved palaces
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="info-box">You have no saved memory palaces yet. Create your first one in the "Create Memory Palace" tab!</div>', unsafe_allow_html=True)
    
    with col2:
        st.metric(label="Memory Recall Rate", value="0%", delta=None)
        st.progress(0)

with tab3:
    st.markdown('<div class="subheader-style">Memory Techniques</div>', unsafe_allow_html=True)
    
    techniques = [
        {
            "name": "Method of Loci (Memory Palace)",
            "description": "Associate pieces of information with specific locations in a familiar space. As you mentally walk through the space, you retrieve the information.",
            "example": "Placing an image of a neural network at your front door, transformers on your coffee table, etc."
        },
        {
            "name": "Spaced Repetition",
            "description": "Review information at increasing intervals to improve long-term retention.",
            "example": "Review new material after 1 day, then 3 days, 7 days, etc."
        },
        {
            "name": "Mnemonic Devices",
            "description": "Create associations between new information and something you already know.",
            "example": "ROY G. BIV for the colors of the rainbow (Red, Orange, Yellow, Green, Blue, Indigo, Violet)"
        }
    ]
    
    for technique in techniques:
        with st.expander(technique["name"]):
            st.write(technique["description"])
            st.markdown("**Example:**")
            st.markdown(f"<div class='info-box'>{technique['example']}</div>", unsafe_allow_html=True)

# Sidebar for additional settings and navigation
with st.sidebar:
    st.markdown('<div class="subheader-style">Settings</div>', unsafe_allow_html=True)
    
    # Notification settings
    st.toggle("Enable practice reminders", value=True)
    
    reminder_frequency = st.select_slider(
        "Reminder frequency:",
        options=["Daily", "Every 3 days", "Weekly"]
    )
    
    # Learning style
    learning_style = st.multiselect(
        "Your learning style:",
        ["Visual", "Auditory", "Reading/Writing", "Kinesthetic"],
        default=["Visual"]
    )
    
    # User stats section
    st.markdown('<div class="subheader-style">Your Stats</div>', unsafe_allow_html=True)
    st.markdown("Total items memorized: 0")
    st.markdown("Memory palaces created: 0")
    st.markdown("Current streak: 0 days")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.markdown("© 2025 Memory Palace Builder")
with col2:
    st.markdown("Built with Streamlit and ❤️")
with col3:
    st.markdown("Version 1.0.0")
