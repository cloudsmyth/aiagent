import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from os import sys

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    verbose = '--verbose' in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]

    if len(args) < 1:
        sys.exit("Error: no prompt provided")

    prompt = args[0]
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    count = 0
    while True:
        count += 1
        if count > 20:
            print("Max tries reached")
            sys.exit(1)
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error generating content: {e}")


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {
              response.usage_metadata.candidates_token_count}")

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_response = call_function(function_call_part, verbose)
        if (
            not function_call_response.parts
            or not function_call_response.parts[0].function_response
        ):
            raise Exception("empty function call response")
        if verbose:
            print(
                f"-> {function_call_response.parts[0].function_response.response}"
            )

        function_responses.append(function_call_response.parts[0])

    if not function_responses:
        raise Exception("No function responses")

    messages.append(types.Content(role="tool", parts=function_responses))


if __name__ == "__main__":
    main()
