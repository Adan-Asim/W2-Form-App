const SITE_BASE_URL =
  process.env.REACT_APP_BACKEND_BASE_URL || "http://0.0.0.0:5000"; //window.location.origin;

export const getJwtToken = () => localStorage.getItem("jwtToken", "");

export const loginUser = async (data) => {
  const response = await fetch(`${SITE_BASE_URL}/api/user/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return response;
};

export const signupUser = async (data) => {
  const response = await fetch(`${SITE_BASE_URL}/api/user/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return response;
};

export const fetchUserChats = async () => {
  const response = await fetch(`${SITE_BASE_URL}/api/user/chat-history`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getJwtToken()}`,
    },
  });
  return response;
};

export const uploadNewFile = async (formData) => {
  const response = await fetch(`${SITE_BASE_URL}/api/file/upload`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${getJwtToken()}`,
    },
    body: formData,
  });
  return response;
};

export const askQuestion = async (data) => {
  const response = await fetch(`${SITE_BASE_URL}/api/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getJwtToken()}`,
    },
    body: JSON.stringify(data),
  });
  return response;
};

export const logout = () =>
  fetch(`${SITE_BASE_URL}/api/logout`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${getJwtToken()}`,
    },
  });
