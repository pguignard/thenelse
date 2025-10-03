from ..models import Languages, Levels

from .javascript import themes as js_themes
from .python import themes as py_themes
from .c import themes as c_themes
from .typescript import themes as ts_themes
from .cpp import themes as cpp_themes
from .csharp import themes as csharp_themes
from .java import themes as java_themes


themes_data = {
    Languages.JAVASCRIPT: js_themes,
    Languages.PYTHON: py_themes,
    Languages.TYPESCRIPT: ts_themes,
    Languages.C: c_themes,
    Languages.CPP: cpp_themes,
    Languages.CSHARP: csharp_themes,
    Languages.JAVA: java_themes,
}
