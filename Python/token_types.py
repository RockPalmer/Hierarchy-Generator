import re

class TokenType:
	def __init__(self,**args) -> None:
		self.args = {k : v for k,v in args.items()}
	def __getattr__(self,name):
		return self.args[name]

TOKENS = [
	TokenType(
		pattern = re.compile(r'\s*\/\s*'),
		symbol = '/',
		names = {
			'FORWARD_SLASH',
			'PositionalDelimiter',
			'Ordering',
			'RenameWith.DELIMITER',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*<-\s*'),
		symbol = '<-',
		names = {
			'LEFT_ARROW',
			'ParentReference',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*:\s*'),
		symbol = ':',
		names = {
			'COLON',
			'Instance',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*<\s*'),
		symbol = '<',
		names = {
			'LESS_THAN',
			'Inheritance',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*>\s*'),
		symbol = '>',
		names = {
			'GREATER_THAN',
			'Providing',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*=\s*'),
		symbol = '=',
		names = {
			'EQUAL',
			'Equivalence',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*\.\s*'),
		symbol = '.',
		names = {
			'DOT',
			'ENTITY_ATTRIBUTE_ACCESS'
		}
	),
	TokenType(
		pattern = re.compile(r'\s*!\s*'),
		symbol = '!',
		names = {
			'EXCLAMATION',
			'ENTITY_ARGUMENT_ACCESS'
		}
	),
	TokenType(
		pattern = re.compile(r'\s*\{\s*'),
		symbol = '{',
		names = {
			'LEFT_CURLY',
			'AttributeList.OPEN',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*\}\s*'),
		symbol = '}',
		names = {
			'RIGHT_CURLY',
			'AttributeList.CLOSE',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*\(\s*'),
		symbol = '(',
		names = {
			'LEFT_PAR',
			'General.OPEN',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*\)\s*'),
		symbol = ')',
		names = {
			'RIGHT_PAR',
			'General.CLOSE',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*,\s*'),
		symbol = ',',
		names = {
			'COMMA',
			'NameList.DELIMITER',
			'ArgumentList.DELIMITER',
			'RenameBody.DELIMITER',
			'ProjectionBody.DELIMITER',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*\|\s*'),
		symbol = '|',
		names = {
			'VERTICAL_BAR',
			'Union.DELIMITER',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*&\s*'),
		symbol = '&',
		names = {
			'AMPERSAND',
			'Intersection.DELIMITER',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*&\s*'),
		symbol = '^',
		names = {
			'CARROT',
			'SymmetricDifference.DELIMITER',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*\*\s*'),
		symbol = '*',
		names = {
			'ASTERISK',
			'CartesianProduct.DELIMITER',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*-\s*'),
		symbol = '-',
		names = {
			'HYPHEN',
			'Difference.DELIMITER',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*---\s*'),
		symbol = '---',
		names = {
			'TRIPLE_HYPHEN',
			'InnerJoin.DELIMITER',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*>--\s*'),
		symbol = '>--',
		names = {
			'GREATER_THAN_DOUBLE_HYPHEN',
			'LeftJoin.DELIMITER',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*--<\s*'),
		symbol = '--<',
		names = {
			'DOUBLE_HYPHEN_LESS_THAN',
			'RightJoin.DELIMITER',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*>-<\s*'),
		symbol = '>-<',
		names = {
			'GREATER_THAN_HYPHEN_LESS_THAN',
			'FullJoin.DELIMITER',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*\$\s*'),
		symbol = '$',
		names = {
			'DOLLAR_SIGN',
			'Select.DELIMITER',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*%\s*'),
		symbol = '%',
		names = {
			'PERCENT_SIGN',
			'Projection.DELIMITER',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*@\s*'),
		symbol = '@',
		names = {
			'AT_SIGN',
			'Alias.DELIMITER',
		}
	),
	TokenType(
		pattern = re.compile(r'\s*~\s*'),
		symbol = '~',
		names = {
			'TILDE',
			'Rename.DELIMITER',
		}
	),
]

def symbol_of(*values : tuple[str,...]) -> str:
	vals = set(values)
	return [token.symbol for token in TOKENS if vals <= token.names][0]