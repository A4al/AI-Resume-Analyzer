import streamlit as st
import json

from resume_parser import extract_text_from_pdf
from ai_analyzer import analyze_resume
from report_generator import generate_report

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)
st.markdown("""
<style>

.main {
    background-color: #f8f9fa;
}

h1 {
    text-align: center;
    font-size: 42px;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #666;
    font-size: 18px;
    margin-bottom: 30px;
}

div[data-testid="stMetric"] {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

div[data-testid="stMetric"] label {
    color: #555555 !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #111111 !important;
    font-size: 32px !important;
    font-weight: 700 !important;
}

div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    color: #555555 !important;
}

</style>
""", unsafe_allow_html=True)
st.title("📄 AI Resume Analyzer")

st.markdown(
    '<div class="subtitle">'
    'Upload your resume and get AI-powered career insights'
    '</div>',
    unsafe_allow_html=True
)
resume = st.file_uploader(
    "Upload your Resume",
    type=["pdf"]
)
st.subheader("🎯 Target Job Description (Optional)")

job_description = st.text_area(
    "Paste the Job Description here",
    height=250,
    placeholder="Paste the job description of the role you are applying for..."
)

if resume is not None:

    st.success("Resume uploaded successfully! ✅")

    text = extract_text_from_pdf(resume)

    st.subheader("📄 Extracted Resume Text")

    st.text_area(
        "Resume Content",
        text,
        height=400
    )
    if st.button("🤖 Analyze Resume"):


        try:
            with st.spinner("AI is analyzing your resume..."):
                analysis = analyze_resume(text, job_description)
        except Exception as e:
            st.error("⚠️ Gemini API error occurred.")  
            if "429" in str(e) or "quota" in str(e).lower():
                        st.warning(
                            "Gemini API quota/rate limit reached. "
                            "Please wait for some time and try again."
                        )
            else:
                st.warning(
                    "Something went wrong while contacting the AI service."
                )
            st.stop()
        try:
            analysis = analysis.strip()

            # Remove Markdown code fences
            if analysis.startswith("```"):
                analysis = analysis.split("\n", 1)[1]

            if analysis.endswith("```"):
                analysis = analysis[:-3]

            analysis = analysis.strip()

            data = json.loads(analysis)

        except json.JSONDecodeError:
            st.error(
                "AI returned an invalid JSON response. "
                "Please try Analyze Resume again."
            )
            st.code(analysis)
            st.stop()      
        
        # -------------------------
        # RESUME SCORE
        # -------------------------

        st.subheader("📊 AI Resume Analysis")

        score = data["resume_score"]

        st.markdown("### 📊 Resume Score")

        score_col1, score_col2 = st.columns([1, 3])

        with score_col1:

            st.metric(
                "Resume Score",
                f"{score}/100"
            )

        with score_col2:

            st.write("### 📈 Overall Resume Performance")

            st.progress(score / 100)

            st.write(data["score_explanation"])


        # -------------------------
        # SKILLS ANALYSIS
        # -------------------------

        st.subheader("🛠️ Skills Analysis")

        col1, col2 = st.columns(2)

        with col1:

            st.write("### ✅ Skills Detected")

            for skill in data["skills_detected"]:

                st.markdown(
                    f"""
                    <span style="
                        display:inline-block;
                        padding:6px 12px;
                        margin:4px;
                        border-radius:15px;
                        border:1px solid #28a745;
                    ">
                    {skill}
                    </span>
                    """,
                    unsafe_allow_html=True
                )

        with col2:

            st.write("### ❌ Missing Skills")

            for skill in data["missing_skills"]:

                st.markdown(
                    f"""
                    <span style="
                        display:inline-block;
                        padding:6px 12px;
                        margin:4px;
                        border-radius:15px;
                        border:1px solid #dc3545;
                    ">
                    {skill}
                    </span>
                    """,
                    unsafe_allow_html=True
                )


        # -------------------------
        # JOB ROLE MATCH
        # -------------------------

        st.subheader("🎯 Job Role Match")

        job_cols = st.columns(len(data["job_role_match"]))

        for col, job in zip(
            job_cols,
            data["job_role_match"]
        ):

            with col:

                st.markdown(
                    f"### 💼 {job['role']}"
                )

                st.metric(
                    "Match",
                    f"{job['match_percentage']}%"
                )

                st.progress(
                    job["match_percentage"] / 100
                )

                st.write(job["reason"])
        # -------------------------
        # TARGET JOB MATCH
        # -------------------------

        if data.get("job_description_match"):

            st.subheader("🎯 Target Job Match")

            job_match = data["job_description_match"]

            # Score + Progress
            match_col1, match_col2 = st.columns([1, 2])

            with match_col1:
                st.metric(
                "Job Match Score",
                f"{job_match['match_score']}%"
                )

            with match_col2:
                st.write("### 📈 Job Compatibility")
                st.progress(job_match["match_score"] / 100)

            st.divider()

            # Matching Skills
            st.write("### ✅ Matching Skills")

            matching_skills = job_match["matching_skills"]

            if matching_skills:
                for skill in matching_skills:
                    st.markdown(
                        f"""
                        <span style="
                        display:inline-block;
                        padding:6px 12px;
                        margin:4px;
                        border-radius:15px;
                        border:1px solid #28a745;
                        background:#f0fff4;
                    ">
                    {skill}
                    </span>
                    """,
                    unsafe_allow_html=True
                    )
            else:
                st.write("No matching skills found.")

            st.divider()

            # Missing Job Skills
            st.write("### ❌ Missing Job Skills")

            missing_skills = job_match["missing_job_skills"]

            if missing_skills:
                for skill in missing_skills:
                    st.markdown(
                        f"""
                        <span style="
                            display:inline-block;
                            padding:6px 12px;
                            margin:4px;
                            border-radius:15px;
                            border:1px solid #dc3545;
                            background:#fff5f5;
                        ">
                        {skill}
                        </span>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.success("No major missing skills found! 🎉")

            st.divider()

            # Job Specific Suggestions
            st.write("### 💡 Job-Specific Suggestions")

            for suggestion in job_match["suggestions"]:
                st.info(suggestion)
        # -------------------------
        # SUGGESTIONS
        # -------------------------

        st.subheader("💡 Suggestions")

        for index, suggestion in enumerate(
            data["suggestions"],
            start=1
        ):
            st.info(
            f"**{index}.** {suggestion}"
            )
        # -------------------------
        # DOWNLOAD REPORT
        # -------------------------

        report_file = generate_report(data)

        with open(report_file, "rb") as file:
            st.download_button(
               label="📥 Download Analysis Report",
               data=file,
               file_name="resume_analysis_report.pdf",
               mime="application/pdf"
            )