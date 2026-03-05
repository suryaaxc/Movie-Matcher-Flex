import streamlit as st

def render_header(tm):
    # CSS for Floating Animation
    st.markdown("""
        <style>
        @keyframes floating {
            0% { transform: translate(0,  0px); }
            50%  { transform: translate(0, -10px); }
            100%   { transform: translate(0, -0px); }   
        }
        .floating-text {
            animation-name: floating;
            animation-duration: 3s;
            animation-iteration-count: infinite;
            animation-timing-function: ease-in-out;
            display: inline-block;
        }
        </style>
    """, unsafe_allow_html=True)

    # Professional Neon Popcorn Icon
    logo_svg = """
    <div class="floating-text">
    <svg width="60" height="60" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M25 40C25 28.9543 33.9543 20 45 20H55C66.0457 20 75 28.9543 75 40V70C75 75.5228 70.5228 80 65 80H35C29.4772 80 25 75.5228 25 70V40Z" stroke="#00FFFF" stroke-width="5" stroke-linecap="round"/>
        <path d="M40 30L35 15M50 30L50 10M60 30L65 15" stroke="#FFD700" stroke-width="5" stroke-linecap="round"/>
        <circle cx="50" cy="50" r="10" stroke="#00FFFF" stroke-width="5"/>
        <path d="M20 90H80" stroke="#00FFFF" stroke-width="5" stroke-linecap="round"/>
    </svg>
    </div>
    """
    
    col1, col2 = st.columns([0.1, 0.9])
    
    with col1:
        st.markdown(logo_svg, unsafe_allow_html=True)
        
    with col2:
        # Title with Floating Class
        st.markdown(f"""
            <div class="floating-text" style="display: flex; flex-direction: column; justify-content: center; height: 60px;">
                <h1 style='margin:0; padding:0; font-size: 2.2em; color:{tm['txt']} !important; 
                    font-family: "Montserrat", sans-serif; text-transform: uppercase; letter-spacing: 2px;
                    text-shadow: {"0 0 15px #00FFFF" if tm["txt"] == "#00FFFF" else "none"};'>
                    Movie Matcher Flex
                </h1>
                <p style='margin:0; padding:0; font-size: 0.9em; color:#00CCCC; font-weight: normal; letter-spacing: 1px;'>
                    ULTIMATE MATCHING | Professional Edition
                </p>
            </div>
        """, unsafe_allow_html=True)