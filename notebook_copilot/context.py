import pandas as pd
from IPython import get_ipython
from langchain import FAISS
from langchain.document_transformers import EmbeddingsRedundantFilter
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import EmbeddingsFilter, DocumentCompressorPipeline
from langchain.text_splitter import RecursiveCharacterTextSplitter


def get_ipython_run_history():
    shell = get_ipython()
    last_session_history = list(shell.history_manager.get_range_by_str('', output=True))[:-1]
    pretty_history = '\n'.join(
        ', '.join(map(str, t[2])) for t in last_session_history)
    return pretty_history


def get_pandas_dataframes():
    shell = get_ipython()
    dfs = []
    for name, value in shell.user_ns.items():
        if isinstance(value, pd.DataFrame):
            dfs.append(value)
    return dfs


def compress_notebook_context(notebook_documents):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["'markdown' cell:", "'code' cell:", "\n\n", "\n", " ", ""],
        chunk_size=1000,
        chunk_overlap=0,
        length_function=len,
    )
    texts = text_splitter.split_documents(notebook_documents)
    retriever = FAISS.from_documents(texts, OpenAIEmbeddings()).as_retriever()
    embeddings = OpenAIEmbeddings()
    redundant_filter = EmbeddingsRedundantFilter(embeddings=embeddings)
    relevant_filter = EmbeddingsFilter(embeddings=embeddings, similarity_threshold=0.56)
    pipeline_compressor = DocumentCompressorPipeline(
        transformers=[text_splitter, redundant_filter, relevant_filter]
    )
    compression_retriever = ContextualCompressionRetriever(base_compressor=pipeline_compressor,
                                                           base_retriever=retriever)

    return compression_retriever.get_relevant_documents(
        "What is the purpose of this notebook?"
    )
