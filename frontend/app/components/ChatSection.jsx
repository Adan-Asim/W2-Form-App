import React from "react";

const ChatSection = ({
  selectedFile,
  conversations,
  sendingMessage,
  chatError,
  newMessage,
  setNewMessage,
  handleSendMessage,
}) => (
  <div className="col-span-2 bg-gray-700 p-6 rounded-xl shadow-lg overflow-auto flex flex-col">
    {selectedFile && (
      <>
        <div className="flex flex-col mb-4 flex-grow">
          <h3 className="text-xl font-bold text-cyan-500 mb-2">W2 Form Chat</h3>
          <div className="bg-gray-800 p-4 rounded-lg mb-4 overflow-y-auto w-full flex-grow min-h-96 max-h-96 lg:h-full lg:min-h-4/5 lg:max-h-4/5">
            {conversations
              .filter((conv) => conv.w2_form_id === selectedFile)
              .map((conv, index) => (
                <div key={index} className="flex flex-col mb-4">
                  {conv.chat_history.map((msg, idx) => (
                    <div key={idx} className="flex flex-col my-2">
                      <div
                        className={
                          "rounded-lg p-3 bg-cyan-500 text-gray-900 self-end"
                        }
                      >
                        <p>{msg.user_query}</p>
                      </div>
                      {msg.ai_response && (
                        <div
                          className={
                            "rounded-lg p-3 mt-2 bg-gray-600 text-gray-300 self-start"
                          }
                        >
                          <p>{msg.ai_response}</p>
                        </div>
                      )}
                      <p className="text-xs text-gray-400 mt-1">
                        {msg.timestamp}
                      </p>
                    </div>
                  ))}
                </div>
              ))}
            {!(
              conversations.filter((conv) => conv.w2_form_id === selectedFile)
                .length > 0
            ) && (
              <p className="text-gray-200">No conversation history exists...</p>
            )}
          </div>
        </div>
        <div className="flex items-center">
          <input
            type="text"
            placeholder="Ask a question..."
            className="w-full p-2 rounded-l-lg focus:outline-none text-black"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !sendingMessage) {
                handleSendMessage();
              }
            }}
          />
          <button
            className="bg-cyan-500 hover:bg-cyan-600 text-white py-2 px-3 rounded-r-lg focus:outline-none"
            onClick={handleSendMessage}
            disabled={sendingMessage}
          >
            {sendingMessage ? "Sending..." : "Send"}
          </button>
        </div>
      </>
    )}
    {!chatError && !selectedFile && (
      <p className="text-gray-400 m-auto min-h-full">
        Select an existing file or upload a new one to start the conversation...
      </p>
    )}
    {chatError && <p className="text-red-500 text-sm mt-2">{chatError}</p>}
  </div>
);

export default ChatSection;
