import streamlit as st
import json

from resume_parser import extract_text_from_pdf
from ai_analyzer import analyze_resume


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and get AI-powered feedback.")


resume = st.file_uploader(
    "Upload your Resume",
    type=["pdf"]
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
    job_description = st.text_area(
        "🎯 Target Job Description (Optional)",
        placeholder="Paste the job description here...",
        height=250
    )
    if st.button("🤖 Analyze Resume"):

        with st.spinner("AI is analyzing your resume..."):

            analysis = analyze_resume(text, job_description)

        try:
            analysis = analysis.strip()

            # Remove Markdown code fences like ```json or ```python
            if analysis.startswith("```"):
                analysis = analysis.split("\n", 1)[1]

            if analysis.endswith("```"):
                analysis = analysis[:-3]

            analysis = analysis.strip()

            data = json.loads(analysis)

        except json.JSONDecodeError:
            st.error("AI returned an invalid JSON response. Please try Analyze Resume again.")
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

        for col, job in zip(job_cols, data["job_role_match"]):

            with col:
                st.markdown(f"### 💼 {job['role']}")

                st.metric(
                    "Match",
                    f"{job['match_percentage']}%"
                )

                st.progress(job["match_percentage"] / 100)

                st.write(job["reason"])
                if data.get("job_description_match"):

                    st.subheader("🎯 Target Job Match")

                    job_match = data["job_description_match"]

                    st.metric(
                        "Job Match Score",
                        f"{job_match['match_score']}/100"
                    )

                    st.write("### ✅ Matching Skills")

                    for skill in job_match["matching_skills"]:
                        st.write(f"• {skill}")

                    st.write("### ❌ Missing Job Skills")

                    for skill in job_match["missing_job_skills"]:
                        st.write(f"• {skill}")

                    st.write("### 💡 Job-Specific Suggestions")

                    for suggestion in job_match["suggestions"]:
                        st.write(f"• {suggestion}")
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