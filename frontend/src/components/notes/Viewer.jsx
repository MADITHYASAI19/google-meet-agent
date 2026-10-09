import React from 'react';
import ReactMarkdown from 'react-markdown';
import { LuSearch } from 'react-icons/lu';

const NotesViewer = ({ content, search }) => {
  const highlightText = (text) => {
    if (!search) return text;
    const parts = text.split(new RegExp(`(${search})`, 'gi'));
    return parts.map((part, i) =>
      part.toLowerCase() === search.toLowerCase()
        ? <mark key={i} className="bg-yellow-200 dark:bg-yellow-800 text-gray-900 dark:text-white rounded-sm">{part}</mark>
        : part
    );
  };

  return (
    <div className="bg-white dark:bg-dark-card p-8 rounded-2xl border border-gray-200 dark:border-gray-700 min-h-[600px] prose dark:prose-invert max-w-none">
      <ReactMarkdown
        components={{
          p: ({ children }) => <p className="mb-4 leading-relaxed text-gray-700 dark:text-gray-300">{highlightText(children)}</p>,
          h1: ({ children }) => <h1 className="text-3xl font-bold mb-6 text-gray-900 dark:text-white">{highlightText(children)}</h1>,
          h2: ({ children }) => <h2 className="text-2xl font-bold mt-8 mb-4 text-gray-800 dark:text-gray-200">{highlightText(children)}</h2>,
          h3: ({ children }) => <h3 className="text-xl font-semibold mt-6 mb-3 text-gray-800 dark:text-gray-300">{highlightText(children)}</h3>,
          li: ({ children }) => <li className="mb-1">{highlightText(children)}</li>,
          code: ({ children }) => <code className="bg-gray-100 dark:bg-gray-800 px-1 rounded text-sm">{highlightText(children)}</code>,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};

export default NotesViewer;
