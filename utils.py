from pygments import highlight
from pygments.lexers import PythonLexer, get_lexer_by_name
from pygments.formatters import NullFormatter
from pygments.token import Token

def format_code_block(content):
    """Format code blocks with Pygments, returning tagged text for Tkinter."""
    print(f"Input content: {content[:50]}...")
    lines = content.split('\n')
    result = []  # List of (text, tag) tuples
    in_code_block = False
    code_buffer = []
    language = None

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            if in_code_block:
                print(f"End code block, language: {language}, buffer: {code_buffer}")
                try:
                    lexer = get_lexer_by_name(language) if language else PythonLexer()
                    tokens = lexer.get_tokens('\n'.join(code_buffer))
                    for token_type, value in tokens:
                        tag = 'normal'
                        if token_type in Token.Keyword:
                            tag = 'keyword'
                        elif token_type in Token.String:
                            tag = 'string'
                        elif token_type in Token.Comment:
                            tag = 'comment'
                        for subline in value.split('\n'):
                            if subline:
                                result.append(('    ' + subline + '\n', tag))
                            else:
                                result.append(('\n', 'normal'))
                except Exception as e:
                    print(f"Pygments error: {e}")
                    for line in code_buffer:
                        result.append(('    ' + line + '\n', 'normal'))
                code_buffer = []
                in_code_block = False
                language = None
            else:
                in_code_block = True
                lang = stripped[3:].strip()
                language = lang if lang else None
                print(f"Start code block, detected language: {language}")
        elif in_code_block:
            code_buffer.append(line)
        else:
            result.append((line + '\n', 'normal'))

    print(f"Formatted output: {result[:50]}...")
    return result