"use client";

import { useState, FormEvent, useEffect, useRef } from "react";
import { Send, ChevronDown } from "lucide-react";
import { Message, Route, L1Request, L2Request } from "../types/chat";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [selectedRoute, setSelectedRoute] = useState<string>("/chat/l1");
  const [isDropdownOpen, setIsDropdownOpen] = useState<boolean>(false);
  const [ws, setWs] = useState<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const routes: Route[] = [
    { path: "/chat/l1", name: "L1 - Basic API Chatbot" },
    { path: "/chat/l2", name: "L2 - Movie Script Storage" },
    { path: "/chat/l3", name: "L3 - RAG with Vector Search" },
    { path: "/chat/l4", name: "L4 - Scaled Version" },
    { path: "/chat/l5", name: "L5 - Optimize for Latency & Chat History" },
  ];

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const formatRequestBody = (message: string): L1Request | L2Request => {
    return selectedRoute === "/chat/l1"
      ? { character: "default", user_message: message }
      : { script: message };
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setInput("");
    setIsLoading(true);

    try {
      let data: string;
      if (selectedRoute === "/chat/l5" && ws) {
        ws.send(JSON.stringify(formatRequestBody(userMessage)));
      } else {
        const response = await fetch(`http://127.0.0.1:8000${selectedRoute}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formatRequestBody(userMessage)),
        });

        if (!response.ok) throw new Error("Network response was not ok");
        data = await response.json();
      }

      setMessages((prev) => [...prev, { role: "assistant", content: data }]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "system",
          content: "Sorry, there was an error processing your request.",
        },
      ]);
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (selectedRoute === "/chat/l5") {
      const test = new WebSocket("ws://127.0.0.1:8000/chat/l5");
      setWs(test);

      test.onmessage = (event) => console.log(event.data);
    }

    return () => {
      if (ws) ws.close();
    };
  }, [selectedRoute]);

  const formatContent = (content: any): string => {
    if (typeof content === "string") return content;
    try {
      return JSON.stringify(content, null, 2);
    } catch (e) {
      return String(content);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <Card className="max-w-3xl mx-auto">
        <CardHeader className="border-b">
          <div className="flex items-center justify-between">
            <CardTitle className="text-xl text-gray-800">
              AI Chatbot Demo
            </CardTitle>
            <div className="relative">
              <button
                type="button"
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
              >
                {routes.find((r) => r.path === selectedRoute)?.name}
                <ChevronDown className="w-4 h-4" />
              </button>

              {isDropdownOpen && (
                <div className="absolute right-0 mt-2 w-64 bg-white border rounded-md shadow-lg z-10">
                  {routes.map((route) => (
                    <button
                      key={route.path}
                      onClick={() => {
                        setSelectedRoute(route.path);
                        setIsDropdownOpen(false);
                        setMessages([]);
                      }}
                      className="w-full text-left px-4 py-2 hover:bg-gray-50 transition-colors first:rounded-t-md last:rounded-b-md"
                    >
                      {route.name}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        </CardHeader>

        <CardContent className="p-0">
          <div className="h-[600px] flex flex-col">
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`
                    max-w-[80%] rounded-lg p-4 shadow-sm
                    ${
                      message.role === "user"
                        ? "ml-auto bg-blue-500 text-white"
                        : message.role === "assistant"
                          ? "bg-white"
                          : "bg-red-50 text-red-800"
                    }
                  `}
                >
                  {message.role === "assistant" ? (
                    <pre className="whitespace-pre-wrap font-mono text-sm">
                      {formatContent(message.content)}
                    </pre>
                  ) : (
                    <div className="text-sm">
                      {formatContent(message.content)}
                    </div>
                  )}
                </div>
              ))}
              {isLoading && (
                <div className="flex space-x-2 p-4">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <form onSubmit={handleSubmit} className="p-4 border-t bg-white">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Type your message..."
                  disabled={isLoading}
                  className="flex-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
                />
                <button
                  type="submit"
                  disabled={isLoading || !input.trim()}
                  className="p-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-blue-300 disabled:cursor-not-allowed transition-colors"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </form>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ChatInterface;
