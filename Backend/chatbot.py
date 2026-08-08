from retriever import (
    load_model,
    connect_database,
    retrieve_chunks
)

from generator import generate_answer


def main():

    print("Loading model...")
    model = load_model()

    print("Connecting database...")
    collection = connect_database()

    print("\nPortfolio Chatbot Ready!")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            break

        # Retrieve relevant chunks
        chunks = retrieve_chunks(
            model,
            collection,
            question
        )

        # Generate final answer
        answer = generate_answer(
            question,
            chunks
        )

        print("\nBot:")
        print(answer)
        print()


if __name__ == "__main__":
    main()