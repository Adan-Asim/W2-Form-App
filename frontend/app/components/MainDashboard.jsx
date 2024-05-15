"use client";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  fetchUserChats,
  uploadNewFile,
  askQuestion,
  getJwtToken,
} from "../actions/actions";
import FilesSection from "./FilesSection";
import ChatSection from "./ChatSection";
import ShowError from "./ShowError";
import LogoutButton from "./LogoutButton";

const MainDashboard = () => {
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [conversations, setConversations] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [sendingMessage, setSendingMessage] = useState(false);

  const [uploadError, setUploadError] = useState("");
  const [chatError, setChatError] = useState("");
  const router = useRouter();

  useEffect(() => {
    if (!getJwtToken()) router.push("/login");

    fetchChatData();

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchChatData = async () => {
    setLoading(true);
    setChatError("");

    try {
      const response = await fetchUserChats();

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();

      const { chat_history_by_w2_form } = data;

      if (chat_history_by_w2_form && chat_history_by_w2_form.length > 0) {
        const filesData = chat_history_by_w2_form.map((item) => ({
          id: item.w2_form_id,
          filename: `W2 Form ${item.filename}`,
          fileInfo: `Chat history for W2 Form ${item.w2_form_id}`,
        }));
        
        setFiles(filesData);
        setConversations(chat_history_by_w2_form);
      }
    } catch (error) {
      console.error("Error fetching chat data:", error);
      setChatError(
        error + "" || "Failed to fetch chat data. Please try again.",
      );
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = (fileId) => {
    setSelectedFile(fileId);
  };

  const handleNewFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    setUploadError("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await uploadNewFile(formData);

      if (!response.ok) {
        throw new Error(
          `Failed to upload file, make sure it was in correct format: ${response.status}`,
        );
      }

      await fetchChatData();
    } catch (error) {
      setUploadError(error + "" || "Failed to upload file. Please try again.");
      console.error("Error uploading file:", error);
    } finally {
      setUploading(false);
    }
  };

  const handleSendMessage = async () => {
    if (!newMessage.trim() || !selectedFile) return;

    setSendingMessage(true);
    setChatError("");

    try {
      const response = await askQuestion({
        query: newMessage,
        file_id: selectedFile,
      });

      if (!response.ok) {
        throw new Error(
          `Failed to send message make sure its correct: ${response.status}`,
        );
      }

      const responseData = await response.json();

      const updatedConversations = conversations.map((conv) => {
        if (conv.w2_form_id === selectedFile) {
          return {
            ...conv,
            chat_history: [
              ...conv.chat_history,
              {
                user_query: newMessage,
                ai_response: responseData.ai_response,
                timestamp: responseData.timestamp,
              },
            ],
          };
        }
        return conv;
      });

      setConversations(updatedConversations);
      setNewMessage("");
    } catch (error) {
      console.error("Error sending message:", error);
      setChatError(error + "" || "Failed to send message. Please try again.");
    } finally {
      setSendingMessage(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-900">
      <div className="bg-gray-800 shadow-xl rounded-xl p-10 mx-10 my-10 w-full max-w-screen-2xl h-5/6 border border-cyan-500">
        <h2 className="text-3xl font-bold mb-8 text-center text-cyan-500">
          Dashboard
        </h2>
        <ShowError uploadError={uploadError} />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 h-full">
          <FilesSection
            files={files}
            selectedFile={selectedFile}
            uploading={uploading}
            loading={loading}
            handleNewFileUpload={handleNewFileUpload}
            handleFileSelect={handleFileSelect}
          />
          <ChatSection
            selectedFile={selectedFile}
            conversations={conversations}
            sendingMessage={sendingMessage}
            chatError={chatError}
            newMessage={newMessage}
            setNewMessage={setNewMessage}
            handleSendMessage={handleSendMessage}
          />
        </div>
      </div>
      <LogoutButton />
    </div>
  );
};

export default MainDashboard;
