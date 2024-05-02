"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { loginUser, signupUser } from "../actions/actions";

const AuthForm = ({ isSignup }) => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = isSignup
        ? await signupUser({ name, email, password })
        : await loginUser({ email, password });

      if (response.ok) {
        const data = await response.json();
        if (!isSignup) {
          localStorage.setItem("jwtToken", data?.access_token);
          router.push("/dashboard");
          return;
        }
        router.push("/login");
      } else {
        const data = await response.json();
        setError(data.message);
      }
    } catch (error) {
      console.error("API Error:", error);
      setError("An error occurred. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-[#0e1017]">
      <form
        onSubmit={handleSubmit}
        className="bg-[#1F2833] shadow-md rounded-lg p-8 w-96 border border-[#66FCF1]"
      >
        <h2 className="text-3xl font-bold mb-6 text-center text-[#66FCF1]">
          {isSignup ? "Create Account" : "Log In"}
        </h2>
        {error && (
          <div className="my-3 text-[#FF6347] text-sm text-center">{error}</div>
        )}

        {isSignup && (
          <div className="mb-6">
            <label
              className="block text-[#C5C6C7] text-sm font-bold mb-2"
              htmlFor="name"
            >
              Name
            </label>
            <input
              className="appearance-none border rounded w-full py-2 px-3 text-[#0B0C10] leading-tight focus:outline-none focus:shadow-outline bg-[#C5C6C7] placeholder-[#0B0C10]"
              id="name"
              type="text"
              placeholder="Enter your name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
        )}
        <div className="mb-6">
          <label
            className="block text-[#C5C6C7] text-sm font-bold mb-2"
            htmlFor="email"
          >
            Email
          </label>
          <input
            className="appearance-none border rounded w-full py-2 px-3 text-[#0B0C10] leading-tight focus:outline-none focus:shadow-outline bg-[#C5C6C7] placeholder-[#0B0C10]"
            id="email"
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="mb-6">
          <label
            className="block text-[#C5C6C7] text-sm font-bold mb-2"
            htmlFor="password"
          >
            Password
          </label>
          <input
            className="appearance-none border rounded w-full py-2 px-3 text-[#0B0C10] leading-tight focus:outline-none focus:shadow-outline bg-[#C5C6C7] placeholder-[#0B0C10]"
            id="password"
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {isSignup ? (
          <p
            className="text-[#66FCF1] text-sm my-4 text-center cursor-pointer"
            onClick={() => router.push("login")}
          >
            Already have an account? login from <u> here</u>
          </p>
        ) : (
          <p
            className="text-[#66FCF1] text-sm my-4 text-center cursor-pointer"
            onClick={() => router.push("/signup")}
          >
            Dont have an account? sign up from <u>here</u>
          </p>
        )}
        <div className="flex justify-center">
          <button
            className={`bg-[#45A29E] hover:bg-[#66FCF1] text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition-colors duration-200 ${
              loading ? "opacity-50 cursor-not-allowed" : ""
            }`}
            type="submit"
            disabled={loading}
          >
            {loading ? "Loading..." : isSignup ? "Join Us" : "Sign In"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AuthForm;
