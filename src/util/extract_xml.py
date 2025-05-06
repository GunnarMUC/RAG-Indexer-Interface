import re


def extract_xml_tag(content: str, tag: str) -> str:
    pattern = re.compile(f"<{tag}>(.*?)</{tag}>", re.DOTALL | re.MULTILINE)
    match = pattern.search(content.strip())
    if match:
        return match.group(1).strip()
    return None
