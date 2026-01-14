def normalize_gravity_tests(tests):
    normalized = []
    for i, tc in enumerate(tests, start=1):
        normalized.append({
            "id": f"TC-G-{i}",
            "input": tc["input"],
            "expected_tool": tc["expected_tool"],
            "expected_behavior": tc["expected_behavior"]
        })
    return normalized
