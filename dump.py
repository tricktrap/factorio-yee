from draftsman.blueprintable import Blueprint, BlueprintBook
from draftsman import utils

from sys import stdin, stdout

# read stdin
input = stdin.read()

# parse input
data = Blueprint(input)

print(data)