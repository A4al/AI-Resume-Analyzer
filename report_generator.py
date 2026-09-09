from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

def generate_report(data, filename="resume_analysis_report.pdf"):

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["BodyText"]

    content = []

    # -------------------------
    # TITLE
    # -------------------------

    content.append(
        Paragraph(
            "AI Resume Analysis Report",
            title_style
        )
    )

    content.append(Spacer(1, 20))

    # -------------------------
    # RESUME SCORE
    # -------------------------

    content.append(
        Paragraph(
            "Resume Score",
            heading_style
        )
    )

    content.append(
        Paragraph(
            f"<b>{data['resume_score']}/100</b>",
            normal_style
        )
    )

    content.append(Spacer(1, 10))

    content.append(
        Paragraph(
            data["score_explanation"],
            normal_style
        )
    )

    content.append(Spacer(1, 20))

    # -------------------------
    # SKILLS DETECTED
    # -------------------------

    content.append(
        Paragraph(
            "Skills Detected",
            heading_style
        )
    )

    for skill in data["skills_detected"]:
        content.append(
            Paragraph(
                f"• {skill}",
                normal_style
            )
        )

    content.append(Spacer(1, 15))

    # -------------------------
    # MISSING SKILLS
    # -------------------------

    content.append(
        Paragraph(
            "Missing Skills",
            heading_style
        )
    )

    for skill in data["missing_skills"]:
        content.append(
            Paragraph(
                f"• {skill}",
                normal_style
            )
        )

    content.append(Spacer(1, 20))

    # -------------------------
    # JOB ROLE MATCH
    # -------------------------

    content.append(
        Paragraph(
            "Job Role Match",
            heading_style
        )
    )

    for job in data["job_role_match"]:

        # Support different possible key names
        role = job.get("role", "Unknown Role")

        match_percentage = job.get(
            "match_percentage",
            job.get("match", 0)
        )

        reason = job.get(
            "reason",
            job.get("explanation", "")
        )

        content.append(
            Paragraph(
                f"<b>{role}</b> - {match_percentage}%",
                normal_style
            )
        )

        if reason:
            content.append(
                Paragraph(
                    reason,
                    normal_style
                )
            )

        content.append(Spacer(1, 8))

    content.append(Spacer(1, 15))

    # -------------------------
    # TARGET JOB MATCH
    # -------------------------

    if data.get("job_description_match"):

        job_match = data["job_description_match"]

        content.append(
            Paragraph(
                "Target Job Match",
                heading_style
            )
        )

        content.append(
            Paragraph(
                f"<b>Match Score:</b> "
                f"{job_match.get('match_score', 0)}%",
                normal_style
            )
        )

        content.append(Spacer(1, 10))

        # Matching Skills

        content.append(
            Paragraph(
                "Matching Skills",
                heading_style
            )
        )

        matching_skills = job_match.get(
            "matching_skills",
            []
        )

        if matching_skills:

            for skill in matching_skills:
                content.append(
                    Paragraph(
                        f"• {skill}",
                        normal_style
                    )
                )

        else:

            content.append(
                Paragraph(
                    "No matching skills found.",
                    normal_style
                )
            )

        content.append(Spacer(1, 10))

        # Missing Job Skills

        content.append(
            Paragraph(
                "Missing Job Skills",
                heading_style
            )
        )

        missing_job_skills = job_match.get(
            "missing_job_skills",
            []
        )

        if missing_job_skills:

            for skill in missing_job_skills:
                content.append(
                    Paragraph(
                        f"• {skill}",
                        normal_style
                    )
                )

        else:

            content.append(
                Paragraph(
                    "No major missing job skills found.",
                    normal_style
                )
            )

        content.append(Spacer(1, 20))

    # -------------------------
    # SUGGESTIONS
    # -------------------------

    content.append(
        Paragraph(
            "Suggestions",
            heading_style
        )
    )

    for i, suggestion in enumerate(
        data["suggestions"],
        1
    ):

        content.append(
            Paragraph(
                f"{i}. {suggestion}",
                normal_style
            )
        )

        content.append(
            Spacer(1, 5)
        )

    # -------------------------
    # BUILD PDF
    # -------------------------

    doc.build(content)

    return filename