#  LangChain Neo4j GraphDB Example
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)]()
[![Maintaner](https://img.shields.io/static/v1?label=Andriy%20Gulak&message=Maintainer&color=red)](mailto:andriy.gulak@extrawest.com)
[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://github.com/extrawest/neo4j_graph_db_example/issues)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## PROJECT INFO
- **Langchain Python AI Graph RAG**
- Neo4j for GraphDB
- Cypher for queries

## Features
- Neo4j GraphDB RAG is an AI-based content interpretation and search capability. Using LLMs, it parses data to create a knowledge graph and answer user questions about a user-provided private dataset

## Demo
1. Query:
**Which actors have acted in the most movies?**

Output:
![neo4j_graphdb](https://github.com/user-attachments/assets/3392bfad-1da0-4e46-83c6-5d24f21fcfdd)

2. Query:
```cypher
MATCH (n:Genre) RETURN n LIMIT 25;
```

Output:
![visualisation (1)](https://github.com/user-attachments/assets/359e1360-490c-4613-a539-8c74135007ed)

3. Query:
```bash
MATCH p=()-[:IN_GENRE]->() RETURN p LIMIT 25;
```
Output:
![visualisation (2)](https://github.com/user-attachments/assets/13a3f5f5-66fb-4769-bb73-5f270a0d1e04)

## Installing:
**1. Clone this repo to your folder:**

```
git clone THIS REPO
```

**2. Create a virtual environment**

**3. Install the dependencies**

```
pip install -r requirements.txt
``` 

[Extrawest.com](https://www.extrawest.com), 2024


