from typing import List
from langchain.docstore.document import Document
from langchain.chains.qa_with_sources import load_qa_with_sources_chain

from app.utils.constants import AnswerGenerationConstants


def get_answer(relevant_documents: List[Document], query: str) -> str:
    """generates ans with api call to LLM

    Args:
        relevant_documents: documents to be considered for answering question
        query: question asked by user

    Returns:
        response from api call
    """

    llm = AnswerGenerationConstants.ANSWER_LLM.value
    prompt = AnswerGenerationConstants.PROMPT.value

    search_chain = load_qa_with_sources_chain(
        llm=llm, chain_type="stuff", prompt=prompt
    )

    answer = search_chain(
        {"input_documents": relevant_documents, "question": query},
        return_only_outputs=True,
    )

    return answer


def get_sources(answer: str) -> List[str]:
    """
    extract the sources from answer generated by LLM

    Args:
        answer: answer generated by llm

    Returns:
        list of source id's
    """

    split_list = answer["output_text"].split("SOURCES:")
    answer = split_list[0]
    extracted_source_list = []

    # handle edge cases when model does not generate source or no answer but generates sources
    if len(split_list) > 1:
        extracted_text = split_list[1].strip()

        # Remove the surrounding square brackets and split by commas
        extracted_source_list = [
            str(item.strip()) for item in extracted_text[1:-1].split(",")
        ]

    return extracted_source_list


def get_documents_considered(
    token_safe_documents: str, sources: List[str]
) -> List[Document]:
    """
    gets the list of documents that were used for answering the llm answer from documents that were given to it.

    Args:
        token_safe_documents: documnts within the token limit that were used for answer generation
        sources: list of sources extracted from llm answer

    Returns:
        list of documents that llm considered for creating the final answer
    """

    return [
        document
        for document in token_safe_documents
        if document.metadata["source"] in sources
    ]


with open("data/stopwords.txt", "r") as file:
    stop_word = {line.strip() for line in file}


def filter_stop_word(query: str) -> str:
    """
    Filters out stop words from the given query.

    Args:
        query (str): The input query string.

    Returns:
        str: The filtered query string without stop words.

    Example:
        query = "top 10 keytruda abstracts"
        filter_stop_word(query)
        output: "keytruda"
    """

    query = query.strip()
    words = query.split()
    filtered_words = [word for word in words if word.lower() not in stop_word]
    filtered_query = " ".join(filtered_words).rstrip("?.")

    return filtered_query