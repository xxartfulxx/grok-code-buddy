from pygments import highlight
from pygments.lexers import PythonLexer, get_lexer_by_name
from pygments.formatters import NullFormatter

def format_code_block(content):
    """Format code blocks using Pygments."""
    lines = content.split('\n')
    result = []
    in_code_block = False
    code_buffer = []
    language = None

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            if in_code_block:
                try:
                    lexer = get_lexer_by_name(language) if language else PythonLexer()
                    formatted = highlight('\n'.join(code_buffer), lexer, NullFormatter())
                    result.append('\n'.join('    ' + l for l in formatted.split('\n')))
                except Exception:
                    result.append('\n'.join('    ' + l for l in code_buffer))
                code_buffer = []
                in_code_block = False
                language = None
            else:
                in_code_block = True
                lang = stripped[3:].strip()
                language = lang if lang else None
        elif in_code_block:
            code_buffer.append(line)
        else:
            result.append(line)

    return '\n'.join(result)