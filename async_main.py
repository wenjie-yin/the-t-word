import asyncio
import ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

with open("system_prompts/default.txt", "r") as f:
    system_text = f.read()

template = ChatPromptTemplate([
    ("system", system_text),
    #("placeholder", "{last_snysnession_summary}"),
    ("placeholder", "{conversation}"),
    ("user", "{user_input}"),
])

conversation_history = []

llm = ChatOllama(
    model="llama3.2",
    temperature=0)

async def get_input():
    print("Start typing your input. Press Enter to record it. Press Ctrl+C to stop and save all input.")
    while True:
        try:
            # Wait for user input asynchronously
            user_input = await asyncio.to_thread(input)
            
            prompt = template.invoke({"user_input": user_input, \
                                      "conversation": conversation_history})
            response = llm.invoke(prompt)
            print(response.content)

            # append both to history
            conversation_history.append(('user', user_input))
            conversation_history.append(('assistant', response.content))
            
        except asyncio.CancelledError:
            break

async def main():
    
    input_task = asyncio.create_task(get_input())

    try:
        # Keep the program running until interrupted
        await input_task
    except KeyboardInterrupt:
        # On Ctrl+C, cancel the input task
        input_task.cancel()

    finally:
        # Write the saved input to a file even if interrupted
        with open("saved.txt", "w") as f:
            f.write("\n".join(saved_input))
        print("\nInput saved to saved.txt")


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
