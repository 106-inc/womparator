import { Routes, Route } from "react-router-dom";
import ImportFiles from "./ImportFiles"
import DiffViewerPage from "./DiffView";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<ImportFiles />} />
      <Route path="/diff-view" element={<DiffViewerPage />} />
    </Routes>
  );
}
