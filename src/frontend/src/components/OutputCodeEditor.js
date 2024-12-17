import React from 'react';
import Editor from "@monaco-editor/react";
import '../App.css'; 
import '../pages/Pages.css'

function OutputCodeEditor() {
  return (
    <div className='editor-container'>
      <Editor 
            defaultLanguage='python'
            theme='vs-dark'
            defaultValue={`
# Copy and paste your legacy code in this editor
"""

Example Code:

"""
class PythonLinter:
    def __init__(self):
        self.matchers: List[Matcher] = []

    def add_matcher(self, matcher: Matcher):
        """Add a matcher to the linter."""
        self.matchers.append(matcher)

    def lint(self, code: str) -> List[Dict]:
        """Parse code and run all matchers on the AST."""
        tree = ast.parse(code)
        diagnostics = []

        for node in ast.walk(tree):
            for matcher in self.matchers:
                diagnostics.extend(matcher.lint(node))

        return diagnostics`}
          />
    </div>
    
  );
}

export default OutputCodeEditor;
