import re


def replace_quotes(text):
    def replace_match(match):
        return '«' + match.group(1) + '»'
    return re.sub(r'"([^"]*)"', replace_match, text)


def fool_proof(text, replacement):
    if not hasattr(fool_proof, "statics"):
        fool_proof.statics = True
        fool_proof.replacer = re.compile(r'[^а-яА-ЯёЁ0-9.,«»"\- ]+')
        fool_proof.checker = re.compile(r'[а-яА-ЯёЁ]{2,}')
    text = fool_proof.replacer.sub('☒', text).strip()
    return replace_quotes(text) if fool_proof.checker.search(text) else replacement
