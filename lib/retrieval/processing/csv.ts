export const processCSV = async (
  csv: Blob
): Promise<{ content: string; tokens: number }[]> => {
  const { CSVLoader } = await import("langchain/document_loaders/fs/csv")
  const { RecursiveCharacterTextSplitter } = await import(
    "langchain/text_splitter"
  )
  const { encode } = await import("gpt-tokenizer")
  const { CHUNK_OVERLAP, CHUNK_SIZE } = await import("./config.ts")

  const loader = new CSVLoader(csv)
  const docs = await loader.load()
  let completeText = docs.map(doc => doc.pageContent).join("\n\n")

  const splitter = new RecursiveCharacterTextSplitter({
    chunkSize: CHUNK_SIZE,
    chunkOverlap: CHUNK_OVERLAP,
    separators: ["\n\n"]
  })
  const splitDocs = await splitter.createDocuments([completeText])

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
