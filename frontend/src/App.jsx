
import { useEffect, useState } from "react";
import "./App.css";
import ReactMarkdown from "react-markdown";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [documents, setDocuments] = useState([]);
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [asking, setAsking] = useState(false);
  const [message, setMessage] = useState("");

  async function loadDocuments() {
    try {
      const response = await fetch(`${API_URL}/documents/`);

      if (!response.ok) {
        throw new Error("Could not load documents");
      }

      const data = await response.json();
      setDocuments(data);

      if (selectedDocument) {
        const updated = data.find(
          (doc) => doc.id === selectedDocument.id
        );
        setSelectedDocument(updated || null);
      }
    } catch (error) {
      setMessage(error.message);
    }
  }

  useEffect(() => {
    loadDocuments();
  }, []);

  async function handleUpload(event) {
    event.preventDefault();

    if (!file) {
      setMessage("Please select a PDF file.");
      return;
    }

    setUploading(true);
    setMessage("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_URL}/documents/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      setMessage(
        `Uploaded and indexed successfully! ${data.total_chunks} chunks created.`
      );
      setFile(null);
      event.target.reset();

      await loadDocuments();

      setSelectedDocument({
        id: data.document_id,
        filename: data.filename,
        status: data.status,
      });

      setAnswer("");
      setSources([]);
    } catch (error) {
      setMessage(error.message);
    } finally {
      setUploading(false);
    }
  }

  async function handleAsk(event) {
    event.preventDefault();

    if (!selectedDocument) {
      setMessage("Please select an indexed document.");
      return;
    }

    if (!question.trim()) {
      return;
    }

    setAsking(true);
    setMessage("");
    setAnswer("");
    setSources([]);

    try {
      const response = await fetch(
        `${API_URL}/chat/${selectedDocument.id}/ask`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ question }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Could not generate an answer");
      }

      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (error) {
      setMessage(error.message);
    } finally {
      setAsking(false);
    }
  }

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">D</div>
          <div>
            <h2>DocuMind</h2>
            <span>Document Intelligence Assistant</span>
          </div>
        </div>
        <span className="status">AI Powered</span>
      </header>

      <main className="layout">
        <aside className="sidebar">
          <h3>Your Documents</h3>

          <form onSubmit={handleUpload} className="upload-box">
            <label htmlFor="pdf-file">Upload a PDF</label>
            <input
              id="pdf-file"
              type="file"
              accept=".pdf,application/pdf"
              onChange={(event) => setFile(event.target.files[0])}
            />

            {file && <p className="file-name">{file.name}</p>}

            <button type="submit" disabled={uploading}>
              {uploading ? "Processing PDF..." : "Upload & Index"}
            </button>
          </form>

          <div className="document-list">
            {documents.map((doc) => (
              <button
                key={doc.id}
                className={`document-item ${
                  selectedDocument?.id === doc.id ? "selected" : ""
                }`}
                onClick={() => {
                  setSelectedDocument(doc);
                  setAnswer("");
                  setSources([]);
                  setMessage("");
                }}
              >
                <span className="pdf-icon">PDF</span>
                <span className="document-info">
                  <strong>{doc.filename}</strong>
                  <small>
                    {doc.status} · ID {doc.id}
                  </small>
                </span>
              </button>
            ))}

            {documents.length === 0 && (
              <p className="empty-text">No documents uploaded yet.</p>
            )}
          </div>
        </aside>

        <section className="chat-section">
          <div className="chat-heading">
            <div>
              <p className="eyebrow">DOCUMENT Q&A</p>
              <h1>Ask your documents.</h1>
              <p>Get answers grounded in your uploaded PDFs.</p>
            </div>
          </div>

          {selectedDocument ? (
            <div className="selected-document">
              <span>Selected document</span>
              <strong>{selectedDocument.filename}</strong>
              <small>Status: {selectedDocument.status}</small>
            </div>
          ) : (
            <div className="welcome">
              <div className="welcome-icon">✦</div>
              <h2>Welcome to DocuMind</h2>
              <p>Upload a PDF or select an indexed document to get started.</p>
            </div>
          )}

          {message && <div className="message">{message}</div>}

          <div className="answer-area">
            {asking && <p className="loading">Analyzing your document...</p>}

            {answer && (
              <div className="answer-card">
                <h3>Answer</h3>
                <div className="answer-text">
                  <ReactMarkdown>{answer}</ReactMarkdown>
                </div>

                {sources.length > 0 && (
                  <div className="sources">
                    <h4>Sources</h4>
                    {sources.map((source, index) => (
                      <div className="source-item" key={index}>
                        <strong>Chunk {source.chunk_index}</strong>
                        <p>{source.content}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>

          <form className="question-form" onSubmit={handleAsk}>
            <input
              type="text"
              placeholder={
                selectedDocument
                  ? "Ask something about this document..."
                  : "Select a document first..."
              }
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              disabled={!selectedDocument || asking}
            />
            <button
              type="submit"
              disabled={!selectedDocument || asking || !question.trim()}
            >
              {asking ? "Thinking..." : "Ask"}
            </button>
          </form>

          <p className="footer-note">
            AI-generated answers are based on retrieved document content.
          </p>
        </section>
      </main>
    </div>
  );
}

export default App;
