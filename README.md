# Technical Project Report: Agentic Product Support

## Project Overview
The **Agentic Product Support** project is a multi-agent AI system designed to provide intelligent product support for Bosch washing machines. It leverages the **crewAI** framework to enable seamless collaboration between agents, utilizing advanced tools like QR code scanning, PDF parsing, and web search to retrieve machine details and provide accurate, stepwise resolutions to user queries. The system is powered by **Google Gemini LLMs** for generating FAQs, image descriptions, and cross-referencing information from manuals and the web.

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
  - The decoded machine model is matched against a CSV file (`bosch_washing_machines.csv`) containing machine details.
- **Output**: Machine details (e.g., model, type, load capacity, energy rating, etc.).

**Code Reference**:
```python
qr_image = Image.open("user_inputs/scans/qr_scan.png")
data = decode(qr_image)
machine_name = data[0].data.decode("utf-8")
df = pd.read_csv("../../data/bosch_washing_machines.csv")
product_dict = df.set_index("Model").T.to_dict()
self.state.machine_details = product_dict.get(machine_name, "Model not found")
```

---

### 2. **Initial Hypothesis Generation**
- **Input**: Machine details.
- **Process**:
  - The `HypothesisCrew` agent generates FAQs based on the machine's features.
  - FAQs are returned as a Python list.
- **Output**: A list of 5 FAQs.

**Code Reference**:
```python
hypothesis_crew = HypothesisCrew()
inputs = {"machine_details": self.state.machine_details}
initial_hypothesis = hypothesis_crew.crew().kickoff(inputs)
self.state.initial_hypothesis = eval(initial_hypothesis.raw.replace("```python", "").replace("```", "").strip())
```

---

### 3. **User Query Handling**
- **Input**: User-selected FAQ or custom query.
- **Process**:
  - The user selects a query from the generated FAQs or inputs their own.
  - The query is passed to the `MainCrew` for processing.
- **Output**: User query stored in the system state.

**Code Reference**:
```python
input_choice_hypo = int(input("Choose query: "))
if input_choice_hypo == len(self.state.initial_hypothesis) + 1:
    self.state.user_prompt = input("Enter your own query: ")
else:
    self.state.user_prompt = self.state.initial_hypothesis[input_choice_hypo - 1].strip()
```

---

### 4. **Main Crew Execution**
- **Input**: User query, machine details, and conversation history.
- **Process**:
  - The `MainCrew` agent uses tools like PDF parsing and web search to retrieve relevant information.
  - The response is generated using the Google Gemini LLM.
- **Output**: Final response to the user query.

**Code Reference**:
```python
inputs = {
    "user_prompt": self.state.user_prompt,
    "machine_details": self.state.machine_details,
    "conversation_history": self.state.conversation_history
}
result = main_crew.crew().kickoff(inputs)
self.state.final_result = result.raw
```

---

## Agent and Crew Details

### 1. **HypothesisCrew**
- **Role**: Generate FAQs based on machine details.
- **Task**: `generate_faqs`
- **Configuration**:
  - **Agent**: `faq_generator`
  - **Task YAML**:
    ```yaml
    generate_faqs:
      description: >
        Generate 5 relevant FAQs for a washing machine.
      expected_output: >
        A Python list of 5 string-based FAQs.
    ```

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

**Code Reference**:
```python
pdf_tool = PDFSearchTool(config={...}, pdf="product_support/data/manual.pdf")
web_search_tool = WebsiteSearchTool(config={...})
ImageDescriberTool()
```

---

## Tools and Utilities

### 1. **PDFSearchTool**
- Parses the washing machine manual to retrieve relevant information.
- **Configuration**:
  ```python
  config=dict(
      llm=dict(provider="google", config=dict(model="models/gemini-2.0-flash")),
      embedder=dict(provider="google", config=dict(model="models/embedding-001"))
  )
  ```

---

### 2. **ImageDescriberTool**
- Analyzes washing machine images and generates descriptive paragraphs.
- **Process**:
  - Loads images from the `/images` folder.
  - Uses the Google Gemini LLM to generate descriptions.
- **Output**: A paragraph describing each image.

**Code Reference**:
```python
image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
response = model.generate_content(contents=[image])
description += response.text.strip()
```

---

## Deployment Details

### 1. **Environment Setup**
- **Python Version**: >=3.10, <3.13
- **Dependencies**: Managed via pyproject.toml.
- **Environment Variables**: API keys stored in `.env`.

### 2. **Execution**
- **Command**: `crewai run`
- **Flow**: Defined in `ProductSupportFlow`.

---

## Key Achievements
- **Multi-Agent Collaboration**: Seamless integration of agents for complex workflows.
- **High Accuracy**: Reliable responses using Google Gemini LLMs.
- **Scalability**: Modular architecture for easy customization and expansion.

---

## Future Enhancements
- Add support for additional product categories.
- Integrate voice-based user interactions.
- Enhance the database with more detailed product information.

---

This report provides a comprehensive overview of the technical aspects of the **Agentic Product Support** project, highlighting its architecture, workflows, and key components.
