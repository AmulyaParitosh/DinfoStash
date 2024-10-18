import argparse
from argparse import Namespace
from pathlib import Path

from .resume import ResumeTemplateEnum, create_resume_from_file


def list_templates() -> None:
    print("The available resume formats are:")
    for i, template in enumerate(
        (template.value for template in ResumeTemplateEnum), start=1
    ):
        print(f"\t{i}. {template}")


def generate_resume(args: Namespace) -> None:
    create_resume_from_file(
        args.datafile_path,
        args.output_path,
        args.template,
    )
    print("Resume generated successfully.")


def parse_args() -> Namespace:
    parser = argparse.ArgumentParser(
        prog="resume-generator",
        description="Generate a resume based on provided data.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    formats_parser = subparsers.add_parser("templates", help="List available formats.")
    # formats_parser.add_argument(
    #     "ls",
    #     help="List of all available templates.",
    #     action="store_false",
    # )

    generate_parser = subparsers.add_parser("generate", help="Generate a resume.")
    generate_parser.add_argument(
        "datafile_path",
        metavar="DATAFILE_PATH",
        help="Path to the data file containing resume information.",
        type=Path,
    )
    generate_parser.add_argument(
        "output_path",
        metavar="OUTPUT_PATH",
        help="Path to the output file for the generated resume.",
        type=Path,
    )
    generate_parser.add_argument(
        "template",
        metavar="RESUME_TEMPLATE",
        type=lambda x: ResumeTemplateEnum[x],
        choices=list(ResumeTemplateEnum),
        help="Template of the output resume format.",
    )

    command_group = generate_parser.add_mutually_exclusive_group()
    # TODO: add function for resume preview before saving
    command_group.add_argument(
        "--preview",
        action="store_true",
        help="Preview the generated resume without saving.",
    )
    # TODO: add function for data validation
    command_group.add_argument(
        "--validate",
        action="store_true",
        help="Validate the input data file.",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose mode for debugging.",
    )

    return parser.parse_args()


def main() -> None:
    args: Namespace = parse_args()
    if args.subcommand == "templates":
        list_templates()
    elif args.subcommand == "generate":
        generate_resume(args)
    else:
        raise ValueError(f"Invalid subcommand {args.subcommand}.")


if __name__ == "__main__":
    main()
