import React from "react";
import { logout } from "../actions/actions";

const LogoutButton = () => {
  const onLogout = () => {
    logout();
    localStorage.removeItem("jwtToken");
    window.location.href = "/login";
  };

  return (
    <button
      className="fixed bottom-8 right-8 bg-cyan-500 hover:bg-cyan-600 text-white px-4 py-2 rounded-md shadow cursor-pointer"
      onClick={onLogout}
    >
      Logout
    </button>
  );
};

export default LogoutButton;
