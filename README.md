# Code Assistant

Convert Python → high-performance C++ **or** add PEP-257 docstrings/comments to Python, with a clean streaming UI built in **Gradio** and the **OpenAI** API.

> ⚠️ Generated code is unaudited. Don’t run untrusted code.

---

## Features

* **Two modes**

  * **Convertor**: re-implements Python in optimized **C++17+** (code block only)
  * **Documentation**: injects docstrings + concise comments into Python without changing behavior
* **Streaming UX**: tokens appear live in the app while the model writes
* **Reliable parsing**: robust fenced-code extraction (`cpp / `python / plain)
* **Artifacts**: saves outputs to `optimized.cpp` or `Documented.py`
* **(Optional) Native run**: one-click **Compile & Run (C++)** for local benchmarking

---

## Quick start

### 1) Setup

```bash
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # then put your key inside
```

### 2) Environment

Edit `.env`:

```env
OPENAI_API_KEY=sk-your-key
```

### 3) Run the app

```bash
python app.py
```

Open the printed local URL (e.g., `http://127.0.0.1:7860`).

---

## How to use

1. Paste **Python** code in the text box.
2. Choose **Mode**:

   * **Convertor** → “Python → C++”
   * **Documentation** → “Docstrings + comments”
3. Click **Run**. Output streams into the right panel.
4. When generation ends, the app writes one of:

   * `optimized.cpp` *(Convertor)*
   * `Documented.py` *(Documentation)*
5. (Optional) Click **Compile & Run (C++)** to build & run `optimized.cpp` locally.

> The compile button uses `clang++` on macOS and `g++` on Linux:
>
> ```
> -O3 -std=c++17 -march=native -o optimized optimized.cpp
> ```

---

## Under the hood

* **Prompts** (`prompts.py`)

  * `system_message_for("Convertor")` asks for **pure C++ code** in a \`\`\`cpp fenced block, with correct headers and attention to integer width/overflow.
  * `system_message_for("Documentation")` asks for **pure Python code** in a \`\`\`python fenced block, adding PEP-257 docstrings + minimal inline comments, **no behavior changes**.

* **Streaming** (`app.py`)

  * Uses `client.chat.completions.create(..., stream=True, temperature=0)` for deterministic generation.
  * Buffers fragments and streams to the UI; writes the final cleaned code to disk.

* **Fence parsing** (`utils.py`)

  * `extract_code_block()` finds the **first matching fenced block**, preferring a requested language when present.
  * `write_output()` writes the cleaned code to `optimized.cpp` or `Documented.py`.
  * `compile_and_run_cpp()` compiles + runs locally and returns stdout.

---

## Examples

### Convertor (Python → C++)

Input (Python):

```python
print("hello")
```

Output (C++, saved to `optimized.cpp`):

```cpp
#include <iostream>
int main(){ std::cout << "hello\n"; }
```

### Documentation (Python → commented Python)

Input:

```python
def add(a,b):
    return a+b
```

Output (saved to `Documented.py`):

```python
def add(a: int, b: int) -> int:
    """Return the sum of two integers.

    Args:
        a (int): First addend.
        b (int): Second addend.
    Returns:
        int: a + b.
    """
    return a + b
```

---

## Troubleshooting

* **Blank output or backticks in files**
  The extractor in `utils.py` removes code fences. If a model replies without fences, the raw text is saved as-is.

* **“No optimized.cpp found.” on compile**
  Run **Convertor** first, then click **Compile & Run**.

* **Compiler not found**
  Install a C++ compiler:

  * macOS: `xcode-select --install` (gives `clang++`)
  * Linux: `sudo apt install g++`

* **Safety**
  Don’t compile/run code you don’t trust. Review the generated C++ first. Or run on a different compiler. 

---

## Cost & limits

The app uses `gpt-4o-mini` by default (low cost). You can change the model via `OPENAI_MODEL` in `app.py`. API usage incurs costs—monitor your key. 
You can also substitute with any open source model using ollama if needed, however, accuracy and performance of the application will differ. 

---

## License

MIT (suggested). Add a `LICENSE` file if you plan to open-source.

---

## Acknowledgments

Built with **Gradio** for the UI and **OpenAI** for generation.
