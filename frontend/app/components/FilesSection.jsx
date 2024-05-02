import React from "react";

const FilesSection = ({
  files,
  selectedFile,
  uploading,
  loading,
  handleNewFileUpload,
  handleFileSelect,
}) => (
  <div className="col-span-1 bg-gray-700 p-6 rounded-xl overflow-auto min-w-full shadow-lg h-full">
    <h3 className="text-xl font-bold text-cyan-500 mb-4">Previous Files</h3>
    <ul className="text-gray-400 overflow-auto h-auto mb-4">
      {loading && <p>Loading Data...</p>}
      {!loading &&
        files.map((file) => (
          <li
            key={file.id}
            className={`cursor-pointer hover:text-gray-100 transition-colors duration-150 p-2 rounded-md ${
              selectedFile === file.id
                ? "bg-cyan-500 text-gray-200 font-semibold"
                : "hover:bg-gray-600"
            }`}
            onClick={() => handleFileSelect(file.id)}
          >
            {file.filename}
          </li>
        ))}
    </ul>
    <label className="bg-cyan-500 hover:bg-cyan-600 justify-start text-white font-bold py-1 px-6 rounded focus:outline-none focus:shadow-outline transition-colors duration-200">
      + Upload New File
      <input
        type="file"
        className="hidden"
        onChange={handleNewFileUpload}
        disabled={uploading}
      />
    </label>
  </div>
);

export default FilesSection;
