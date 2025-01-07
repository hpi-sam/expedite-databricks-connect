import React from 'react';
import Editor from "@monaco-editor/react";
import '../App.css'; 
import '../pages/Pages.css'

function InputCodeEditor({ code, setCode }) {
  const handleEditorChange = (value, event) => {
    setCode(value);
  };

  return (
    <div className='editor-container'>
      <Editor 
            height="90vh"
            defaultLanguage='python'
            theme='vs-dark'
            value={code}
            onChange={handleEditorChange}
            options={{
              automaticLayout: true,
            }}
          />
    </div>
    
  );
}

export default InputCodeEditor;
