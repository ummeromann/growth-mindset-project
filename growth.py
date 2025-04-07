import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Page config
st.set_page_config(page_title="📀 Data Sweeper", layout="wide")

# Custom CSS styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: #00FFAA;
    }
    h1, h2, h3, h4, h5 {
        color: #00FFAA;
    }
    .stButton > button {
        background-color: #00FFAA;
        color: black;
        font-weight: bold;
    }
    .stDownloadButton > button {
        background-color: #1DB954;
        color: white;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App title and description
st.title("📀 DataSweeper - Sterling Integrator by Umme Roman Syed")
st.markdown("### Transform your files between CSV and Excel formats with built-in data cleaning and visualization.")

# File uploader
uploaded_files = st.file_uploader(
    "📤 Upload your files (CSV or Excel supported):",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

# Processing uploaded files
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        # Preview
        st.markdown(f"### 🔍 Preview of `{file.name}`")
        st.dataframe(df.head())

        # Data cleaning
        st.markdown("### 🧹 Data Cleaning Options")
        if st.checkbox(f"Clean data for `{file.name}`"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🧽 Remove Duplicates from `{file.name}`"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates removed!")

            with col2:
                if st.button(f"🩹 Fill Missing Values in `{file.name}`"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values filled with column means!")

        # Select columns to keep
        st.markdown("### 🎯 Select Columns to Keep")
        columns = st.multiselect(f"Choose columns for `{file.name}`", df.columns, default=df.columns)
        df = df[columns]

        # Visualization
        st.markdown("### 📊 Data Visualization")
        if st.checkbox(f"Show visualization for `{file.name}`"):
            if df.select_dtypes(include='number').shape[1] >= 1:
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
            else:
                st.warning("⚠️ No numeric columns to visualize.")

        # File conversion
        st.markdown("### 🔄 Conversion Options")
        conversion_type = st.radio(f"Convert `{file.name}` to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            file_name = None
            mime_type = None

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            if file_name and mime_type:
                st.download_button(
                    label=f"⬇️ Download `{file.name}` as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )
            else:
                st.error("❌ Conversion failed. Please try again.")

# Footer success
st.success("🎉 All files processed successfully!")
