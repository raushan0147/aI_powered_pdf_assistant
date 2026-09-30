import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import { askQuestion, clearAuthToken, uploadPdf } from "../api";
import AnswerPanel from "../components/AnswerPanel";
import AppHeader from "../components/AppHeader";
import ErrorAlert from "../components/ErrorAlert";
import QuestionPanel from "../components/QuestionPanel";
import UploadPanel from "../components/UploadPanel";

function getErrorMessage(error) {
  return (
    error?.response?.data?.detail ||
    error?.response?.data?.message ||
    error?.message ||
    "Something went wrong"
  );
}

export default function PdfChatPage() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [uploadInfo, setUploadInfo] = useState(null);
  const [question, setQuestion] = useState("");
  const [askedQuestion, setAskedQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [status, setStatus] = useState("Ready");
  const [error, setError] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [isAsking, setIsAsking] = useState(false);

  const canAsk = useMemo(() => question.trim().length > 0 && !isAsking, [question, isAsking]);

  function handleLogout() {
    clearAuthToken();
    navigate("/login");
  }

  async function handleUpload(event) {
    event.preventDefault();
    if (!file) {
      setError("Choose a PDF first.");
      return;
    }

    setIsUploading(true);
    setError("");
    setStatus("Uploading and indexing PDF...");

    try {
      const result = await uploadPdf(file);
      setUploadInfo(result);
      setStatus("PDF indexed successfully.");
    } catch (err) {
      setError(getErrorMessage(err));
      setStatus("Upload failed.");
    } finally {
      setIsUploading(false);
    }
  }

  async function handleAsk(event) {
    event.preventDefault();
    const submittedQuestion = question.trim();

    setIsAsking(true);
    setError("");
    setAskedQuestion(submittedQuestion);
    setAnswer("Searching your PDFs...");
    setStatus("Generating answer...");

    try {
      const result = await askQuestion(submittedQuestion);
      setAnswer(result || "No response returned.");
      setStatus("Answer ready.");
    } catch (err) {
      setAnswer("");
      setError(getErrorMessage(err));
      setStatus("Question failed.");
    } finally {
      setIsAsking(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-100 px-4 py-8 text-slate-950 sm:px-6 lg:px-8">
      <div className="mx-auto grid w-full max-w-6xl gap-5">
        <AppHeader fileName={uploadInfo?.filename || file?.name} onLogout={handleLogout} status={status} />
        <ErrorAlert message={error} />

        <section className="grid gap-5 lg:grid-cols-[0.9fr_1.1fr]">
          <UploadPanel
            file={file}
            uploadInfo={uploadInfo}
            isUploading={isUploading}
            onFileChange={setFile}
            onSubmit={handleUpload}
          />
          <QuestionPanel
            canAsk={canAsk}
            isAsking={isAsking}
            onQuestionChange={setQuestion}
            onSubmit={handleAsk}
            question={question}
          />
        </section>

        <AnswerPanel answer={answer} question={askedQuestion} />
      </div>
    </main>
  );
}
