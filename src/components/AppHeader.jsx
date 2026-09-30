export default function AppHeader({ fileName, onLogout, status }) {
  return (
    <header className="flex flex-col gap-4 border-b border-slate-300 pb-5 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <h1 className="text-3xl font-bold tracking-normal sm:text-5xl">PDF Chatbot</h1>
        <p className="mt-2 text-sm text-slate-600">{status}</p>
      </div>
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <div className="max-w-full rounded-full border border-slate-300 bg-white px-4 py-2 text-sm text-slate-600 shadow-sm">
          {fileName || "No PDF selected"}
        </div>
        {onLogout && (
          <button
            className="h-10 rounded-lg border border-slate-300 bg-white px-4 text-sm font-semibold text-slate-700 transition hover:border-teal-700 hover:text-teal-800"
            type="button"
            onClick={onLogout}
          >
            Logout
          </button>
        )}
      </div>
    </header>
  );
}
