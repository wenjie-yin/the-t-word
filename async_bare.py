import asyncio

# Initialize an empty list to store the inputs
saved_input = []

async def get_input():
    print("Start typing your input. Press Enter to record it. Press Ctrl+C to stop and save all input.")
    while True:
        try:
            # Wait for user input asynchronously
            user_input = await asyncio.to_thread(input)
            saved_input.append(user_input)
            print("noted")
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
