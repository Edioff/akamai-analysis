"""
Akamai Bot Manager v2 — String Obfuscation Pattern (Generic Example)

This demonstrates the general pattern Akamai uses for string obfuscation
in their bot detection scripts. The actual implementation uses different
values and additional layers of obfuscation.

Pattern:
1. All strings are stored in a single array
2. The array is rotated by a fixed offset at script initialization
3. A decoder function retrieves strings by index with numeric offset

This is a simplified, educational example — not the actual Akamai code.
"""


def create_string_store(strings: list[str], rotation: int) -> list[str]:
    """Simulate Akamai's rotated string array initialization."""
    rotated = strings[rotation:] + strings[:rotation]
    return rotated


def decode_string(store: list[str], index: int, offset: int = 0) -> str:
    """
    Simulate Akamai's string decoder function.

    In the real script, this function is called thousands of times
    with different index/offset combinations to retrieve obfuscated strings.
    """
    actual_index = index - offset
    if 0 <= actual_index < len(store):
        return store[actual_index]
    return ""


# --- Example usage ---

if __name__ == "__main__":
    # Original strings (before obfuscation)
    original_strings = [
        "navigator",
        "userAgent",
        "platform",
        "hardwareConcurrency",
        "deviceMemory",
        "languages",
        "cookieEnabled",
        "doNotTrack",
        "maxTouchPoints",
        "connection",
        "webdriver",
        "plugins",
    ]

    # Step 1: Rotate the array (obfuscation)
    ROTATION = 5
    store = create_string_store(original_strings, ROTATION)

    print("=== Rotated string store ===")
    for i, s in enumerate(store):
        print(f"  [{i}] = '{s}'")

    # Step 2: Access strings through decoder (as Akamai does)
    OFFSET = 0x1a4  # Hex offset used in decoder calls

    print("\n=== Decoded strings ===")
    # In Akamai's code, you'd see calls like: _0x1234(0x1a4) -> "languages"
    # The index encodes the offset so the actual access is: index - OFFSET
    for i in range(len(store)):
        decoded = decode_string(store, i + OFFSET, OFFSET)
        print(f"  decoder(0x{i + OFFSET:x}) = '{decoded}'")

    print("\n=== What this means ===")
    print("Instead of writing 'navigator.userAgent' directly,")
    print("Akamai's script writes something like:")
    print("  window[_0xabc(0x1a5)][_0xabc(0x1a6)]")
    print("Which decodes to: window['navigator']['userAgent']")
    print("\nThis makes static analysis much harder, but")
    print("the decoded strings can be recovered at runtime.")
