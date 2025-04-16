from crewai_tools import PDFSearchTool
from crewai_tools import WebsiteSearchTool
import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def other_tools():
    pdf_tool = PDFSearchTool(
        config=dict(
            llm=dict(
                provider="google",
                config=dict(
                    model="models/gemini-2.0-flash",
                    temperature=0.5,
                    top_p=3,
                ),
            ),
            embedder=dict(
                provider="google",
                config=dict(
                    model="models/embedding-001",
                    task_type="retrieval_document",
                ),
            ),
        ),
        pdf="product_support/data/manual.pdf",
    )

    web_search_tool = WebsiteSearchTool(
        config=dict(
            llm=dict(
                provider="google",
                config=dict(
                    model="models/gemini-2.0-flash",
                    temperature=0.5,
                    top_p=3,
                ),
            ),
            embedder=dict(
                provider="google",
                config=dict(
                    model="models/embedding-001",
                    task_type="retrieval_document",
                    title="Web Embeddings",
                ),
            ),
        )
    )

    return pdf_tool, web_search_tool
