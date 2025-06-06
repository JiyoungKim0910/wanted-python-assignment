def get_localized(items, lang: str) -> str | None:
    """
    언어 코드(lang)에 해당하는 name을 반환,
    없으면 첫 번째 값을 fallback으로 반환
    """
    lang_map = {item.language: item.name for item in items}
    return lang_map.get(lang) or next(iter(lang_map.values()), None)

def get_localized_strict(items, lang: str) -> str | None:
    """
    언어 코드(lang)가 정확히 일치할 때만 반환, 없으면 None
    """
    for item in items:
        if item.language == lang:
            return item.name
    return None