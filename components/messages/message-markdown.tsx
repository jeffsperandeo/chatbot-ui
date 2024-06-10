import React, { FC, useEffect, useState } from "react"
import { MessageCodeBlock } from "./message-codeblock"
import MessageMarkdownMemoized from "./message-markdown-memoized"

interface MessageMarkdownProps {
  content: string
}

export const MessageMarkdown: FC<MessageMarkdownProps> = ({ content }) => {
  const [remarkGfm, setRemarkGfm] = useState<any>(null)
  const [remarkMath, setRemarkMath] = useState<any>(null)

  useEffect(() => {
    import("remark-gfm").then(module => setRemarkGfm(() => module.default))
    import("remark-math").then(module => setRemarkMath(() => module.default))
  }, [])

  if (!remarkGfm || !remarkMath) return null

  return (
    <MessageMarkdownMemoized
      remarkPlugins={[remarkGfm, remarkMath]}
      components={{
        p: ({ children }: { children: React.ReactNode }) => {
          return <p className="mb-2 last:mb-0">{children}</p>
        },
        img: ({ node, ...props }: { node: any; [key: string]: any }) => {
          return <img className="max-w-[67%]" {...props} />
        },
        code: ({
          node,
          className,
          children,
          ...props
        }: {
          node: any
          className: string
          children: React.ReactNode
          [key: string]: any
        }) => {
          const childArray = React.Children.toArray(children)
          const firstChild = childArray[0] as React.ReactElement
          const firstChildAsString = React.isValidElement(firstChild)
            ? (firstChild as React.ReactElement).props.children
            : firstChild

          if (firstChildAsString === "▍") {
            return <span className="mt-1 animate-pulse cursor-default">▍</span>
          }

          if (typeof firstChildAsString === "string") {
            childArray[0] = firstChildAsString.replace("`▍`", "▍")
          }

          const match = /language-(\w+)/.exec(className || "")

          if (
            typeof firstChildAsString === "string" &&
            !firstChildAsString.includes("\n")
          ) {
            return (
              <code className={className} {...props}>
                {childArray}
              </code>
            )
          }

          return (
            <MessageCodeBlock
              key={Math.random()}
              language={(match && match[1]) || ""}
              value={String(childArray).replace(/\n$/, "")}
              {...props}
            />
          )
        }
      }}
    >
      {content}
    </MessageMarkdownMemoized>
  )
}
