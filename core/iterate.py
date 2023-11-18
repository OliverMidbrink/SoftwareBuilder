from openai import OpenAI
from core.terminal import Terminal
import os
import subprocess

def t_gpt(input_text, prompt, model):
    gpt_response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_text}
        ],
        model=model,
        
    )

    t_gpt_output = gpt_response.choices[0].message.content
    return t_gpt_output 

def save_api_key(api_key):
    with open("core/api_key.txt", "w") as file:
        file.write(api_key)

def get_api_key():
    if not os.path.exists("./core/api_key.txt"):
        api_key = input("Please enter your API key (only first time you need to do this)\n")
        save_api_key(api_key)

def get_prompt(shell_history):
    controller = None
    instructions = None

    with open("core/controller.txt", "r") as file:
        controller = file.read()

    with open("instructions.txt", "r") as file:
        instructions = file.read()

    prompt = controller.format(instructions, str(shell_history))
    security_instruction = "Only output the next command in your work towards achieving the given instruction."

    return prompt, security_instruction

def iterating():
    new_prompt, security_instruction = get_prompt(terminal.return_history_as_dict())
    new_command = t_gpt(new_prompt, security_instruction, "gpt-4-1106-preview")
    print(' - Running command "{}".'.format(new_command))
    output, error = terminal.run_command(new_command)
    #print('Command output was "{}".'.format(output))

    if output == "QUIT\n":
        return False
    
    return True

api_key = None
if not os.path.exists("core/api_key.txt"):
    get_api_key()
    print("Installing the requirements for SoftwareBuilder...")
    command = "pip install -r core/requirements.txt"
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    print("Finished installing dependencies.")

with open("core/api_key.txt", "r") as file:
    api_key = file.read()

terminal = Terminal()

client = OpenAI(
    api_key=api_key,
)

