from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from pyzbar.pyzbar import decode
from PIL import Image
import pandas as pd
import os
from crews.hypothesis_crew.hypothesis_crew import HypothesisCrew
from crews.main_crew.main_crew import MainCrew

class ProductSupportState(BaseModel):
    machine_details: str = ""
    initial_hypothesis: list = []
    user_prompt: str = ""
    final_result: str = ""
    conversation_history: list = []


class ProductSupportFlow(Flow[ProductSupportState]):

    @start()
    def get_machine_details(self):
        print("getting machine details")
        qr_image = Image.open("user_inputs/scans/qr_scan.png")
        data = decode(qr_image)
        if data:
            machine_name = data[0].data.decode("utf-8")
        else: 
            raise("Invalid QR code")
        
        file_path = "../../data/bosch_washing_machines.csv"
        df = pd.read_csv(file_path)
        product_dict = df.set_index("Model").T.to_dict()
        self.state.machine_details = product_dict.get(machine_name, "Model not found")
        if self.state.machine_details == "Model not found":
            raise("Model not found")
        print(f"Machine details: {self.state.machine_details}")

    @listen(get_machine_details)
    def initial_hypothesis(self):
        print("preparing initial hypothesis")
        hypothesis_crew = HypothesisCrew()
        inputs = {
            "machine_details": self.state.machine_details
        }
        initial_hypothesis = hypothesis_crew.crew().kickoff(inputs)
        cleaned_hypothesis = initial_hypothesis.raw.replace("```python", "").replace("```", "").strip()
        self.state.initial_hypothesis = eval(cleaned_hypothesis)
        print(f"Initial hypothesis: {self.state.initial_hypothesis}")

    @listen(initial_hypothesis)
    def get_user_input(self):
        print("getting user input")
        for i, hypothesis in enumerate(self.state.initial_hypothesis):
            print(f"{i+1}. {hypothesis}")

        print(f"{len(self.state.initial_hypothesis) + 1} - Own query")

        input_choice_hypo = int(input("Choose query: "))

        if input_choice_hypo == len(self.state.initial_hypothesis) + 1:
            own_query = input("Enter your own query: ")
            self.state.user_prompt = own_query
        elif input_choice_hypo == 7:
            self.state.user_prompt = "how to connect the hose?"
        else:
            self.state.user_prompt = self.state.initial_hypothesis[input_choice_hypo - 1].strip()
        

    @listen(get_user_input)
    def call_main_crew(self):
        print("calling main crew")
        main_crew = MainCrew()
        i = 0
        while True:
            if i != 0:
                query = input("Enter your own query (or) 0 to exit: ")
                self.state.user_prompt = query
                if query == "0":
                    break
            inputs = {
                "user_prompt": self.state.user_prompt,
                "machine_details": self.state.machine_details,
                "conversation_history": self.state.conversation_history
            }
            result = main_crew.crew().kickoff(inputs)
            self.state.final_result = result.raw
            print(f"Final result: {self.state.final_result}")

            self.state.conversation_history.append("User: "+self.state.user_prompt+"\nAI: "+self.state.final_result)
            i = 1



    
def kickoff():
    support_flow = ProductSupportFlow()
    support_flow.kickoff()


if __name__ == "__main__":
    kickoff()
