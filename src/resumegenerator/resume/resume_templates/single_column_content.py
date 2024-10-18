from typing import List

from pylatex import (
    Command,
    Document,
    FlushLeft,
    FlushRight,
    HorizontalSpace,
    NoEscape,
    Section,
    Tabular,
    VerticalSpace,
)

from ...data.models import (
    Achievement,
    Education,
    Experience,
    PersonalInfo,
    Project,
    ResumeData,
    Skill,
)


def add_educations(doc: Document, educations: List[Education]) -> None:
    doc.append(NoEscape(r"% % -------------------- EDUCATION --------------------"))

    doc.append(Section("Education"))

    doc.append(Command("resumeSubHeadingListStart"))

    for i, edu in enumerate(educations, start=1):
        doc.append(
            Command(
                "resumeSubheading",
                arguments=[
                    rf"{edu.institute}",
                    edu.year,
                    edu.degree,
                    f"{edu.marks.type}: {edu.marks.value}",
                ],
            )
        )

        if i != len(educations):
            doc.append(VerticalSpace("4pt"))

    doc.append(Command("resumeSubHeadingListEnd"))


def add_skills(doc: Document, skills: List[Skill]) -> None:
    doc.append(NoEscape(r"% % -------------------- SKILLS --------------------"))

    doc.append(Section("Skills"))

    doc.append(NoEscape(r"\begin{itemize}[leftmargin=0.15in, label={}]"))

    doc.append(
        Command(
            "small",
            arguments=[
                Command(
                    "item",
                    arguments=[
                        NoEscape(
                            "\n".join(
                                [
                                    rf"\textbf{{{skill.type}}}{{{': ' + ', '.join(skill.values)}}} \\"
                                    for skill in skills
                                ]
                            )
                        )
                    ],
                )
            ],
        )
    )

    doc.append(Command("end", arguments=["itemize"]))


def add_expirence(doc: Document, exps: List[Experience]):
    doc.append(NoEscape(r"%% -------------------- EXPERIENCE --------------------"))
    doc.append(Section("Professional Experience"))

    doc.append(Command("resumeSubHeadingListStart"))

    for exp in exps:
        doc.append(
            Command(
                r"resumeProjectHeading",
                arguments=[
                    NoEscape(
                        rf"\textbf{'{'}\href{{{exp.link}}}{'{'}\underline{{{exp.organization+'}'}}}}}"
                        + " $|$ "
                        + rf"\footnotesize\emph{{{exp.position}}}\vspace{{8pt}}{'}'}{{{exp.date}}}"
                        + "\\\\\n".join(
                            rf"{{\small{{{dec}}}}}" for dec in exp.descriptions
                        )
                        + "\\\\\n"
                        + rf"{{\small{{{', '.join(exp.technologies)}}}"
                    )
                ],
            )
        )

    doc.append(Command("resumeSubHeadingListEnd"))


def add_projects(doc: Document, projects: List[Project]):
    doc.append(NoEscape(r"%% -------------------- PROJECTS --------------------"))
    doc.append(Section("Projects"))
    doc.append(Command("resumeSubHeadingListStart"))

    for proj in projects:
        doc.append(Command("resumeProjectHeading"))
        doc.append(
            NoEscape(
                r"{\textbf{\href{"
                + str(proj.link)
                + r"}{\underline{"
                + proj.name
                + r"}}} $|$ \footnotesize\emph{"
                + ", ".join(proj.technologies)
                + r"}}{}"
            )
        )
        doc.append(Command("resumeItemListStart"))
        doc.append(Command("resumeItem", arguments=[proj.description]))
        doc.append(Command("resumeItemListEnd"))

    doc.append(Command("resumeSubHeadingListEnd"))


def add_achievements(doc: Document, achievements: List[Achievement]):
    doc.append(NoEscape(r"%% -------------------- ACHIEVEMENTS --------------------"))
    doc.append(Section("Achievements"))
    doc.append(Command("resumeSubHeadingListStart"))

    for achiev in achievements:
        doc.append(Command("resumeProjectHeading"))
        doc.append(
            NoEscape(
                # {\textbf{Patent} $|$ \footnotesize\emph{Drain Clogging Prevention System}}{Application no. :202211017463}
                r"{\textbf{"
                + achiev.type
                + r"} $|$ \footnotesize\emph{"
                + achiev.title
                + r"}}{"
                + achiev.data
                + "}"
            )
        )

    doc.append(Command("resumeSubHeadingListEnd"))


def set_resume_header_for_nophoto(doc: Document, data: PersonalInfo):
    doc.append(NoEscape(r"% % -------------------- HEADING --------------------"))

    doc.append(
        NoEscape(
            rf"""
\begin{{flushright}}
\end{{flushright}}

\begin{{center}}
    \textbf{{\Huge \scshape {data.name}}} \\ \vspace{{8pt}}
    \small """
        )
    )

    doc.append(
        NoEscape(
            " $ $\n".join(
                rf"\faIcon{{{contact.fa_icon}}} \href{{{contact.link}}}{{\underline{{{contact.display}}}}}"
                for contact in data.contact_infos
            )
        )
    )

    doc.append(NoEscape(r"\end{center}"))


def set_resume_header_for_photo(doc: Document, data: PersonalInfo):
    doc.append(NoEscape(r"% % -------------------- HEADING --------------------"))

    with doc.create(FlushLeft()):
        doc.append(HorizontalSpace("0.5cm"))
        doc.append(
            Command(
                "includegraphics",
                arguments=[data.photo],
                options="height=4cm",
            )
        )

    doc.append(NoEscape(r"\vspace{-150pt}"))

    with doc.create(FlushRight()):
        doc.append(
            Command(
                "textbf",
                arguments=[NoEscape(rf"\Huge {data.name}  \\ \vspace{{8pt}}")],
            )
        )

        with doc.create(Tabular("ll")):
            doc.append(VerticalSpace("6pt"))
            doc.append(
                NoEscape(
                    " \\\\ \\vspace{8pt}\n".join(
                        rf"\faIcon{{{contact.fa_icon}}} & \href{{{contact.link}}}{{\underline{{{contact.display}}}}}"
                        for contact in data.contact_infos
                    )
                )
            )
            doc.append(VerticalSpace("6pt"))


def create_document_with_nophoto(data: ResumeData) -> Document:
    latex = Document(documentclass="article", document_options=["letterpaper", "11pt"])

    with open(
        "ResumeGenerator/src/resume/resume_templates/single_column_nophoto_preamble.tex",
        "r",
        encoding="utf-8",
    ) as file:
        latex.preamble.append(NoEscape(file.read()))

    set_resume_header_for_nophoto(latex, data.personal_info)

    add_educations(latex, data.educations)
    add_skills(latex, data.skills)
    add_expirence(latex, data.experience)
    add_projects(latex, data.projects)
    add_achievements(latex, data.achievements)

    return latex


def create_document_with_photo(data: ResumeData) -> Document:
    latex = Document(documentclass="article", document_options=["letterpaper", "11pt"])

    with open(
        "ResumeGenerator/src/resume/resume_templates/single_column_photo_preamble.tex",
        "r",
        encoding="utf-8",
    ) as file:
        latex.preamble.append(NoEscape(file.read()))

    set_resume_header_for_photo(latex, data.personal_info)

    add_educations(latex, data.educations)
    add_skills(latex, data.skills)
    add_expirence(latex, data.experience)
    add_projects(latex, data.projects)
    add_achievements(latex, data.achievements)

    return latex
