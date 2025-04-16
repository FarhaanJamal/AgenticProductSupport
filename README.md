# Agentic Product Support

## Project Overview
The **Agentic Product Support** project is a multi-agent AI system designed to provide intelligent support for household products by orchestrating 2 crews, 3 tools, and 4 specialized agents in a coordinated flow using the crewAI framework. It leverages technologies like QR code scanning, PDF parsing, and web search to retrieve machine-specific details and deliver accurate, stepwise solutions to user queries, all powered by Google Gemini LLMs for generating FAQs, image descriptions, and cross-referencing information. The system includes a FastAPI backend for managing APIs, image uploads, and agent execution, along with a responsive React frontend built with Material UI for intuitive user interaction through QR uploads, chat interface, and FAQ selection.

---

## Video Demo
https://github.com/user-attachments/assets/31504266-379b-4b84-a38c-2d34ea7063cb

---

## System Architecture

### 1. **Core Components**
- **Agents**: Specialized AI entities with unique roles and goals.
- **Tasks**: Defined workflows that agents execute.
- **Crews**: Groups of agents collaborating to complete tasks.
- **Tools**: External utilities integrated into agents for specific functionalities.

### 2. **Key Technologies**
- **crewAI Framework**: Provides the flow-based architecture for multi-agent collaboration.
- **Google Gemini LLMs**: Used for natural language understanding and generation.
- **FastAPI**: Backend framework for API handling and coordination between frontend and agent layer.
- **React + Material UI**: Frontend stack for user interaction and display.
- **Python Libraries**:
  - `pydantic`: For state management.
  - `pyzbar`: For QR code decoding.
  - `Pandas`: For CSV data handling.
  - `Pillow`: For image processing.
- **Database**: SQLite for storing embeddings and other data.

---

## Functional Workflow

### 1. **Machine Details Retrieval**
- **Input**: QR code image of the washing machine.
- **Process**:
  - QR code is decoded using `pyzbar`.
  - The decoded machine model is matched against a CSV file (`_washing_machines.csv`) containing machine details.
- **Output**: Machine details (e.g., model, type, load capacity, energy rating, etc.).

---

### 2. **Initial Hypothesis Generation**
- **Input**: Machine details.
- **Process**:
  - The `HypothesisCrew` agent generates FAQs based on the machine's features.
  - FAQs are returned as a Python list.
- **Output**: A list of 5 FAQs.

---

### 3. **User Query Handling**
- **Input**: User-selected FAQ or custom query.
- **Process**:
  - The user selects a query from the generated FAQs or inputs their own.
  - The query is passed to the `MainCrew` for processing.
- **Output**: User query stored in the system state.

---

### 4. **Main Crew Execution**
- **Input**: User query, machine details, and conversation history.
- **Process**:
  - The `MainCrew` agent uses tools like PDF parsing and web search to retrieve relevant information.
  - The response is generated using the Google Gemini LLM.
- **Output**: Final response to the user query.

---

## Agent and Crew Details

### 1. **HypothesisCrew**
- **Role**: Generate FAQs based on machine details.
- **Task**: `generate_faqs`
- **Configuration**:
  - **Agent**: `faq_generator`
  - **Task**: `generate_faq`: Based on machine details generate faqs.
   
---

### 2. **MainCrew**
- **Role**: Provide detailed responses to user queries.
- **Tasks**:
  - `describe_image`: Analyze washing machine images.
  - `unified_reflection_task`: Retrieve and validate information from PDFs and the web.
- **Tools**:
  - **PDFSearchTool**: Parses the washing machine manual.
  - **WebsiteSearchTool**: Searches the web for additional information.
  - **ImageDescriberTool**: Analyzes washing machine images and generates descriptions.

---

## Tools and Utilities

### 1. **PDFSearchTool**
- Parses the washing machine manual to retrieve relevant information.

---

### 2. **ImageDescriberTool**
- Analyzes washing machine images and generates descriptive paragraphs.
- **Process**:
  - Loads images from the `/images` folder.
  - Uses the Google Gemini LLM to generate descriptions.
- **Output**: A paragraph describing each image.

---
