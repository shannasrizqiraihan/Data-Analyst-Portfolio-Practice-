"""
Netflix Content Analysis Dashboard
Created by: Shannas Rizqi
GitHub: https://github.com/shannasrizqiraihan/Data-Analyst-Portfolio-Practice-
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Netflix Content Analysis",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #0f0f0f;
    }
    .stMetric {
        background-color: #1f1f1f;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #E50914;
    }
    h1 {
        color: #E50914;
        font-family: 'Arial Black', sans-serif;
    }
    h2, h3 {
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# LOAD DATA
# ============================================================================
@st.cache_data
def load_data():
    df = pd.read_csv('02-Netflix-Dashboard/netflix_titles.csv')
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
    return df

df = load_data()

# ============================================================================
# SIDEBAR
# ============================================================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=200)
st.sidebar.title("🎬 Filters")

# Type filter
type_filter = st.sidebar.multiselect(
    "Content Type",
    options=df['type'].unique(),
    default=df['type'].unique()
)

# Year filter
year_range = st.sidebar.slider(
    "Release Year",
    min_value=int(df['release_year'].min()),
    max_value=int(df['release_year'].max()),
    value=(2000, int(df['release_year'].max()))
)

# Rating filter
rating_filter = st.sidebar.multiselect(
    "Rating",
    options=sorted(df['rating'].dropna().unique()),
    default=sorted(df['rating'].dropna().unique())
)

# Apply filters
df_filtered = df[
    (df['type'].isin(type_filter)) &
    (df['release_year'].between(year_range[0], year_range[1])) &
    (df['rating'].isin(rating_filter))
]

st.sidebar.markdown("---")
st.sidebar.info("""
**About this Dashboard:**
This dashboard provides comprehensive analysis of Netflix's content catalog, 
including trends, distributions, and insights about movies and TV shows.

**Data Source:** Netflix Titles Dataset (Kaggle)

**Created by:** Shannas Rizqi  
**GitHub:** https://github.com/shannasrizqiraihan/Data-Analyst-Portfolio-Practice-
""")

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

st.title("🎬 NETFLIX CONTENT ANALYSIS DASHBOARD")
st.markdown("### Comprehensive insights into Netflix's movie and TV show catalog")
st.markdown("---")

# ============================================================================
# KEY METRICS
# ============================================================================
st.header("📊 Key Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Total Titles",
        value=f"{len(df_filtered):,}",
        delta=f"{len(df_filtered) - len(df):,}" if len(df_filtered) != len(df) else None
    )

with col2:
    movies_count = len(df_filtered[df_filtered['type'] == 'Movie'])
    st.metric(
        label="Movies",
        value=f"{movies_count:,}",
        delta=f"{movies_count/len(df_filtered)*100:.1f}%"
    )

with col3:
    tv_count = len(df_filtered[df_filtered['type'] == 'TV Show'])
    st.metric(
        label="TV Shows",
        value=f"{tv_count:,}",
        delta=f"{tv_count/len(df_filtered)*100:.1f}%"
    )

with col4:
    countries = df_filtered['country'].dropna().str.split(',').explode().nunique()
    st.metric(
        label="Countries",
        value=f"{countries:,}"
    )

with col5:
    genres = df_filtered['listed_in'].dropna().str.split(',').explode().nunique()
    st.metric(
        label="Genres",
        value=f"{genres:,}"
    )

st.markdown("---")

# ============================================================================
# ROW 1: CONTENT TYPE & RATING DISTRIBUTION
# ============================================================================
st.header("📺 Content Overview")

col1, col2 = st.columns(2)

with col1:
    # Content Type Distribution
    type_counts = df_filtered['type'].value_counts()
    
    fig_type = px.pie(
        values=type_counts.values,
        names=type_counts.index,
        title="Content Type Distribution",
        color_discrete_sequence=['#E50914', '#564d4d'],
        hole=0.4
    )
    fig_type.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont_size=14
    )
    fig_type.update_layout(
        showlegend=True,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12)
    )
    st.plotly_chart(fig_type, use_container_width=True, key="unique_key_here")

with col2:
    # Rating Distribution
    rating_counts = df_filtered['rating'].value_counts().sort_values(ascending=True)
    
    fig_rating = px.bar(
        x=rating_counts.values,
        y=rating_counts.index,
        orientation='h',
        title="Content by Rating",
        color=rating_counts.values,
        color_continuous_scale='Reds',
        labels={'x': 'Number of Titles', 'y': 'Rating'}
    )
    fig_rating.update_layout(
        showlegend=False,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        xaxis=dict(showgrid=True, gridcolor='#333333'),
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig_rating, use_container_width=True)

st.markdown("---")

# ============================================================================
# ROW 2: GEOGRAPHIC & TEMPORAL ANALYSIS
# ============================================================================
st.header("🌍 Geographic & Temporal Trends")

col1, col2 = st.columns(2)

with col1:
    # Top Countries
    countries_data = df_filtered['country'].dropna().str.split(',').str[0].str.strip()
    top_countries = countries_data.value_counts().head(15)
    
    fig_countries = px.bar(
        x=top_countries.values,
        y=top_countries.index,
        orientation='h',
        title="Top 15 Content Producing Countries",
        color=top_countries.values,
        color_continuous_scale='Reds',
        labels={'x': 'Number of Titles', 'y': 'Country'}
    )
    fig_countries.update_layout(
        showlegend=False,
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        xaxis=dict(showgrid=True, gridcolor='#333333'),
        yaxis=dict(showgrid=False)
    )
    fig_countries.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_countries, use_container_width=True)

with col2:
    # Release Year Trend
    year_counts = df_filtered['release_year'].value_counts().sort_index()
    year_counts = year_counts[year_counts.index >= 1990]
    
    fig_year = px.area(
        x=year_counts.index,
        y=year_counts.values,
        title="Content by Release Year (1990+)",
        labels={'x': 'Release Year', 'y': 'Number of Titles'}
    )
    fig_year.update_traces(
        fill='tozeroy',
        line_color='#E50914',
        fillcolor='rgba(229, 9, 20, 0.3)'
    )
    fig_year.update_layout(
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        xaxis=dict(showgrid=True, gridcolor='#333333'),
        yaxis=dict(showgrid=True, gridcolor='#333333')
    )
    st.plotly_chart(fig_year, use_container_width=True)

st.markdown("---")

# ============================================================================
# ROW 3: GENRE ANALYSIS & CONTENT ADDED OVER TIME
# ============================================================================
st.header("🎭 Genre Insights & Content Growth")

col1, col2 = st.columns(2)

with col1:
    # Top Genres
    all_genres = df_filtered['listed_in'].dropna().str.split(',').explode().str.strip()
    top_genres = all_genres.value_counts().head(15)
    
    fig_genres = px.bar(
        x=top_genres.values,
        y=top_genres.index,
        orientation='h',
        title="Top 15 Genres",
        color=top_genres.values,
        color_continuous_scale='Reds',
        labels={'x': 'Number of Titles', 'y': 'Genre'}
    )
    fig_genres.update_layout(
        showlegend=False,
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        xaxis=dict(showgrid=True, gridcolor='#333333'),
        yaxis=dict(showgrid=False)
    )
    fig_genres.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_genres, use_container_width=True)

with col2:
    # Content Added Over Time
    yearly_added = df_filtered['year_added'].dropna().value_counts().sort_index()
    
    # Separate by type
    movies_yearly = df_filtered[df_filtered['type'] == 'Movie']['year_added'].value_counts().sort_index()
    tv_yearly = df_filtered[df_filtered['type'] == 'TV Show']['year_added'].value_counts().sort_index()
    
    fig_added = go.Figure()
    fig_added.add_trace(go.Scatter(
        x=movies_yearly.index,
        y=movies_yearly.values,
        mode='lines+markers',
        name='Movies',
        line=dict(color='#E50914', width=3),
        marker=dict(size=8)
    ))
    fig_added.add_trace(go.Scatter(
        x=tv_yearly.index,
        y=tv_yearly.values,
        mode='lines+markers',
        name='TV Shows',
        line=dict(color='#564d4d', width=3),
        marker=dict(size=8)
    ))
    
    fig_added.update_layout(
        title="Content Added to Netflix by Year",
        xaxis_title="Year",
        yaxis_title="Number of Titles",
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        xaxis=dict(showgrid=True, gridcolor='#333333'),
        yaxis=dict(showgrid=True, gridcolor='#333333'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    st.plotly_chart(fig_added, use_container_width=True)

st.markdown("---")

# ============================================================================
# ROW 4: DURATION ANALYSIS
# ============================================================================
st.header("⏱️ Duration Analysis")

col1, col2 = st.columns(2)

with col1:
    # Movie Duration Distribution
    movies_df = df_filtered[df_filtered['type'] == 'Movie'].copy()
    movies_df['duration_min'] = movies_df['duration'].str.replace(' min', '').astype(float)
    
    fig_movie_duration = px.histogram(
        movies_df,
        x='duration_min',
        nbins=30,
        title="Movie Duration Distribution",
        labels={'duration_min': 'Duration (minutes)', 'count': 'Frequency'},
        color_discrete_sequence=['#E50914']
    )
    
    # Add median line
    median_duration = movies_df['duration_min'].median()
    fig_movie_duration.add_vline(
        x=median_duration,
        line_dash="dash",
        line_color="yellow",
        annotation_text=f"Median: {median_duration:.0f} min",
        annotation_position="top right"
    )
    
    fig_movie_duration.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        xaxis=dict(showgrid=True, gridcolor='#333333'),
        yaxis=dict(showgrid=True, gridcolor='#333333'),
        showlegend=False
    )
    st.plotly_chart(fig_movie_duration, use_container_width=True)
    
    # Statistics
    st.markdown(f"""
    **Movie Duration Statistics:**
    - Mean: {movies_df['duration_min'].mean():.0f} minutes
    - Median: {movies_df['duration_min'].median():.0f} minutes
    - Min: {movies_df['duration_min'].min():.0f} minutes
    - Max: {movies_df['duration_min'].max():.0f} minutes
    """)

with col2:
    # TV Show Seasons Distribution
    tv_df = df_filtered[df_filtered['type'] == 'TV Show'].copy()
    tv_df['num_seasons'] = tv_df['duration'].str.replace(' Season', '').str.replace('s', '').astype(float)
    
    seasons_counts = tv_df['num_seasons'].value_counts().sort_index()
    
    fig_tv_seasons = px.bar(
        x=seasons_counts.index,
        y=seasons_counts.values,
        title="TV Show Number of Seasons",
        labels={'x': 'Number of Seasons', 'y': 'Frequency'},
        color=seasons_counts.values,
        color_continuous_scale='Reds'
    )
    
    fig_tv_seasons.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        xaxis=dict(showgrid=True, gridcolor='#333333'),
        yaxis=dict(showgrid=True, gridcolor='#333333'),
        showlegend=False
    )
    st.plotly_chart(fig_tv_seasons, use_container_width=True)
    
    # Statistics
    st.markdown(f"""
    **TV Show Season Statistics:**
    - Mean: {tv_df['num_seasons'].mean():.1f} seasons
    - Median: {tv_df['num_seasons'].median():.0f} seasons
    - Min: {tv_df['num_seasons'].min():.0f} seasons
    - Max: {tv_df['num_seasons'].max():.0f} seasons
    """)

st.markdown("---")

# ============================================================================
# ROW 5: TOP CONTRIBUTORS
# ============================================================================
st.header("🎬 Top Contributors")

col1, col2 = st.columns(2)

with col1:
    # Top Directors
    directors = df_filtered['director'].dropna().str.split(',').explode().str.strip()
    top_directors = directors.value_counts().head(10)
    
    fig_directors = px.bar(
        x=top_directors.values,
        y=top_directors.index,
        orientation='h',
        title="Top 10 Directors",
        color=top_directors.values,
        color_continuous_scale='Reds',
        labels={'x': 'Number of Titles', 'y': 'Director'}
    )
    fig_directors.update_layout(
        showlegend=False,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        xaxis=dict(showgrid=True, gridcolor='#333333'),
        yaxis=dict(showgrid=False)
    )
    fig_directors.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_directors, use_container_width=True)

with col2:
    # Top Actors
    actors = df_filtered['cast'].dropna().str.split(',').explode().str.strip()
    top_actors = actors.value_counts().head(10)
    
    fig_actors = px.bar(
        x=top_actors.values,
        y=top_actors.index,
        orientation='h',
        title="Top 10 Actors",
        color=top_actors.values,
        color_continuous_scale='Reds',
        labels={'x': 'Number of Appearances', 'y': 'Actor'}
    )
    fig_actors.update_layout(
        showlegend=False,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        xaxis=dict(showgrid=True, gridcolor='#333333'),
        yaxis=dict(showgrid=False)
    )
    fig_actors.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_actors, use_container_width=True)

st.markdown("---")

# ============================================================================
# DATA EXPLORER
# ============================================================================
st.header("🔍 Data Explorer")

# Show raw data
if st.checkbox("Show Raw Data"):
    st.dataframe(
        df_filtered[['type', 'title', 'director', 'cast', 'country', 
                    'release_year', 'rating', 'duration', 'listed_in']].head(100),
        use_container_width=True
    )

# Download filtered data
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name="netflix_filtered_data.csv",
    mime="text/csv",
)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888888;'>
    <p>📊 Netflix Content Analysis Dashboard | Created with Streamlit & Plotly</p>
    <p>Data Source: <a href='https://www.kaggle.com/datasets/shivamb/netflix-shows' target='_blank'>Netflix Shows Dataset (Kaggle)</a></p>
    <p>© 2025 Shannas Rizqi | <a href='https://github.com/shannasrizqiraihan/Data-Analyst-Portfolio-Practice-' target='_blank'>GitHub Repository</a></p>
</div>
""", unsafe_allow_html=True)