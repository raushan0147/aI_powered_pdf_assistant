import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";

import { getAuthToken, loginUser, registerUser, setAuthToken } from "../api";

function getErrorMessage(error) {
  return (
    error?.response?.data?.detail ||
    error?.response?.data?.message ||
    error?.message ||
    "Something went wrong"
  );
}

export default function AuthPage({ mode }) {
  const navigate = useNavigate();
  const isRegister = mode === "register";
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (getAuthToken()) {
    return <Navigate to="/" replace />;
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      if (isRegister) {
        await registerUser({ name, email, password });
        navigate("/login", { replace: true });
        return;
      }

      const result = await loginUser({ email, password });
      setAuthToken(result.access_token);
      navigate("/", { replace: true });
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="grid min-h-screen place-items-center bg-slate-100 px-4 py-8 text-slate-950">
      <form onSubmit={handleSubmit} className="w-full max-w-md rounded-lg border border-slate-300 bg-white p-6 shadow-sm">
        <h1 className="text-2xl font-bold">{isRegister ? "Create account" : "Login"}</h1>
        <p className="mt-2 text-sm text-slate-600">
          {isRegister ? "Register to use the PDF chatbot." : "Login to continue to your PDFs."}
        </p>

        {error && (
          <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-700">
            {error}
          </div>
        )}

        {isRegister && (
          <label className="mt-5 block text-sm font-medium text-slate-700">
            Name
            <input
              className="mt-2 h-11 w-full rounded-lg border border-slate-300 bg-slate-50 px-3 text-sm outline-none transition focus:border-teal-700 focus:ring-4 focus:ring-teal-700/10"
              value={name}
              onChange={(event) => setName(event.target.value)}
              required
            />
          </label>
        )}

        <label className="mt-5 block text-sm font-medium text-slate-700">
          Email
          <input
            className="mt-2 h-11 w-full rounded-lg border border-slate-300 bg-slate-50 px-3 text-sm outline-none transition focus:border-teal-700 focus:ring-4 focus:ring-teal-700/10"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </label>

        <label className="mt-4 block text-sm font-medium text-slate-700">
          Password
          <input
            className="mt-2 h-11 w-full rounded-lg border border-slate-300 bg-slate-50 px-3 text-sm outline-none transition focus:border-teal-700 focus:ring-4 focus:ring-teal-700/10"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />
        </label>

        <button
          className="mt-5 h-11 w-full rounded-lg bg-teal-700 px-4 font-semibold text-white transition hover:bg-teal-800 disabled:cursor-wait disabled:opacity-60"
          disabled={isSubmitting}
          type="submit"
        >
          {isSubmitting ? "Please wait..." : isRegister ? "Register" : "Login"}
        </button>

        <Link className="mt-4 block w-full text-center text-sm font-medium text-teal-800" to={isRegister ? "/login" : "/register"}>
          {isRegister ? "Already have an account? Login" : "Need an account? Register"}
        </Link>
      </form>
    </main>
  );
}
