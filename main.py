import datetime

import numpy as np
import pandas as pd
import streamlit as st

import process


def main():
    st.title("CP-Seeker Post-Processing App")

    st.markdown(
        """
        This app is designed to facilitate post-processing of CP-Seeker's output (McGrath, J. et al, 2023).
        Link to [GitHub](https://github.com/adamcseresznye/CP-Seeker_post_processor) repository.
        **Disclaimer**:*The developer is not liable for errors or inaccuracies. This app is provided as-is, without any warranties or guarantees.*

        ## Steps:

        1. Upload your CP-Seeker output files.
        2. Optionally, set the column locations of the confidence values and peak intensities separated by ':' and set your confidence level (the default confidence level is 80%).
        3. Download the filtered and merged dataset.
        """
    )

    st.markdown("### Upload your files")
    uploaded_files = st.file_uploader(
        "Drop your CP-Seeker *.xlsx output files here:", accept_multiple_files=True
    )

    with st.expander("### Optional settings"):
        location_scores = st.text_input(
            label="Range of confidence values in CP-Seeker excel file",
            value="A:AB",
            help="Default is set to A to AB separated by :",
        )
        location_intensities = st.text_input(
            label="Range of peak intensities in CP-Seeker excel file",
            value="AD:BF",
            help="Default is set to AD to BF separated by :",
        )
        threshold = st.slider("Set your confidence level", 0, 100, 80)

    click = st.button("Start Post-Processing", key="start-button")

    if click:
        if uploaded_files:
            processed_df = process.data_cleanup(
                uploaded_files=uploaded_files,
                threshold=threshold,
                location_intensities=location_intensities,
                location_scores=location_scores,
            )
            csv = process.convert_df(processed_df)

            st.download_button(
                "Press to Download",
                csv,
                f"{pd.Timestamp('today').strftime('%Y%m%d')}_experiment.csv",
                "text/csv",
                key="download-csv",
            )
            st.success("File is available for downloading.", icon="✅")
        else:
            st.error("No data available for processing.", icon="🚨")
    elif uploaded_files:
        st.info("Start your post-processing.", icon="ℹ️")


if __name__ == "__main__":
    main()
