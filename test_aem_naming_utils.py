import pytest
from aem_naming_utils import AemNamingUtils

@pytest.mark.parametrize(
    "instr, outstr",
    [
        ('filename--with--multiple--hypens', 'filename-with-multiple-hypens'),
        ('multiple  spaces', 'multiple-spaces'),
        ('extra space at the end ', 'extra-space-at-the-end'),
        (' extra space at the beginning', 'extra-space-at-the-beginning'),
        ('extra hypen at end-', 'extra-hypen-at-end'),
        ('-extra hyphen at begining', 'extra-hyphen-at-begining'),
        ('-extra hyphen at begining and end-', 'extra-hyphen-at-begining-and-end'),
        ('----extra hyphens at begining and end--', 'extra-hyphens-at-begining-and-end'),
        ('one_underscore', 'one-underscore'),
        ('multiple___underscores', 'multiple-underscores'),
        ('underscore at end_', 'underscore-at-end'),
        ('_underscore at beginnning', 'underscore-at-beginnning'),
        ('_underscore at beginnning and end_', 'underscore-at-beginnning-and-end'),
        ('awesome   filename with extention.PDF____   -----', 'awesome-filename-with-extention.pdf'),
        ('__  ---- %@#@ ^^^!@#$*() awesome   filename with extention.PDF____   -----', 'awesome-filename-with-extention.pdf'),
        ('__  \'---- "" %@#@ nothing^^^!@#$*(somehting) awesome   filename with extention.PDF____   -----', 'nothing-somehting-awesome-filename-with-extention.pdf'),
        ('__  ---- %@#@ 1.3 nothing^^^!@#$*(somehting) awesome   filename with extention.PDF____   -----', '1-3-nothing-somehting-awesome-filename-with-extention.pdf'),
        ('filename ™ with trademark ™', 'filename-with-trademark'),
        ('filename ® with copyright ® ', 'filename-with-copyright'),
        ('filename with single quote \' in it', 'filename-with-single-quote-in-it'),
        ('filename with double quote \" in it', 'filename-with-double-quote-in-it'),
    ]
)
def test_create_proper_name(instr, outstr):
    anu = AemNamingUtils()
    name = anu.create_proper_name(instr)
    assert name == outstr
