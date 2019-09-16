import os
from glob import glob
try:
    import regex as re
except ImportError:
    import re

token_pattern = re.compile(r"{{([\w_]+)}}")


class nre_obj:
    def __init__(self, d, title=""):
        doc = "# " + title if title != "" else '# Regular expressions: '
        for k, v in d.items():
            setattr(self, k, v)
            doc += '\n\t{k}={v}'.format(k=k, v=v.pattern)
        setattr(self, "__doc__", doc)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def __contains__(self, key):
        return hasattr(self, key)

    def __len__(self):
        return -1 + len(self.__doc__.split('\n'))

    def __str__(self):
        return self.__doc__

    def __repr__(self):
        return self.__doc__


def validate(lines):
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("#"):
            continue
        if line.find("=") > 0:
            continue
        raise SyntaxError(
            "Error in line {i}: Not a variable assignment (a=expression) or a comment (#) \n {l}\n".format(i=i, l=line))


def from_string(content, title=""):
    if type(content) == str:
        lines = [line.strip() for line in content.split("\n") if any(line.strip()) and not line.strip().startswith("#")]
    elif type(content) == list:
        lines = content
    else:
        raise TypeError("`content` should be a string")
    validate(lines)
    expressions = [line.split("=", 1) for line in lines if line.find("=") > 0]
    # Reading regular expressions
    res = {}
    for var, exp in expressions:
        tokens = token_pattern.findall(exp)
        res[var] = exp
        try:
            for token in tokens:
                res[var] = res[var].replace('{{' + token + '}}', res[token])
        except KeyError as e:
            raise SyntaxError("Expression {e} was evaluated but not defined".format(e=e.args[0]))
    # compile
    for k in res.keys():
        try:
            res[k] = re.compile(res[k])
        except:
            raise SyntaxError("Error compiling regular expression {v} = {e}\n".format(e=res[k], v=k))
    return nre_obj(res, title)


def read_imports(file_name):
    if not os.path.exists(file_name):
        #smart-search for nre files
        f = file_name if '.nre' in file_name else file_name + '.nre'
        file_names = glob(f)+glob('../*/'+f)+glob("*/"+f)+glob("../../*/"+f)+glob("../../*/*/"+f)+glob("*/*/"+f)
        if not any(file_names):
            raise FileNotFoundError(file_name)
        file_name = file_names[0] 
    content = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("import "):
                content.extend(read_imports(line[7:].strip()))
            elif not line.startswith("#"):
                content.append(line)
    return content


def from_file(file_name):
    return from_string(read_imports(file_name), file_name)


if __name__ == "__main__":
    my_regex = from_string(r'''
    number=\d+
    decimal={{number}}\.{{number}}
    ''')
    print (my_regex.__doc__)
    print(my_regex.decimal.findall("123.22"))
    print(my_regex.decimal.findall("abc"))
