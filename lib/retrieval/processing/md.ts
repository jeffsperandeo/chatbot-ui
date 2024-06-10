export const processMarkdown = async (
  markdown: Blob
): Promise<{ content: string; tokens: number }[]> => {
  const { encode } = await import("gpt-tokenizer")
  const { RecursiveCharacterTextSplitter } = await import(
    "langchain/text_splitter"
  )

  const fileBuffer = Buffer.from(await markdown.arrayBuffer())
  const textDecoder = new TextDecoder("utf-8")
  const textContent = textDecoder.decode(fileBuffer)

  const CHUNK_SIZE = 1000 // Define CHUNK_SIZE here
  const CHUNK_OVERLAP = 200 // Define CHUNK_OVERLAP here

  const splitter = RecursiveCharacterTextSplitter.fromLanguage("markdown", {
    chunkSize: CHUNK_SIZE,
    chunkOverlap: CHUNK_OVERLAP
  })

  const splitDocs = await splitter.createDocuments([textContent])

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
