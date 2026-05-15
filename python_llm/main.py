import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(20):
        final = generate_content(client, messages, args)
        if final:
            print(final)
            return
    print("Max iterations reached")
    sys.exit(1)

def generate_content(client, messages, args):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
        )
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    function_results = []
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)
            if function_call_result.parts is None:
                raise Exception("parts is None")
            if function_call_result.parts[0].function_response is None:
                raise Exception("no function_response")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("no response")
            function_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    if not response.function_calls:
        return response.text
    messages.append(types.Content(role="user", parts=function_results))


if __name__ == "__main__":
    main()

