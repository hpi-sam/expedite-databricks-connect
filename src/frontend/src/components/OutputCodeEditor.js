import React from 'react';
import Editor from "@monaco-editor/react";
import '../App.css'; 
import '../pages/Pages.css'

function OutputCodeEditor({ code }) {
  return (
    <div className='editor-container'>
      <Editor 
            height="90vh"
            defaultLanguage='python'
            theme='vs-dark'
            value={code}
            options={{
              readOnly: false,
              automaticLayout: true,
            }}
          />
    </div>
  );
}

export default OutputCodeEditor;
