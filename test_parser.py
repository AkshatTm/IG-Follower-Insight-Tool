from src.parser import _extract_username

def test():
    # Test valid username
    entry = {"string_list_data": [{"value": "valid_user.name123"}]}
    assert _extract_username(entry) == "valid_user.name123"

    # Test username with malicious injection characters
    entry_malicious = {"string_list_data": [{"value": "=cmd|' /C calc'!A0"}]}
    assert _extract_username(entry_malicious) == "cmdCcalcA0"

    # Test username with XSS
    entry_xss = {"string_list_data": [{"value": "<script>alert(1)</script>"}]}
    assert _extract_username(entry_xss) == "scriptalert1script"

    print("All tests passed.")

if __name__ == "__main__":
    test()
