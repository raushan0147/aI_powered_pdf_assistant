export default function AnswerPanel({ answer, question }) {
  const responseQuestion = answer && typeof answer === "object" ? answer.question : "";
  const responseAnswer = answer && typeof answer === "object" ? answer.answer : answer;

  return (
    <section className="min-h-72 rounded-lg border border-slate-300 bg-white p-5 shadow-sm">
      {question ? (
        <div className="mt-4 rounded-lg border border-slate-200 bg-slate-50 p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Question</p>
          <p className="mt-2 whitespace-pre-wrap text-sm leading-6 text-slate-800">{question}</p>
        </div>
      ) : null}
      <div className="mt-4 rounded-lg border border-slate-200 bg-slate-50 p-4">
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Answer</p>
        <div className="mt-2 whitespace-pre-wrap rounded-lg bg-white p-3 text-sm leading-7 text-slate-700">
          {responseAnswer || "The backend answer will appear here."}
        </div>
        {responseQuestion && responseQuestion !== question ? (
          <div className="mt-3 border-t border-slate-200 pt-3">
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Backend Question</p>
            <p className="mt-1 whitespace-pre-wrap text-sm leading-6 text-slate-700">{responseQuestion}</p>
          </div>
        ) : null}
      </div>
    </section>
  );
}
