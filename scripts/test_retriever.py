from memory.vectorstore import VDB

def main():
    docs_and_scores = VDB.similarity_search_with_score("eat", k=4)
    for doc, score in docs_and_scores:
        print(f"{score:.2f} | {doc.metadata['source']} | {doc.page_content[:60]}...")

if __name__ == "__main__":
    main()
