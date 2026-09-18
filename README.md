# KubeGraph RAG

> A hybrid Retrieval-Augmented Generation (RAG) system for Kubernetes documentation, combining **vector search** with a **knowledge graph**.

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)
[![Neo4j](https://img.shields.io/badge/Neo4j-Graph%20Database-008CC1?logo=neo4j)](https://neo4j.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql)](https://www.postgresql.org/)
[![pgvector](https://img.shields.io/badge/pgvector-Vector%20Search-336791)](https://github.com/pgvector/pgvector)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Claude](https://img.shields.io/badge/Claude-API-D97757)](https://www.anthropic.com/api)
[![Sentence Transformers](https://img.shields.io/badge/Sentence--Transformers-Embeddings-yellow)](https://www.sbert.net/)
[![Docker](https://img.shields.io/badge/Docker-Containers-2496ED?logo=docker)](https://www.docker.com/)
[![LangChain](https://img.shields.io/badge/LangChain-LLM%20Framework-1C3C3C?logo=langchain)](https://www.langchain.com/)

---

## 🚧 Project Status

**Current progress: Step 13 — Vector Search implemented**

The project is being built incrementally. At the current stage, Kubernetes documentation is:

* collected and stored as Markdown
* split into chunks
* converted into vector embeddings
* stored in PostgreSQL with `pgvector`
* searchable using cosine similarity

Knowledge graph extraction, graph retrieval, routing, hybrid retrieval, evaluation, and the FastAPI interface will be added in later stages.

---

## 🎯 Project Goal

The goal of **KubeGraph RAG** is to build a RAG system that can answer questions about Kubernetes using two complementary retrieval approaches:

```text
                    User Question
                         │
                         ▼
                  Query Processing
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
        Vector Retrieval       Graph Retrieval
          (pgvector)              (Neo4j)
              │                     │
              └──────────┬──────────┘
                         ▼
                   Hybrid Context
                         │
                         ▼
                  Claude Response
```

Vector search is useful for finding relevant documentation passages, while the knowledge graph will later represent explicit relationships between Kubernetes concepts.

---

## 📚 Current Corpus

The project currently uses Kubernetes documentation as its knowledge source.

Example document categories include:

* Cluster Architecture
* Nodes
* Pods
* Workloads
* Deployments
* ReplicaSets
* Services
* Networking
* Storage
* Scheduling
* Kubernetes Components

The documentation is converted into chunks before indexing.

---

## 🔍 Vector Search

The current implementation uses:

**Sentence Transformers → PostgreSQL → pgvector**

For example:

```text
Query:
"How does Kubernetes run containers on a node?"

                    ↓

              Query embedding

                    ↓

              pgvector search

                    ↓

             Top-K chunks

                    ↓

nodes:chunk_0
pods:chunk_0
pods:chunk_1
architecture:chunk_1
architecture:chunk_0
```

The vector search uses cosine distance through the pgvector `<=>` operator.

---

## 🧰 Technologies & Packages

### Python

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)

The main programming language used to build the ingestion, embedding, retrieval, graph, API, and evaluation components.

---

### Sentence Transformers

![Sentence Transformers](https://img.shields.io/badge/Sentence--Transformers-Embeddings-yellow)

Used to convert Kubernetes documentation chunks and user queries into numerical vector embeddings.

Current model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

---

### PostgreSQL

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql)

Relational database used to store the original document chunks, metadata, and vector embeddings.

---

### pgvector

![pgvector](https://img.shields.io/badge/pgvector-Vector%20Search-336791)

PostgreSQL extension that enables vector similarity search.

It is currently used to retrieve the most semantically similar Kubernetes documentation chunks.

The project uses cosine distance:

```sql
ORDER BY embedding <=> query_embedding
```

---

### Neo4j

![Neo4j](https://img.shields.io/badge/Neo4j-Graph%20Database-008CC1?logo=neo4j)

Graph database that will be used to represent Kubernetes entities and relationships.

Planned examples:

```text
Deployment
    │
    └── CREATES
          ↓
      ReplicaSet
          │
          └── CREATES
                ↓
              Pod
                │
                └── RUNS_ON
                      ↓
                     Node
```

Neo4j will become the graph retrieval layer in the hybrid RAG pipeline.

---

### Claude API

![Claude](https://img.shields.io/badge/Claude-API-D97757)

Anthropic's Claude API will be used for LLM-based tasks such as:

* entity extraction
* relationship extraction
* query understanding
* answer generation
* grounded response generation

Structured outputs will be validated before being inserted into the knowledge graph.

---

### FastAPI

![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi)

FastAPI will provide the final HTTP API for querying the RAG system.

Planned endpoint:

```text
POST /query
```

Example:

```json
{
  "question": "How does a Deployment eventually get a Pod running on a Node?"
}
```

---

### LangChain

![LangChain](https://img.shields.io/badge/LangChain-LLM%20Framework-1C3C3C?logo=langchain)

LangChain is included as an optional orchestration layer for LLM and retrieval components.

The core retrieval logic remains explicitly implemented so that the graph/vector pipeline is easy to understand and benchmark.

---

### Pydantic

Used for structured data validation.

For example, extracted entities and relationships will follow predefined schemas instead of accepting arbitrary LLM output.

---

### Docker

![Docker](https://img.shields.io/badge/Docker-Containers-2496ED?logo=docker)

Docker Compose is used to run the local infrastructure:

```text
Neo4j
PostgreSQL + pgvector
```

This makes the project reproducible without requiring a Kubernetes cluster.

---

## 📁 Project Structure

```text
kubegraph-rag/
│
├── app/
│   ├── ingestion/
│   │   └── chunker.py
│   │
│   ├── extraction/
│   │
│   ├── graph/
│   │
│   ├── vector/
│   │   ├── embeddings.py
│   │   └── store.py
│   │
│   ├── retrieval/
│   ├── routing/
│   ├── generation/
│   └── main.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── scripts/
│   ├── index_vectors.py
│   └── test_vector_search.py
│
├── tests/
│
├── docker-compose.yml
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 🔄 Current Data Flow

```text
Kubernetes Documentation
          │
          ▼
       Chunking
          │
          ▼
   Document Chunks
          │
          ▼
 Sentence Transformer
          │
          ▼
    Vector Embeddings
          │
          ▼
 PostgreSQL + pgvector
          │
          ▼
   Similarity Search
          │
          ▼
       Top-K Chunks
```

Each chunk has a unique `chunk_id`, which will later act as the bridge between the vector database and knowledge graph.

Example:

```Score: 0.7804392111039645
Chunk: nodes:chunk_0
1. [Kubernetes Documentation](/docs/) 2. [Concepts](/docs/concepts/) 3. [Cluster Architecture](/docs/concepts/architecture/) 4. Nodes Nodes ===== Kubernetes runs your [workload](/docs/concepts/workloads/ "A workload is an application running on Kubernetes.") by placing [containers](/docs/concepts/co
--------------------------------------------------------------------------------
Score: 0.7217033671317491
Chunk: pods:chunk_0
1. [Kubernetes Documentation](/docs/) 2. [Concepts](/docs/concepts/) 3. [Workloads](/docs/concepts/workloads/) 4. Pods Pods ==== *Pods* are the smallest deployable units of computing that you can create and manage in Kubernetes. A *Pod* (as in a pod of whales or pea pod) is a group of one or more [c
--------------------------------------------------------------------------------
Score: 0.7048214009723555
Chunk: pods:chunk_1
with no assigned node, and selects a node for them to run on.") picks a node for the Pod to run on. In any cluster where there is more than one operating system for running nodes, you should set the [kubernetes.io/os](/docs/reference/labels-annotations-taints/#kubernetes-io-os) label correctly on ea
--------------------------------------------------------------------------------
Score: 0.6901060527499895
Chunk: architecture:chunk_1
[kubelet](/docs/reference/command-line-tools-reference/kubelet/) takes a set of PodSpecs that are provided through various mechanisms and ensures that the containers described in those PodSpecs are running and healthy. The kubelet doesn't manage containers which were not created by Kubernetes. ### k
--------------------------------------------------------------------------------
Score: 0.6752191580766718
Chunk: architecture:chunk_0
1. [Kubernetes Documentation](/docs/) 2. [Concepts](/docs/concepts/) 3. Cluster Architecture Cluster Architecture ==================== The architectural concepts behind Kubernetes. A Kubernetes cluster consists of a control plane plus a set of worker machines, called nodes, that run containerized ap
--------------------------------------------------------------------------------
```

---

## ✅ Completed

* [x] Project structure
* [x] Docker environment
* [x] PostgreSQL setup
* [x] pgvector setup
* [x] Kubernetes documentation corpus
* [x] Document chunking
* [x] Stable chunk IDs
* [x] Sentence Transformer embeddings
* [x] Vector storage
* [x] pgvector similarity search
* [x] Top-K vector retrieval

### Example Retrieval

Query:

```text
How does Kubernetes run containers on a node?
```

Example retrieved chunks:

```text
nodes:chunk_0
pods:chunk_0
pods:chunk_1
architecture:chunk_1
architecture:chunk_0
```

---

## 🚀 Planned Next Steps

* [ ] Define graph ontology
* [ ] Extract Kubernetes entities and relationships with Claude
* [ ] Validate structured extraction
* [ ] Entity resolution
* [ ] Store entities and relationships in Neo4j
* [ ] Implement parameterized Cypher retrieval templates
* [ ] Build query router
* [ ] Implement hybrid graph + vector retrieval
* [ ] Generate grounded answers with citations
* [ ] Validate citations against retrieved chunks
* [ ] Build FastAPI endpoint
* [ ] Create vector-only baseline
* [ ] Benchmark vector RAG vs hybrid RAG
* [ ] Measure accuracy, latency, and cost

---

## 🧪 Example Vector Search

Run:

```bash
python -m scripts.test_vector_search
```

Example:

```text
Score: 0.7804
Chunk: nodes:chunk_0

Score: 0.7217
Chunk: pods:chunk_0

Score: 0.7048
Chunk: pods:chunk_1

Score: 0.6901
Chunk: architecture:chunk_1

Score: 0.6752
Chunk: architecture:chunk_0
```

Scores represent vector similarity and are not accuracy percentages.

---

## 🗺️ Long-Term Architecture

The final system will combine semantic retrieval with structured graph traversal:

```text
                         User Question
                               │
                               ▼
                        Query Router
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
                 ▼             ▼             ▼
              VECTOR         GRAPH          BOTH
                 │             │             │
                 ▼             ▼             ▼
             pgvector       Neo4j       Both sources
                 │             │             │
                 └─────────────┼─────────────┘
                               ▼
                        Evidence Merging
                               │
                               ▼
                       Claude Generation
                               │
                               ▼
                    Grounded Answer + Citations
```

---

## 📌 Why This Project?

Traditional vector RAG is effective at finding semantically similar passages, but questions involving relationships and multiple hops can benefit from explicit graph structure.

For example:

```text
How does a Deployment eventually get a Pod running on a Node?
```

The knowledge graph can represent:

```text
Deployment
    ↓
ReplicaSet
    ↓
Pod
    ↓
Node
```

while the original documentation chunks provide textual evidence for each relationship.

The project therefore explores how **vector retrieval and knowledge-graph retrieval can complement each other in an enterprise-style RAG system**.

---

## 📄 License

This project is intended as a portfolio/learning project. Check the licensing terms of any external documentation or datasets used when redistributing them.
