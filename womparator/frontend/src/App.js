import { Routes, Route } from "react-router-dom";
import ImportFiles from "./ImportFiles"
import CsvTableView from "./CsvTableView"

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<ImportFiles />} />
      <Route path="/csv-table-view" element={<CsvTableView />} />
    </Routes>
  );
}
