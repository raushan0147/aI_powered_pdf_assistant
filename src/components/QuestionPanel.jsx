export default function QuestionPanel({ canAsk, isAsking, onQuestionChange, onSubmit, question }) {
  function handleQuestionKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();

      if (canAsk) {
        event.currentTarget.form.requestSubmit();
      }
    }
  }

  return (
    <form onSubmit={onSubmit} className="rounded-lg border border-slate-300 bg-white p-5 shadow-sm">
      <h2 className="text-lg font-semibold">Ask Question</h2>
      <textarea
        className="mt-4 min-h-36 w-full resize-y rounded-lg border border-slate-300 bg-slate-50 p-4 text-sm outline-none transition focus:border-teal-700 focus:ring-4 focus:ring-teal-700/10"
        placeholder="Ask something from your uploaded PDFs"
        value={question}
        onChange={(event) => onQuestionChange(event.target.value)}
        onKeyDown={handleQuestionKeyDown}
      />
      <button
        className="mt-4 h-11 w-full rounded-lg bg-teal-700 px-4 font-semibold text-white transition hover:bg-teal-800 disabled:cursor-wait disabled:opacity-60"
        type="submit"
        disabled={!canAsk}
      >
        {isAsking ? "Asking..." : "Ask"}
      </button>
    </form>
  );
}
