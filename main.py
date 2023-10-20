import datetime

import numpy as np
import pandas as pd
import streamlit as st

import process

st.title("CP-Seeker Post-Processing App")

st.markdown(
    """
            This app is designed to facilitate post-processing of CP-Seeker's output (McGrath, J. et al, 2023).
            Link to [GitHub](https://github.com/adamcseresznye/CP-Seeker_post_processor) repository.
             **Disclaimer**:*The developer is not liable for errors or inaccuracies. This app is provided as-is, without any warranties or guarantees.*

            ## Steps:

            1. Upload your files.
            2. Optionally, set your confidence level (the default confidence level is 80%).
            3. Download the filtered and merged dataset.

        """
)

st.markdown("### Upload your files")
uploaded_files = st.file_uploader(
    "Drop your CPSeeker *.xlsx output files here:", accept_multiple_files=True
)

st.markdown("### Set your confidence level")
threshold = st.slider(" ", 0, 100, 80)

click = st.button("Start Post-Processing", type="primary")

if uploaded_files is not None and click:
    processed_df = process.data_cleanup(
        uploaded_files=uploaded_files, threshold=threshold
    )
    csv = process.convert_df(processed_df)

    st.download_button(
        "Press to Download",
        csv,
        f"{datetime.datetime.now(datetime.UTC).strftime('%y%m%d')}_experiment.csv",
        "text/csv",
        key="download-csv",
    )
