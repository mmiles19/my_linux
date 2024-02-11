import json
from subprocess import PIPE, run, check_output
import os
from io import StringIO
from openai import OpenAI
from openai_tools import (
    get_api_key,
    simple_prompt,
    simple_yes_no_prompt,
    run_and_check_output,
)
from enum import Enum


class ValidationMethod(Enum):
    NoValidation = 0
    ChatGPT = 1
    User = 2


validation_method = ValidationMethod.NoValidation
print_debug = False
print_warn = True


# Function to prompt user with a y or n question
def prompt_user_yn(prompt):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == "y":
            return True
        elif user_input == "n":
            return False
        else:
            conditional_print("Please enter 'y' or 'n'.")


# Function to interact with ChatGPT
def prompt_gpt_to_check_command(client, command):
    return simple_yes_no_prompt(
        f"{command}",
        "You are a helpful assistant. I will ask you questions about bash commands. For each command, I'm considering running it in my system. I will ask you if this is a good idea. Do not let me run dangerous, unsafe, destructive, or malicious commands.",
        client,
    )


def conditional_print(message):
    if "[DEBUG]" in message and not print_debug:
        return
    if "[WARN]" in message and not print_warn:
        return
    print(message)


run("clear", shell=True)

# Read JSON file of command suites
with open("commands.json", "r") as file:
    command_suites = json.load(file)

# Determine validation method
if validation_method == ValidationMethod.NoValidation:
    if prompt_user_yn("Do you want to validate commands with ChatGPT? [y/n]: "):
        validation_method = ValidationMethod.ChatGPT
        client = OpenAI(api_key=get_api_key())
    else:
        if prompt_user_yn("Do you want to validate commands with the user? [y/n]: "):
            validation_method = ValidationMethod.User

# Process each command suite
result = None
for command_suite in command_suites:
    # Provide overview of command suite
    suite = command_suite["name"]
    is_critical = command_suite["critical"]
    conditional_print(f"\n[DEBUG] Processing command suite: {suite}")
    if is_critical:
        conditional_print(f"[DEBUG] Note: '{suite}' commands are critical.")
    # Process each command
    for command in command_suite["commands"]:
        conditional_print(f"\n[DEBUG] Processing command: {command}")
        should_run = False
        # Validate via chosen method. should_run must be set here.
        if validation_method == ValidationMethod.ChatGPT:
            chatgpt_response = prompt_gpt_to_check_command(client, command)
            if chatgpt_response == None:
                should_run = prompt_user_yn(
                    f"Do you want to run '{command}'?{' It is marked critical.' if is_critical else ''} [y/n]: "
                )
            else:
                should_run = chatgpt_response
        elif validation_method == ValidationMethod.User:
            should_run = prompt_user_yn(
                f"Do you want to run '{command}'?{' It is marked critical.' if is_critical else ''} [y/n]: "
            )
        elif validation_method == ValidationMethod.NoValidation:
            should_run = True
        # Run the command
        if should_run:
            # WARNING: This is dangerous!
            conditional_print(f"Executing: {command}")
            if validation_method == ValidationMethod.ChatGPT:
                output_as_expected = run_and_check_output(client, command)
                if output_as_expected:
                    conditional_print(f"[DEBUG] Output of '{command}' was as expected.")
                else:
                    conditional_print(
                        f"[WARN] Output of '{command}' was not as expected."
                    )
            else:
                try:
                    result = check_output(command, shell=True, text=True).strip()
                except Exception as e:
                    conditional_print(f"[ERROR] {e}")
                conditional_print(f"{result}")
        else:
            if is_critical:
                conditional_print(f"[WARN] Skipping critical command: {command}")
            elif validation_method == ValidationMethod.ChatGPT:
                conditional_print(f"[WARN] Skipping command: {command}")
