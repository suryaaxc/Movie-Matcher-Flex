import streamlit as st

def apply_custom_css(tm, mode):
    # --- CONDITION: Sirf Neon Mode mein Movable Float Background dikhega ---
    if mode == 'neon':
        floating_bg_html = """
        <div id="neon-flow"></div>
        <style>
            #neon-flow {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: radial-gradient(circle at center, #0a192f 0%, #050505 100%);
                z-index: -1; overflow: hidden;
            }
            /* Floating Neon Orbs */
            .orb {
                position: absolute;
                border-radius: 50%;
                background: rgba(0, 255, 255, 0.05);
                border: 1px solid rgba(0, 255, 255, 0.3);
                box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
                animation: move 20s linear infinite;
            }
            @keyframes move {
                0% { transform: translateY(100vh) scale(0); opacity: 0; }
                50% { opacity: 0.5; }
                100% { transform: translateY(-10vh) scale(1.5); opacity: 0; }
            }
        </style>
        <script>
            function createOrb() {
                const container = document.getElementById('neon-flow');
                const orb = document.createElement('div');
                orb.className = 'orb';
                const size = Math.random() * 100 + 50 + 'px';
                orb.style.width = size; orb.style.height = size;
                orb.style.left = Math.random() * 100 + 'vw';
                orb.style.animationDuration = Math.random() * 10 + 15 + 's';
                container.appendChild(orb);
                setTimeout(() => orb.remove(), 25000);
            }
            setInterval(createOrb, 1500); // Har 1.5 sec mein naya floating element
        </script>
        """
        st.components.v1.html(floating_bg_html, height=0)

    # --- GLOBAL STATIC STYLES ---
    st.markdown(f"""
        <style>
        .stApp {{ background: {tm['bg']} !important; }}
        
        /* Movie Card Alignment Fix */
        .movie-card {{
            border: 2px solid {'#00FFFF' if mode == 'neon' else 'rgba(255,255,255,0.1)'};
            border-radius: 15px;
            padding: 12px;
            text-align: center;
            background: {tm['card']};
            backdrop-filter: blur(15px);
            transition: 0.3s ease-in-out;
            margin-bottom: 25px;
            box-shadow: {'0 0 15px rgba(0, 255, 255, 0.3)' if mode == 'neon' else 'none'};
        }}
        
        .movie-card:hover {{ transform: translateY(-8px); }}
        
        /* Rank Specific Glows */
        .rank-1 {{ border-color: #FF3131 !important; box-shadow: 0 0 20px #FF3131 !important; }}
        .rank-2 {{ border-color: #00D2FF !important; box-shadow: 0 0 20px #00D2FF !important; }}
        .rank-3 {{ border-color: #39FF14 !important; box-shadow: 0 0 20px #39FF14 !important; }}
        
        .movie-title-text {{
            color: {tm['txt']};
            font-size: 0.85em; font-weight: bold; margin: 10px 0;
            min-height: 45px; display: flex; align-items: center; justify-content: center;
        }}
        </style>
    """, unsafe_allow_html=True)