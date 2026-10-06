def create_chunks(text, max_chars=1000, overlap_paragraphs=1):
    # Split the document into paragraphs
    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = []
    current_length = 0

    for paragraph in paragraphs:

        paragraph_length = len(paragraph)

        # If adding this paragraph makes the chunk too large,
        # save the current chunk first.
        if (
            current_chunk
            and current_length + paragraph_length > max_chars
        ):
            chunks.append("\n\n".join(current_chunk))

            # Keep the last paragraph for overlap
            current_chunk = current_chunk[-overlap_paragraphs:]

            current_length = sum(
                len(p) + 2
                for p in current_chunk
            )

        current_chunk.append(paragraph)
        current_length += paragraph_length + 2

    # Add the final chunk
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks


# Read notes
with open("notes.txt", "r", encoding="utf-8") as f:
    notes = f.read()


# Create chunks
chunks = create_chunks(notes)


print("Number of chunks:", len(chunks))


# Show first 5 chunks
for i, chunk in enumerate(chunks[:5]):

    print(f"\n--- Chunk {i} ---")
    print(chunk)

    print("\nCharacters:", len(chunk))