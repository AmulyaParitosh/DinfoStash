import contextlib
import re

from pylatex import Document, NoEscape, UnsafeCommand
from pylatex.base_classes import Arguments, CommandBase


class _CustomMeta(type):
    """this meta class is used to modify the _latex_name attribute of the class.
    The _latex_name attribute is used to store the name of the command in latex.
    It is set as the class name but with its first letter in lowercase.
    """

    def __new__(cls, name, bases, dct):
        dct["_latex_name"] = name[0].lower() + name[1:]
        return super().__new__(cls, name, bases, dct)


_LatexMeta = type(CommandBase)


class _NewMeta(_LatexMeta, _CustomMeta): ...


class CustomCommand(CommandBase, metaclass=_NewMeta):
    args: int = None
    body: str

    def __init__(self, *args) -> None:
        with contextlib.suppress(AttributeError):
            # args = [NoEscape(a) for a in args]
            args = [
                NoEscape(a.dumps()) if isinstance(a, CommandBase) else NoEscape(a)
                for a in args
            ]
        super().__init__(arguments=Arguments(*args))

    @classmethod
    def declaration(cls, doc: Document) -> Document:
        doc.preamble.append(
            UnsafeCommand(
                "newcommand",
                rf"\{cls._latex_name}",
                options=cls.args,
                extra_arguments=cls.body,
            )
        )
        return doc


class CustomContextCommandMeta(type):
    """
    This metaclass is used to modify the class to include the enter_command and exit_command
    as instances of the CustomCommand class.
    It is for classes that are used as context managers in latex. (the commands that require a start and end tag)
    When a class containing Start and End classes is created, the enter_command and exit_command are created as instances
    of the Start and End classes respectively. But the Start and End classes are modified to have the same name as the
    class containing them. i.e. if the class containing the Start and End classes is called HeaderSection, the Start and
    End classes will be called HeaderSectionStart and HeaderSectionEnd respectively.
    """

    def __new__(cls, name, bases, dct):
        new_dct = dct.copy()
        for key, value in dct.items():
            if isinstance(value, type) and key == "Start":
                new_dct["enter_command"] = cls.__modified_class(name, value)()

            elif isinstance(value, type) and key == "End":
                new_dct["exit_command"] = cls.__modified_class(name, value)()

        return super().__new__(cls, name, bases, new_dct)

    @classmethod
    def __modified_class(cls, base_class_name: str, inner_class: type):
        """
        This method is used to create a new class with the same name as the base_class_name and the inner_class
        """
        return type(
            base_class_name + inner_class.__name__,
            inner_class.__bases__,
            dict(inner_class.__dict__),
        )


class CustomContextCommand(metaclass=CustomContextCommandMeta):

    enter_command: CustomCommand
    exit_command: CustomCommand

    def __init__(self, doc: Document) -> None:
        self.doc = doc

    def __enter__(self):
        self.doc.append(self.enter_command)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.doc.append(self.exit_command)

    @classmethod
    def declare_command_in_document(cls, doc: Document) -> Document:
        cls.enter_command.declaration(doc)
        cls.exit_command.declaration(doc)
        return doc

def bold_percentage(text: str) -> str:
    """
    This function is used to make the percentage in the text bold.
    """
    pattern = r'\b\d+(\.\d+)?\\%'

    return re.sub(
        pattern,
        lambda match: r"\textbf{" + match.group(0) + "}",
        text,
    )
