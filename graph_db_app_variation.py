import os

from dotenv import load_dotenv
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)

moview_query = """
LOAD CSV WITH HEADERS FROM
'https://raw.githubusercontent.com/tomasonjo/blog-datasets/main/movies/movies_small.csv' as row

MERGE(m:Movie{id:row.movieId})
SET m.released = date(row.released),
    m.title = row.title,
    m.imdbRating = toFloat(row.imdbRating)
FOREACH (director in split(row.director, '|') | 
    MERGE (p:Person {name:trim(director)})
    MERGE (p)-[:DIRECTED]->(m))
FOREACH (actor in split(row.actors, '|') | 
    MERGE (p:Person {name:trim(actor)})
    MERGE (p)-[:ACTED_IN]->(m))
FOREACH (genre in split(row.genres, '|') | 
    MERGE (g:Genre {name:trim(genre)})
    MERGE (m)-[:IN_GENRE]->(g))
"""
graph.query(moview_query)
graph.refresh_schema()

llm = ChatGroq(groq_api_key=groq_api_key, model_name="Gemma2-9b-It")

examples = [
    {
        "question": "Find actors who have acted in multiple movies",
        "query": "MATCH (p:Person)-[:ACTED_IN]->(m:Movie) WITH p, COUNT(DISTINCT m) AS movie_count WHERE movie_count > 1 RETURN p.name, movie_count ORDER BY movie_count DESC",
    },
    {
        "question": "What are the top 5 highest-rated movies?",
        "query": "MATCH (m:Movie) RETURN m.title, m.imdbRating ORDER BY m.imdbRating DESC LIMIT 5"
    }
]

formatted_examples = "\n\n".join([
    f"Example {i + 1}:\nQuestion: {ex['question']}\nCypher Query: {ex['query']}"
    for i, ex in enumerate(examples)
])

prompt = PromptTemplate(
    template="You are a Neo4j expert. Given an input question, create a syntactically very accurate Cypher query based on the following examples:\n\n"
             f"{formatted_examples}\n\n"
             "Schema: {schema}\n\n"
             "User input: {question}",
    input_variables=["schema", "question"]
)

chain = GraphCypherQAChain.from_llm(
    graph=graph,
    llm=llm,
    cypher_prompt=prompt,
    verbose=True,
    return_intermediate_steps=True,
    allow_dangerous_requests=True
)


try:
    result = chain.invoke({
        "schema": graph.schema,
        "question": "Which actors have acted in the most movies?",
        "query": ""
    })
    print("Result:", result)

except Exception as e:
    print(f"Error executing Cypher query: {e}")