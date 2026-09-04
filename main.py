from backend.app.pipeline import RAGPipeline


def main():
    """Simple CLI loop for the GraphRAG pipeline."""

    pipeline = RAGPipeline()

    print("=" * 60)
    print("Enterprise Intelligence GraphRAG")
    print("=" * 60)
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Question: ").strip()

        if question.lower() == "exit":
            break

        try:
            answer = pipeline.ask(question)
            print(f"\nAnswer: {answer}\n")
        except Exception as e:
            print(f"\nError: {e}\n")

        print("-" * 60)


if __name__ == "__main__":
    main()
