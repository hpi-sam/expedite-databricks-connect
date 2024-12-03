# VectorStoreFactory Documentation

## Overview
The `VectorStoreFactory` class creates different types of `VectorStore` instances based on the configuration. It supports three types:

- **Docs**: Vector store based on document URLs.
- **Code**: Vector store from GitHub repositories.
- **API Reference**: Vector store based on API documentation.

## Method: `initialize`

```python
@staticmethod
def initialize(vectorstore_type: str, **kwargs) -> Chroma | None:
```

### Arguments:
- `vectorstore_type` (str): Type of vector store. Possible values:
  - `'docs'`: For a document-based vector store.
  - `'code'`: For a code-based vector store from GitHub repositories.
  - `'api_ref'`: For an API reference-based vector store.
- `kwargs`: Additional arguments for specific types:
  - For `'docs'`, provide a list of document URLs with the key `docs`.
  - For `'code'`, provide a list of GitHub repository and branch details with the key `repo_branch_list`.
  - For `'api_ref'`, no additional arguments are required.

### Returns:
- `Chroma | None`: The created `Chroma` vector store instance, or `None` if the `vectorstore_type` is unknown.

### Configuration
Configure the vector store type in `config.py`:
```python
# config.py

VECTORSTORE_TYPE = "docs"  # Options: 'docs', 'code', 'api_ref'

VECTORSTORE_SETTINGS = {
    "docs": {"docs": [...]},
    "code": {"repo_branch_list": [...]},
    "api_ref": {},
}```

