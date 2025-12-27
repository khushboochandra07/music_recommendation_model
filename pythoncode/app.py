import streamlit as st
import pandas as pd

# Load clustered dataset with song details
df = pd.read_csv("../data/clustered_songs.csv")

st.set_page_config(page_title="Music Recommendation", layout="wide")

# Custom CSS to make tabs more intuitive
st.markdown("""
    <style>
    /* Style the tab buttons */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #f0f2f6;
        border-radius: 10px 10px 0 0;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 10px 24px;
        background-color: #ffffff;
        border-radius: 8px 8px 0 0;
        border: 2px solid #e6e6e6;
        border-bottom: none;
        color: #666;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        margin-right: 2px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f8f9fa;
        border-color: #1f77b4;
        color: #1f77b4;
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4 !important;
        border-color: #1f77b4 !important;
        color: white !important;
        box-shadow: 0 4px 8px rgba(31, 119, 180, 0.3);
    }
    
    /* Style the tab content */
    .stTabs [data-baseweb="tab-panel"] {
        background-color: white;
        border: 2px solid #1f77b4;
        border-radius: 0 0 10px 10px;
        padding: 20px;
        margin-top: -2px;
        min-height: 400px;
    }
    
    /* Remove default streamlit tab styling */
    .stTabs > div > div > div > div {
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 Music Recommendation App")

# Navigation tabs with more descriptive labels
tab1, tab2 = st.tabs(["🔥 Top Trending Songs", "🎯 Find Similar Songs"])

# TAB 1: Top Trending Songs (existing flow)
with tab1:
    st.header("Top Recommended Songs by Cluster")
    
    # Sort by popularity and take the first row of each group
    top_representatives = df.sort_values(
        by=['cluster_kmean', 'track_popularity'], 
        ascending=[True, False]
    ).groupby('cluster_kmean').head(1)

    # Create a responsive grid based on the number of clusters
    num_clusters = len(top_representatives)
    cols = st.columns(min(num_clusters, 4)) # Display up to 4 per row

    for i, (_, row) in enumerate(top_representatives.iterrows()):
        col_idx = i % 4
        with cols[col_idx]:
            st.subheader(f"#{int(row['cluster_kmean']) + 1}")
            
            # Display song details in a clean card format
            st.markdown(f"### **{row['track_name']}**")
            st.write(f"👤 **Artist:** {row['track_artist']}")
            st.write(f"🔥 **Popularity:** {row['track_popularity']}")
            
            # Optional: Add a button to see more from this cluster
            if st.button(f"Click to explore songs similar to {row['track_name']}", key=f"trending_btn_{i}"):
                st.session_state['selected_cluster'] = row['cluster_kmean']
                st.session_state['selected_track'] = row['track_name']
                st.session_state['active_tab'] = 'trending'

    st.divider()

    # Dynamic Exploration Section for Tab 1
    if 'selected_cluster' in st.session_state and st.session_state.get('active_tab') == 'trending':
        selected = st.session_state['selected_cluster']
        st.write(f"Showing more songs similar to  **{st.session_state['selected_track']}**:")
        cluster_df = df[df['cluster_kmean'] == selected].sort_values('track_popularity', ascending=False)
        
        # Get the data and make URLs clickable
        display_df = cluster_df[['track_name', 'track_artist', 'spotify_url']].drop_duplicates(subset=['track_name'], keep='first').head(20).copy()
        
        # Format URLs as clickable links
        display_df['spotify_url'] = display_df['spotify_url'].apply(
            lambda x: f'<a href="{x}" target="_blank">🎵 Listen on Spotify</a>' if pd.notna(x) else 'N/A'
        )
        
        # Rename columns for better display to match the second tab
        display_df.columns = ['Song', 'Artist', 'Listen']
        
        # Display with HTML rendering enabled
        st.markdown(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)

# TAB 2: Find Similar Songs (new flow)
with tab2:
    st.header("Find Songs Similar to Your Choice")
    
    # Create a searchable song selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create unique songs with index for better matching
        unique_songs = df.drop_duplicates(subset=['track_name', 'track_artist']).reset_index(drop=True)
        unique_songs['display_name'] = unique_songs['track_name'] + ' - ' + unique_songs['track_artist']
        
        # Song selection dropdown with search
        selected_song_display = st.selectbox(
            "Search and select a song:",
            options=unique_songs['display_name'].tolist(),
            index=0,
            help="Type to search for a song"
        )
    
    with col2:
        st.write("") # spacer
        st.write("") # spacer
        if st.button("🔍 Find Similar Songs", type="primary"):
            if selected_song_display:
                # Find the selected song using the display name
                selected_row = unique_songs[unique_songs['display_name'] == selected_song_display]
                
                if not selected_row.empty:
                    selected_row = selected_row.iloc[0]
                    
                    st.session_state['user_selected_cluster'] = selected_row['cluster_kmean']
                    st.session_state['user_selected_track'] = selected_row['track_name']
                    st.session_state['user_selected_artist'] = selected_row['track_artist']
                    st.session_state['active_tab'] = 'search'
                    st.rerun()  # Refresh to show results immediately
                else:
                    st.error("Song not found. Please try again.")

    st.divider()

    # Show recommendations based on user selection
    if 'user_selected_cluster' in st.session_state and st.session_state.get('active_tab') == 'search':
        selected_cluster = st.session_state['user_selected_cluster']
        
        # Display selected song info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Selected Song", st.session_state['user_selected_track'])
        with col2:
            st.metric("Artist", st.session_state['user_selected_artist'])
        
        st.subheader(f"🎵 Songs Similar to '{st.session_state['user_selected_track']}'")
        
        # Get songs from the same cluster, excluding the selected song
        similar_songs = df[df['cluster_kmean'] == selected_cluster]
        similar_songs = similar_songs[
            ~((similar_songs['track_name'] == st.session_state['user_selected_track']) & 
              (similar_songs['track_artist'] == st.session_state['user_selected_artist']))
        ].sort_values('track_popularity', ascending=False)
        
        # Remove duplicates and get top recommendations
        recommendations = similar_songs[['track_name', 'track_artist', 'track_popularity', 'spotify_url']].drop_duplicates(
            subset=['track_name'], keep='first'
        ).head(15)
        
        if len(recommendations) > 0:
            # Format URLs as clickable links
            recommendations_display = recommendations.copy()
            recommendations_display['spotify_url'] = recommendations_display['spotify_url'].apply(
                lambda x: f'<a href="{x}" target="_blank">🎵 Listen on Spotify</a>' if pd.notna(x) else 'N/A'
            )
            
            # Rename columns for better display
            recommendations_display.columns = ['Song', 'Artist', 'Popularity', 'Listen']
            
            # Display with HTML rendering enabled
            st.markdown(recommendations_display.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.info("No similar songs found in this cluster.")
        
        # Add a button to clear selection
        if st.button("🔄 Search for Another Song"):
            for key in ['user_selected_cluster', 'user_selected_track', 'user_selected_artist', 'active_tab']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()