const ShowError = ({ uploadError }) =>
  uploadError && <p className="text-red-500 text-center mb-4">{uploadError}</p>;
export default ShowError;
