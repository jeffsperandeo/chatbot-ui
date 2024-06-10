export const processDocX = async (
  text: string
): Promise<{ content: string; tokens: number }[]> => {
  const { RecursiveCharacterTextSplitter } = await import(
    "langchain/text_splitter"
  )
  const { encode } = await import("gpt-tokenizer")
  const { CHUNK_OVERLAP, CHUNK_SIZE } = await import("./constants.ts")

  const splitter = new RecursiveCharacterTextSplitter({
    chunkSize: CHUNK_SIZE,
    chunkOverlap: CHUNK_OVERLAP
  })
  const splitDocs = await splitter.createDocuments([text])

  let chunks: { content: string; tokens: number }[] = []

  for (let i = 0; i < splitDocs.length; i++) {
    const doc = splitDocs[i]

    chunks.push({
      content: doc.pageContent,
      tokens: encode(doc.pageContent).length
    })
  }

  return chunks
}
