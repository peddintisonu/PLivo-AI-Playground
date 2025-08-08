// frontend/src/components/Playground.jsx
import { useState } from 'react';
import SkillSelector from './SkillSelector';
// We will create these UI components next
import SummarizationUI from './SummarizationUI';
import ImageAnalysisUI from './ImageAnalysisUI';
import ConversationAnalysisUI from './ConversationAnalysisUI';

const SKILLS = {
  SUMMARIZATION: 'Document/URL Summarization',
  IMAGE_ANALYSIS: 'Image Analysis',
  CONVERSATION_ANALYSIS: 'Conversation Analysis',
};

export default function Playground() {
  const [selectedSkill, setSelectedSkill] = useState(SKILLS.SUMMARIZATION);
  const [isLoading, setIsLoading] = useState(false);
  const [output, setOutput] = useState(null);
  const [error, setError] = useState('');

  const renderSkillUI = () => {
    // This is where you'll pass the setIsLoading, setOutput, setError functions
    // so each UI component can trigger API calls and update the state.
    const commonProps = { setIsLoading, setOutput, setError };

    switch (selectedSkill) {
      case SKILLS.SUMMARIZATION:
        return <SummarizationUI {...commonProps} />;
      case SKILLS.IMAGE_ANALYSIS:
        return <ImageAnalysisUI {...commonProps} />;
      case SKILLS.CONVERSATION_ANALYSIS:
        return <ConversationAnalysisUI {...commonProps} />;
      default:
        return null;
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <SkillSelector
        skills={Object.values(SKILLS)}
        selectedSkill={selectedSkill}
        setSelectedSkill={setSelectedSkill}
      />
      
      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Input Section */}
        <div className="bg-[#121212] p-6 rounded-lg border border-gray-800">
          <h2 className="text-lg font-semibold mb-4">{selectedSkill}</h2>
          {renderSkillUI()}
        </div>
        
        {/* Output Section */}
        <div className="bg-[#121212] p-6 rounded-lg border border-gray-800 min-h-[300px]">
          <h2 className="text-lg font-semibold mb-4">Output</h2>
          {isLoading ? (
            <div className="flex items-center justify-center h-full">
              <p>Loading...</p> {/* You can add a spinner icon here */}
            </div>
          ) : error ? (
            <div className="text-red-400">{error}</div>
          ) : output ? (
            selectedSkill === SKILLS.CONVERSATION_ANALYSIS && output.transcript ? (
              // Special formatting for conversation analysis
              <div className="space-y-6">
                <div>
                  <h3 className="text-md font-semibold text-blue-400 mb-2">Transcript (10 points)</h3>
                  <div className="bg-gray-800 p-4 rounded border text-gray-300">
                    <pre className="whitespace-pre-wrap text-sm">{output.transcript}</pre>
                  </div>
                </div>
                <div>
                  <h3 className="text-md font-semibold text-green-400 mb-2">Diarization (10 points)</h3>
                  <div className="bg-gray-800 p-4 rounded border text-gray-300">
                    <pre className="whitespace-pre-wrap text-sm">{output.diarization}</pre>
                  </div>
                </div>
                <div>
                  <h3 className="text-md font-semibold text-purple-400 mb-2">Summary & Analysis</h3>
                  <div className="bg-gray-800 p-4 rounded border text-gray-300">
                    <pre className="whitespace-pre-wrap text-sm">{output.summary}</pre>
                  </div>
                </div>
              </div>
            ) : (
              // Standard output for other skills
              <pre className="whitespace-pre-wrap text-gray-300">{JSON.stringify(output, null, 2)}</pre>
            )
          ) : (
            <div className="text-gray-500 text-center">No output yet. Select a skill and provide input to get started.</div>
          )}
        </div>
      </div>
    </div>
  );
}