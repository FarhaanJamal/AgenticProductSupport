from pyzbar.pyzbar import decode
from PIL import Image
import pandas as pd
import os
from crews.hypothesis_crew.hypothesis_crew import HypothesisCrew
from crews.main_crew.main_crew import MainCrew


def get_machine_details():
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
    machine_details = product_dict.get(machine_name, "Model not found")
    if machine_details == "Model not found":
        raise("Model not found")
    print(f"Machine details: {machine_details}")
    return machine_details


def get_initial_hypothesis(machine_details):
    print("preparing initial hypothesis")
    hypothesis_crew = HypothesisCrew()
    inputs = {
        "machine_details": machine_details
    }
    initial_hypothesis = hypothesis_crew.crew().kickoff(inputs)
    cleaned_hypothesis = initial_hypothesis.raw.replace("```python", "").replace("```", "").strip()
    initial_hypothesis = eval(cleaned_hypothesis)
    print(f"Initial hypothesis: {initial_hypothesis}")
    return initial_hypothesis

def get_user_input(initial_hypothesis):
    print("getting user input")
    for i, hypothesis in enumerate(initial_hypothesis):
        print(f"{i+1}. {hypothesis}")

    print(f"{len(initial_hypothesis) + 1} - Own query")

    input_choice_hypo = int(input("Choose query: "))

    if input_choice_hypo == len(initial_hypothesis) + 1:
        own_query = input("Enter your own query: ")
        user_prompt = own_query
    elif input_choice_hypo == 7:
        user_prompt = "how to connect the hose?"
    else:
        user_prompt = initial_hypothesis[input_choice_hypo - 1].strip()
    return user_prompt
    

def call_main_crew(user_prompt, machine_details, conversation_history):
    print("calling main crew")
    main_crew = MainCrew()
    i = 0
    while True:
        if i != 0:
            query = input("Enter your own query (or) 0 to exit: ")
            user_prompt = query
            if query == "0":
                break
        inputs = {
            "user_prompt": user_prompt,
            "machine_details": machine_details,
            "conversation_history": conversation_history
        }
        result = main_crew.crew().kickoff(inputs)
        final_result = result.raw
        print(f"Final result: {final_result}")

        conversation_history.append("User: "+user_prompt+"\nAI: "+final_result)
        i = 1
    return conversation_history, final_result


if __name__ == "__main__":
    machine_details = get_machine_details()
    initial_hypothesis = get_initial_hypothesis(machine_details)
    user_prompt = get_user_input(initial_hypothesis)
    
    conversation_history = []
    conversation_history, final_result = call_main_crew(user_prompt, machine_details, conversation_history)
