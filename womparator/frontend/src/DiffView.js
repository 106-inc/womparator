import React from "react";
import ReactDiffViewer, { DiffMethod } from "react-diff-viewer";
import { useLocation } from "react-router-dom";


export default function DiffViewerPage() {

  const location = useLocation();
  const data = location.state;

  const newStyles = {
    variables: {
      light: {
        codeFoldGutterBackground: "#6F767E",
        codeFoldBackground: "#E2E4E5"
      }
    }
  };

  return (
    <div className="App">
      <ReactDiffViewer
        oldValue={JSON.stringify(data.descr, undefined, 4)}
        newValue={JSON.stringify(data.req, undefined, 4)}
        splitView={true}
        compareMethod={DiffMethod.WORDS}
        styles={newStyles}
        leftTitle="Customer"
        rightTitle="Requirements"
      />
    </div>
  );
};
