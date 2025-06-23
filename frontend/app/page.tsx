'use client';

import { useState } from 'react';
import axios from 'axios';

type Suggestion = {
  issue: string;
  suggestion: string;
  example?: string;
};

type AnalysisResult = {
  score: number;
  technique: string;
  strengths: string[];
  issues: string[];
  suggestions: Suggestion[];
};

export default function Home() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState('');

  const analyzePrompt = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    setError('');
    
    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/analyze`,
        { prompt }
      );
      setResult(response.data);
    } catch (err) {
      setError('Failed to analyze prompt. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-green-600';
    if (score >= 5) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreEmoji = (score: number) => {
    if (score >= 8) return '🌟';
    if (score >= 5) return '💡';
    return '🎯';
  };

  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 text-center mb-2">
          Prompt Analyzer
        </h1>
        <p className="text-center text-gray-600 mb-8">
          Write better prompts with AI-powered feedback
        </p>

        {/* Input Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <label htmlFor="prompt" className="block text-sm font-medium text-gray-700 mb-2">
            Enter your prompt
          </label>
          <textarea
            id="prompt"
            rows={6}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., Write a story about a robot learning to paint..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            maxLength={2000}
          />
          <div className="mt-2 flex justify-between items-center">
            <span className="text-sm text-gray-500">
              {prompt.length} / 2000 characters
            </span>
            <button
              onClick={analyzePrompt}
              disabled={loading || !prompt.trim()}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Analyzing...' : 'Analyze Prompt'}
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-8">
            {error}
          </div>
        )}

        {/* Results Section */}
        {result && (
          <div className="space-y-6">
            {/* Score Card */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-semibold">Analysis Results</h2>
                <div className={`text-4xl font-bold ${getScoreColor(result.score)}`}>
                  {result.score}/10 {getScoreEmoji(result.score)}
                </div>
              </div>
              
              <div className="mb-4">
                <span className="inline-block bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full">
                  Technique: {result.technique}
                </span>
              </div>

              {/* Strengths */}
              {result.strengths.length > 0 && (
                <div className="mb-4">
                  <h3 className="font-semibold text-green-700 mb-2">✅ Strengths</h3>
                  <ul className="list-disc list-inside space-y-1">
                    {result.strengths.map((strength, idx) => (
                      <li key={idx} className="text-gray-700">{strength}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Issues */}
              {result.issues.length > 0 && (
                <div>
                  <h3 className="font-semibold text-red-700 mb-2">⚠️ Areas for Improvement</h3>
                  <ul className="list-disc list-inside space-y-1">
                    {result.issues.map((issue, idx) => (
                      <li key={idx} className="text-gray-700">{issue}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Suggestions */}
            {result.suggestions.length > 0 && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold mb-4">💡 Suggestions</h3>
                <div className="space-y-4">
                  {result.suggestions.map((suggestion, idx) => (
                    <div key={idx} className="border-l-4 border-blue-500 pl-4">
                      <p className="font-medium text-gray-900 mb-1">{suggestion.issue}</p>
                      <p className="text-gray-700 mb-2">{suggestion.suggestion}</p>
                      {suggestion.example && (
                        <div className="bg-gray-50 p-3 rounded text-sm">
                          <span className="font-medium">Example: </span>
                          <span className="text-gray-600">{suggestion.example}</span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
