# LlamaIndexProj

This project is a Python-based application that allows users to interact with the content of a GitHub repository using natural language queries. It utilizes the LlamaIndex library for document indexing and question-answering, and the Cohere and Groq APIs for language processing and model serving.

## Features

- Interactive question-answering system for GitHub repositories
- Utilizes LlamaIndex for document indexing and querying
- Integrates Cohere and Groq for language processing and model serving
- Supports asynchronous I/O operations for efficient processing

## Prerequisites

- Python 3.7 or higher
- `pip` package manager
- A GitHub repository with content to interact with
- Cohere and Groq API keys

## Setup

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/llamaindexProj.git
```

2. Create a `.env` file in the project root directory and add your Cohere and Groq API keys:

```ini
COHERE_API_KEY=<your-cohere-api-key>
GROQ_API_KEY=<your-groq-api-key>
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python main.py
```

## Usage

1. Enter the GitHub URL of the repository you want to interact with.
2. Enter your question.
3. The application will return the answer based on the content of the repository.

## Note

Make sure the repository you want to interact with is not empty, as the application requires documents to query.

## Troubleshooting

If you encounter any issues, make sure you have the correct API keys and the repository URL is valid.

## License

This project is licensed under the MIT License.
