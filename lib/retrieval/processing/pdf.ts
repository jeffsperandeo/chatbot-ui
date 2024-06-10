import { FileItemChunk } from "@/types"
import { encode } from "gpt-tokenizer"
const PDFLoader = require("langchain/document_loaders/fs/pdf").PDFLoader
const RecursiveCharacterTextSplitter =
  require("langchain/text_splitter").RecursiveCharacterTextSplitter
import { CHUNK_OVERLAP, CHUNK_SIZE } from "."

export const processPdf = async (pdf: Blob): Promise<FileItemChunk[]> => {
  const loader = new PDFLoader(pdf)
  const docs = await loader.load()
  let completeText = docs.map((doc: any) => doc.pageContent).join(" ")

  const splitter = new RecursiveCharacterTextSplitter({
    chunkSize: CHUNK_SIZE,
    chunkOverlap: CHUNK_OVERLAP
  })
  const splitDocs = await splitter.createDocuments([completeText])

  let chunks: FileItemChunk[] = []

  for (let i = 0; i < splitDocs.length; i++) {
    const doc = splitDocs[i]

    chunks.push({
      content: doc.pageContent,
      tokens: encode(doc.pageContent).length
    })
  }

  return chunks
}
