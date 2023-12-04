import re

def vowel_counter(s: str) -> int: return len(re.findall("a|e|i|o|u|y", s.lower()))

print(vowel_counter("I stole the shed"))