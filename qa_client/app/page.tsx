"use client";

import { useState } from "react";

interface Message {
    role: "user" | "assistant";
    content: string;
    source?: string;
}

export default function Home() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage: Message = { role: "user", content: input };
        setMessages((prev) => [...prev, userMessage]);
        setInput("");
        setIsLoading(true);

        try {
            const response = await fetch("http://localhost:8000/api/ask/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: input }),
            });

            const data = await response.json();
            const assistantMessage: Message = {
                role: "assistant",
                content: data.answer,
                source: data.source,
            };
            setMessages((prev) => [...prev, assistantMessage]);
        } catch (error) {
            setMessages((prev) => [
                ...prev,
                { role: "assistant", content: "Error connecting to API" },
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-screen bg-zinc-900">
            <header className="p-4 border-b border-zinc-700">
                <h1 className="text-xl font-semibold text-white text-center">
                    QA Router Assistant
                </h1>
            </header>

            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.length === 0 ? (
                    <div className="flex items-center justify-center h-full">
                        <p className="text-zinc-500 text-lg">
                            Ask a question about geo data or regulations
                        </p>
                    </div>
                ) : (
                    messages.map((message, index) => (
                        <div
                            key={index}
                            className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
                        >
                            <div
                                className={`max-w-2xl px-4 py-3 rounded-2xl ${
                                    message.role === "user"
                                        ? "bg-blue-600 text-white rounded-br-md"
                                        : "bg-zinc-700 text-zinc-100 rounded-bl-md"
                                }`}
                            >
                                <p className="whitespace-pre-wrap">{message.content}</p>
                                {message.source && (
                                    <span
                                        className={`inline-block mt-2 px-2 py-1 text-xs rounded-full ${
                                            message.source === "geo"
                                                ? "bg-green-600"
                                                : message.source === "regulation"
                                                    ? "bg-purple-600"
                                                    : "bg-zinc-600"
                                        }`}
                                    >
                    Source: {message.source}
                  </span>
                                )}
                            </div>
                        </div>
                    ))
                )}

                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-zinc-700 px-4 py-3 rounded-2xl rounded-bl-md">
                            <div className="flex space-x-2">
                                <div className="w-2 h-2 bg-zinc-400 rounded-full animate-bounce" />
                                <div className="w-2 h-2 bg-zinc-400 rounded-full animate-bounce delay-100" />
                                <div className="w-2 h-2 bg-zinc-400 rounded-full animate-bounce delay-200" />
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Input Form */}
            <form onSubmit={handleSubmit} className="p-4 border-t border-zinc-700">
                <div className="flex gap-3 max-w-4xl mx-auto">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask about soil types, flood zones, building regulations..."
                        className="flex-1 px-4 py-3 bg-zinc-800 text-white rounded-xl border border-zinc-600 focus:outline-none focus:border-blue-500 placeholder-zinc-500"
                    />
                    <button
                        type="submit"
                        disabled={isLoading || !input.trim()}
                        className="px-6 py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        Send
                    </button>
                </div>
            </form>
        </div>
    );
}