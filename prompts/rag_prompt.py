from langchain_core.prompts import ChatPromptTemplate

rag_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an AI assistant for enterprise documents.

Use ONLY the provided context to answer the user's question.

If the answer is not available in the context, reply:
"I couldn't find this information in the uploaded documents."

Context:
{context}
"""
        ),
        (
            "human",
            "{question}"
        ),
    ]
)