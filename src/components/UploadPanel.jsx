export default function UploadPanel({ file, uploadInfo, isUploading, onFileChange, onSubmit }) {
  const chunkCount = uploadInfo?.chunks ?? uploadInfo?.total_chunks;

  return (
    <form onSubmit={onSubmit} className="rounded-lg border border-slate-300 bg-white p-5 shadow-sm">
      <h2 className="text-lg font-semibold">Upload PDF</h2>
      <label className="mt-4 grid min-h-36 cursor-pointer place-items-center rounded-lg border border-dashed border-slate-400 bg-slate-50 px-4 text-center text-sm text-slate-600 transition hover:border-teal-700 hover:bg-teal-50">
        <input
          className="sr-only"
          type="file"
          accept="application/pdf"
          onChange={(event) => onFileChange(event.target.files?.[0] || null)}
        />
        <span>{file ? file.name : "Click to choose a PDF file"}</span>
      </label>
      <button
        className="mt-4 h-11 w-full rounded-lg bg-teal-700 px-4 font-semibold text-white transition hover:bg-teal-800 disabled:cursor-wait disabled:opacity-60"
        type="submit"
        disabled={isUploading}
      >
        {isUploading ? "Uploading..." : "Upload PDF"}
      </button>
      {uploadInfo && (
        <div className="mt-4 rounded-lg bg-slate-50 p-3 text-sm text-slate-700">
          <p className="font-medium text-slate-900">{uploadInfo.message || "PDF uploaded successfully."}</p>
          <dl className="mt-3 grid gap-2">
            {uploadInfo.filename ? (
              <div>
                <dt className="text-xs font-semibold uppercase tracking-wide text-slate-500">File</dt>
                <dd className="mt-1 break-words text-slate-800">{uploadInfo.filename}</dd>
              </div>
            ) : null}
            {typeof chunkCount !== "undefined" ? (
              <div>
                <dt className="text-xs font-semibold uppercase tracking-wide text-slate-500">Chunks Indexed</dt>
                <dd className="mt-1 text-slate-800">{chunkCount}</dd>
              </div>
            ) : null}
            {uploadInfo.path ? (
              <div>
                <dt className="text-xs font-semibold uppercase tracking-wide text-slate-500">Saved Path</dt>
                <dd className="mt-1 break-words text-slate-800">{uploadInfo.path}</dd>
              </div>
            ) : null}
          </dl>
        </div>
      )}
    </form>
  );
}
