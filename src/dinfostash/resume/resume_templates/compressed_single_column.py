from typing import Literal, Union

from pylatex import (Command, Document, NoEscape, Package, Section,
                     VerticalSpace)
from pylatex.base_classes import LatexObject

from ...data.constants import AnyUrlStr
from ...data.models import (Achievement, Education, Experience, Project,
                            ResumeData, Skill)
from .utils import CustomCommand, CustomContextCommand, bold_percentage

CommandArg = Union[str, LatexObject, AnyUrlStr, int, None]


class ItemView(CustomCommand):
    args = 1
    body = r"\item{{#1 \vspace*{-2pt}}}"

    def __init__(self, item: CommandArg) -> None:
        super().__init__(item)


# TODO: try using Latex object for the body of the CustomCommand
class HeadingTwoByTwoView(CustomCommand):
    args = 4
    body = r"\vspace*{-2pt}\item\begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}\vspace*{2pt}\textbf{#1} & #2 \\\textit{#3} & \textit{ #4} \\\end{tabular*}\vspace*{-6pt}"

    def __init__(
        self,
        top_left: CommandArg,
        top_right: CommandArg,
        bottom_left: CommandArg,
        bottom_right: CommandArg,
    ) -> None:
        super().__init__(top_left, top_right, bottom_left, bottom_right)


class DictViewItem(CustomCommand):
    args = 2
    body = r"\item\textbf{#1:} #2\vspace*{-6pt}"

    def __init__(self, key: CommandArg, value: CommandArg) -> None:
        super().__init__(key, value)


class TitleLink(CustomCommand):
    args = 3
    body = r"\textbf{#1} \color{blue}\mdseries\textit{\href{#2}{#3}}"

    def __init__(self, title: CommandArg, link: CommandArg) -> None:
        link_text = "-link" if link else ""
        super().__init__(title, link, link_text)


class SingleLineThreeItem(CustomCommand):
    args = 3
    body = r"\item\vspace*{-4pt}\begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}\textbf{#1} $|$ \footnotesize\emph{#2} & {#3} \\\end{tabular*}\vspace*{-3pt}"

    def __init__(
        self, title: CommandArg, sub_title: CommandArg, data: CommandArg
    ) -> None:
        super().__init__(title, sub_title, data)


class IconLinkView(CustomCommand):
    args = 3
    body = r"\small\faIcon{#1} \href{#2}{\color{blue}\underline{#3}} "

    def __init__(self, icon: CommandArg, link: CommandArg, display: CommandArg) -> None:
        super().__init__(icon, link, display)


class IconLinkViewItem(CustomCommand):
    args = 3
    body = r"\item\large\hspace*{10cm}\hfill\faIcon{#1} \href{#2}{\underline{#3}}\\"

    def __init__(self, icon: CommandArg, link: CommandArg, display: CommandArg) -> None:
        super().__init__(icon, link, display)


class VerticalViewItem(CustomCommand):
    args = 1
    body = r"\item\large\hspace*{2.25cm}\qquad \text{#1} \\"

    def __init__(self, data: CommandArg) -> None:
        super().__init__(data)


class HeaderSection(CustomContextCommand):
    class Start(CustomCommand):
        body = r"\vspace*{-3.5cm}\begin{itemize}[leftmargin=0.15in, label={}]\setlength\itemsep{0.1em}"

    class End(CustomCommand):
        body = r"\end{itemize}"


class SubHeadingList(CustomContextCommand):
    class Start(CustomCommand):
        body = r"\begin{itemize}[leftmargin=0.15in, label={}]"

    class End(CustomCommand):
        body = r"\end{itemize}"


class ItemList(CustomContextCommand):
    class Start(CustomCommand):
        body = r"\begin{itemize}\vspace*{-2pt}"

    class End(CustomCommand):
        body = r"\end{itemize}\vspace*{1pt}"


def import_packages_in_document(doc: Document) -> Document:
    doc.packages.append(Package("inputenc", options=["utf8"]))
    doc.packages.append(Package("fontenc", options=["T1"]))
    doc.packages.append(Package("fontsize"))
    doc.packages.append(Package("mathptmx"))
    doc.packages.append(Package("titlesec"))
    doc.packages.append(Package("enumitem"))
    doc.packages.append(Package("hyperref", options=["hidelinks"]))
    doc.packages.append(Package("fancyhdr"))
    doc.packages.append(Package("xcolor"))
    doc.packages.append(Package("fontawesome5"))
    doc.packages.append(Package("geometry"))
    doc.packages.append(Package("graphicx"))
    doc.packages.append(Package("amsmath"))
    doc.packages.append(Package("setspace"))
    return doc


def add_custom_commands(doc: Document) -> Document:
    ItemView.declaration(doc)
    HeadingTwoByTwoView.declaration(doc)
    DictViewItem.declaration(doc)
    TitleLink.declaration(doc)
    SingleLineThreeItem.declaration(doc)
    IconLinkView.declaration(doc)
    IconLinkViewItem.declaration(doc)
    VerticalViewItem.declaration(doc)
    HeaderSection.declare_command_in_document(doc)
    SubHeadingList.declare_command_in_document(doc)
    ItemList.declare_command_in_document(doc)
    return doc


def define_document_settings(doc: Document) -> Document:
    doc.preamble.append(Command("pagestyle", arguments=["fancy"]))
    doc.preamble.append(Command("fancyhf", arguments=[""]))
    doc.preamble.append(Command("fancyfoot", arguments=[""]))
    doc.preamble.append(
        Command("renewcommand", arguments=[NoEscape(r"\headrulewidth"), "0pt"])
    )
    doc.preamble.append(
        Command("renewcommand", arguments=[NoEscape(r"\footrulewidth"), "0pt"])
    )
    doc.preamble.append(
        Command(
            "changefontsize",
            arguments=["10pt"],
            options=["12.8pt"],
        )
    )
    doc.preamble.append(
        Command(
            "geometry",
            arguments=["a4paper, left=20mm, right=20mm, top=10mm, bottom=10mm"],
        )
    )
    doc.preamble.append(Command("urlstyle", arguments=["same"]))
    doc.preamble.append(Command("raggedbottom"))
    doc.preamble.append(Command("raggedright"))
    doc.preamble.append(
        Command("setlength", arguments=[NoEscape(r"\tabcolsep"), "0in"])
    )
    doc.preamble.append(
        Command(
            "titleformat",
            arguments=[
                NoEscape(r"\section"),
                NoEscape(r"\vspace*{-12pt}\scshape\raggedright\Large\bfseries"),
                "",
                "0em",
                "",
            ],
        )
    )
    doc.preamble.append(NoEscape(r"[\color{black}\titlerule \vspace*{-5pt}]"))
    doc.preamble.append(Command("renewcommand"))
    doc.preamble.append(
        Command(
            "labelitemii", arguments=[NoEscape(r"$\vcenter{\hbox{\tiny$\bullet$}}$")]
        )
    )
    doc.preamble.append(
        Command("setlength", arguments=[NoEscape(r"\footskip"), "4.08003pt"])
    )
    doc.preamble.append(Command("pdfgentounicode=1"))

    return doc


def add_header_section_without_photo(doc: Document, data: ResumeData) -> Document:
    doc.append(Command("setstretch", arguments=["0.5"]))
    doc.append(Command("begin", arguments=["center"]))
    doc.append(
        Command(
            "textbf",
            arguments=[
                NoEscape(rf"\Huge {data.personal_info.name} \\ \vspace*{{10pt}}")
            ],
        )
    )
    doc.append(Command("small"))
    for contact in data.personal_info.contact_infos:
        doc.append(IconLinkView(contact.fa_icon, contact.link, contact.display))
    doc.append(Command("end", arguments=["center"]))

    return doc


def add_header_section_with_photo(doc: Document, data: ResumeData) -> Document:
    doc.append(Command("setstretch", arguments=["0.5"]))
    doc.append(
        Command(
            "includegraphics",
            arguments=[
                data.personal_info.photo,
            ],
            options=["height=3.5cm"],
        )
    )

    with HeaderSection(doc):
        doc.append(
            VerticalViewItem(
                Command(
                    "textbf",
                    arguments=[NoEscape(rf"\huge {data.personal_info.name}")],
                )
            )
        )
        for info in data.personal_info.short_infos:
            doc.append(VerticalViewItem(info))

    doc.append(Command("hfill"))
    doc.append(VerticalSpace("8mm"))

    with HeaderSection(doc):
        for contact_info in data.personal_info.contact_infos:
            doc.append(
                IconLinkViewItem(
                    contact_info.fa_icon,
                    contact_info.link,
                    contact_info.display,
                )
            )

    doc.append(VerticalSpace("5mm"))

    return doc


def add_experience_section(doc: Document, data: list[Experience]) -> Document:
    doc.append(Section("Experience"))
    with SubHeadingList(doc):
        for exp in data:
            doc.append(
                HeadingTwoByTwoView(
                    TitleLink(exp.organization, exp.link),
                    exp.date,
                    exp.position,
                    exp.location,
                )
            )
            with ItemList(doc):
                for decs in exp.descriptions:
                    decs = bold_percentage(decs)
                    doc.append(ItemView(decs))
                doc.append(DictViewItem("Tech Stack", ", ".join(exp.technologies)))

    doc.append(VerticalSpace("1pt"))
    return doc


def add_projects_section(doc: Document, data: list[Project]) -> Document:
    doc.append(Section("Projects"))
    with SubHeadingList(doc):
        for project in data:
            doc.append(
                SingleLineThreeItem(
                    TitleLink(project.name, project.link),
                    project.organization,
                    project.time,
                )
            )
            with ItemList(doc):
                doc.append(ItemView(project.description))
                doc.append(DictViewItem("Tech Stack", ", ".join(project.technologies)))

    doc.append(VerticalSpace("1pt"))
    return doc


def add_education_section(doc: Document, data: list[Education]) -> Document:
    doc.append(Section("Education"))
    with SubHeadingList(doc):
        for i, edu in enumerate(data):
            doc.append(
                HeadingTwoByTwoView(
                    edu.institute,
                    edu.year,
                    edu.degree,
                    f"{edu.marks.type}: {edu.marks.value}",
                )
            )
            if i < len(data) - 1:
                doc.append(VerticalSpace("4pt"))

    doc.append(VerticalSpace("1pt"))
    return doc


def add_skills_section(doc: Document, data: list[Skill]) -> Document:
    doc.append(Section("Skills"))
    with SubHeadingList(doc):
        for skill in data:
            doc.append(DictViewItem(skill.type, ", ".join(skill.values)))

    doc.append(VerticalSpace("1pt"))
    return doc


def add_achievements_section(doc: Document, data: list[Achievement]) -> Document:
    doc.append(Section("Achievements"))
    with SubHeadingList(doc):
        doc.append(VerticalSpace("1pt"))
        for achievement in data:
            doc.append(
                SingleLineThreeItem(
                    achievement.type,
                    # achievement.title + TitleLink(": link", achievement.link).dumps() if achievement.link else achievement.title,
                    TitleLink(achievement.title, achievement.link),
                    achievement.data,
                )
            )

    return doc


def _create_document(data: ResumeData):
    doc = Document()

    doc = import_packages_in_document(doc)

    doc.preamble.append(
        NoEscape("\n% -------------------- CUSTOM COMMANDS --------------------")
    )
    doc = add_custom_commands(doc)

    doc.preamble.append(
        NoEscape("\n\n% -------------------- SETTINGS --------------------")
    )
    doc = define_document_settings(doc)

    doc.preamble.append(
        NoEscape("\n\n% -------------------- HEADING --------------------")
    )
    doc = add_header_section_with_photo(doc, data)

    doc.append(NoEscape("\n\n% -------------------- EDUCATION --------------------"))
    doc = add_education_section(doc, data.educations)

    doc.append(NoEscape("\n\n% -------------------- EXPERIENCE --------------------"))
    doc = add_experience_section(doc, data.experience)

    doc.append(NoEscape("\n\n% -------------------- PROJECTS --------------------"))
    doc = add_projects_section(doc, data.projects)

    doc.append(NoEscape("\n\n% -------------------- SKILLS --------------------"))
    doc = add_skills_section(doc, data.skills)

    doc.append(NoEscape("\n\n% -------------------- ACHIEVEMENTS --------------------"))
    doc = add_achievements_section(doc, data.achievements)

    doc.generate_tex(".dev_utils/example")
