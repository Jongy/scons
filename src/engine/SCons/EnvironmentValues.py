import re

_is_valid_var = re.compile(r'[_a-zA-Z]\w*$')

_rm = re.compile(r'\$[()]')
_remove = re.compile(r'\$\([^$]*(\$[^)][^$]*)*\$\)')

# Regular expressions for splitting strings and handling substitutions,
# for use by the scons_subst() and scons_subst_list() functions:
#
# The first expression compiled matches all of the $-introduced tokens
# that we need to process in some way, and is used for substitutions.
# The expressions it matches are:
#
#       "$$"
#       "$("
#       "$)"
#       "$variable"             [must begin with alphabetic or underscore]
#       "${any stuff}"
#
# The second expression compiled is used for splitting strings into tokens
# to be processed, and it matches all of the tokens listed above, plus
# the following that affect how arguments do or don't get joined together:
#
#       "   "                   [white space]
#       "non-white-space"       [without any dollar signs]
#       "$"                     [single dollar sign]
#
_dollar_exps_str = r'\$[\$\(\)]|\$[_a-zA-Z][\.\w]*|\${[^}]*}'
_dollar_exps = re.compile(r'(%s)' % _dollar_exps_str)
_separate_args = re.compile(r'(%s|\s+|[^\s$]+|\$)' % _dollar_exps_str)

# This regular expression is used to replace strings of multiple white
# space characters in the string result from the scons_subst() function.
_space_sep = re.compile(r'[\t ]+(?![^{]*})')

class ValueTypes(object):
    """
    Enum to store what type of value the variable holds.
    """
    UNKNOWN = 0
    STRING = 1
    CALLABLE = 2
    VARIABLE = 3


class EnvironmentValue(object):
    """
    Hold a single value. We're going to cache parsed version of the file
    We're going to keep track of variables which feed into this values evaluation
    """
    def __init__(self, value):
        self.value = value
        self.var_type = ValueTypes.UNKNOWN

        if callable(self.value):
            self.var_type = ValueTypes.CALLABLE
        else:
            self.parse_value()


    def parse_value(self):
        """
        Scan the string and break into component values
        """

        try:
            if '$' not in self.value:
                self._parsed = self.value
                self.var_type = ValueTypes.STRING
            else:
                # Now we need to parse the specified string
                result = _dollar_exps.sub(sub_match, args)
                print(result)
            pass
        except TypeError:
            # likely callable? either way we don't parse
            self._parsed = self.value

    def parse_trial(self):
        """
        Try alternate parsing methods.
        :return:
        """
        parts = []
        for c in self.value:
            pass



class EnvironmentValues(object):
    """
    A class to hold all the environment variables
    """
    def __init__(self, **kw):
        self._dict = {}
        for k in kw:
            self._dict[k] = EnvironmentValue(kw[k])
