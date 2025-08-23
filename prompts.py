def system_message_for(use_case: str) -> str:
    if use_case == "Convertor":
        return (
            "You are an assistant that reimplements Python code in high-performance C++ "
            "for Apple Silicon (M1/M2) or Linux. Respond with code only in a ```cpp block. "
            "Include necessary headers; avoid prose. Ensure identical output and avoid overflow."
        )
    if use_case == "Documentation":
        return (
            "You are a Python coding assistant. Add PEP 257 docstrings and concise inline comments "
            "to improve readability without changing behavior or identifiers. "
            "Respond with code only in a ```python block."
        )
    return "Unknown use case."

def user_prompt_for(use_case: str, python_src: str) -> str:
    if use_case == "Convertor":
        return (
            "Rewrite the following Python code in optimal C++17+, identical output. "
            "Emit only a ```cpp fenced block. Avoid extra explanations.\n\n" + python_src
        )
    if use_case == "Documentation":
        return (
            "Insert PEP 257 docstrings and minimal inline comments without changing logic or names. "
            "Emit only a ```python fenced block.\n\n" + python_src
        )
    return "Invalid use case."
