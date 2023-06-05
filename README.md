# 🚀 Notebook Copilot: From Thoughts to Well-Crafted Notebook at Record-Speed. 

Welcome to Notebook Copilot, your next-generation tool for Jupyter Notebooks. Inspired by GitHub Copilot, Notebook
Copilot is designed to help engineers and data scientists in developing professional, high-quality notebooks. It's like
having your personal AI-powered assistant that helps you navigate through the Jupyter universe, seamlessly
generating code and markdown cells based on your inputs.

Imagine not having to start with a blank notebook every time. Sounds dreamy, right?

<h2 align="center"> v1 Demo </h2>


https://github.com/talperetz/notebook-copilot/assets/11588598/02e2b030-adb3-42f2-bd6d-4a8451e3831f


## Features

- 🚀 GPT Based Generation: Notebook Copilot employs advanced GPT instances for precise and efficient code generation.
- 💻 Integrated with Any Notebook Environments: Seamless access within Jupyter Notebook and other popular platforms, boosting your productivity.
- 🧩 Automatic Context Retrieval: Understands the full context of your notebook, ensuring consistent and relevant code generation.
- 🔑 Bring Your Own OpenAI Key: Flexibility to use your own OpenAI key for personalized code generation and optimal results.
- 🆓 Free and Open Source: Everyone can benefit from Notebook Copilot. It's our contribution to the coding community, aiming to make coding accessible, efficient, and fun.


## Quickstart
0. Get an OpenAI [API Key](https://platform.openai.com/account/api-keys)
1. Install Notebook Copilot directly from PyPI:

```bash
pip install notebook_copilot
```

2. Load the Notebook Copilot extension in your Jupyter notebook:

```python
%load_ext notebook_copilot

# Optional: If you don't have OPENAI_API_KEY set in your environment, you can set it here
from getpass import getpass
import os
os.environ["OPENAI_API_KEY"] = getpass("Enter your OpenAI Key: ")

%copilot_init -n /Users/tp/dev/workspace/notebook_copilot/copilot_example_notebook.ipynb # improves copilot performance
```

3. Start using Notebook Copilot Magic Functions in your notebook ↓


## ✨ Magic Functions

🪄 Enter Assistant Mode and let Copilot continuously generate professional code and markdown cells for you.
```python
%copilot
```

✍️ Leverage AI to create the next cell from your comments. It's like having a conversation with your notebook.

```python
%%generate 
# Plot the confusion matrix using for the model
```

📘 Automatically generate markdown cells to explain the code in the current cell. Your code is now not only functional but also well-documented.
```python
%%explain
# some code to explain…
```

## Roadmap

- [x] **Copilot Magic Function**: Continues the notebook for you, generating professional code and markdown cells, making
  blank notebooks a thing of the past.
- [x] **Generate Magic Function**: Turn Your Comments into Code
- [x] **Explain Magic Function**: Generate Markdown Cells that Explain Your Code
- [ ] Support parallel cell generation
- [ ] Update underlying strategy and prompts
- [ ] Support more llm providers
  - [ ] Starcoder
  - [ ] Anthropic
- [ ] AI-Powered Code completion inside cells
    

## Contributing
We appreciate all contributions. If you're planning to contribute back bug-fixes, please do so without any further discussion. If you plan to contribute new features, utility functions, or extensions to the core, please first open an issue and discuss the feature with us.

## License
Notebook Copilot is MIT licensed, as found in the LICENSE file.
