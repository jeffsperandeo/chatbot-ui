import React, { FC, useEffect, useState } from "react"

interface MessageMarkdownMemoizedProps {
  children: string
  remarkPlugins: any[]
  components: any
}

const MessageMarkdownMemoized: FC<MessageMarkdownMemoizedProps> = ({
  children,
  remarkPlugins,
  components
}) => {
  const [ReactMarkdown, setReactMarkdown] = useState<any>(null)

  useEffect(() => {
    import("react-markdown").then(module =>
      setReactMarkdown(() => module.default)
    )
  }, [])

  if (!ReactMarkdown) return null

  return (
    <ReactMarkdown remarkPlugins={remarkPlugins} components={components}>
      {children}
    </ReactMarkdown>
  )
}

export default React.memo(MessageMarkdownMemoized)
