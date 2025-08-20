# utils.py
import os, re, subprocess
from typing import Optional

FENCE_PATTERN = r"```(?:([\w+#+-]+))?\s*([\s\S]*?)```"

def extract_code_block(text: str, preferred_lang: Optional[str] = None) -> str:
    """Return the best fenced code block, or raw text if none."""
    blocks = re.findall(FENCE_PATTERN, text, flags=re.IGNORECASE)
    if not blocks:
        return text.strip()
    if preferred_lang:
        for lang, code in blocks:
            if (lang or "").lower() == preferred_lang.lower():
                return code.strip()
    # fallback to first code block
    return blocks[0][1].strip()

def write_output(use_case: str, output: str) -> str:
    if use_case == "Convertor":
        code = extract_code_block(output, preferred_lang="cpp")
        path = "optimized.cpp"
    elif use_case == "Documentation":
        code = extract_code_block(output, preferred_lang="python")
        path = "Documented.py"
    else:
        raise ValueError(f"Unknown use_case: {use_case}")
    with open(path, "w") as f:
        f.write(code)
    return path

def compile_and_run_cpp(source: str = "optimized.cpp") -> str:
    if not os.path.exists(source):
        return "No optimized.cpp found."
    compiler = "clang++" if os.uname().sysname == "Darwin" else "g++"
    cmd = [compiler, "-O3", "-std=c++17", "-march=native", "-o", "optimized", source]
    try:
        subprocess.check_call(cmd)
        out = subprocess.check_output(["./optimized"], text=True)
        return out
    except subprocess.CalledProcessError as e:
        return f"Compile/Run error:\n{e}"
