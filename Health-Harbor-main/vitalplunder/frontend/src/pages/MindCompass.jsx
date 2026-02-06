import React, { useState } from 'react';
import { Brain, Smile, Frown, Meh } from 'lucide-react';

function MindCompass() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setLoading(true);
    // TODO: API call to /api/mind-compass/analyze
    // const response = await api.mindCompass.analyze({ text });
    setTimeout(() => {
      setResult({ sentiment: 'positive', stress_level: 'low', confidence: 0.78, suggestion: 'Keep up the positive mindset!' });
      setLoading(false);
    }, 1000);
  };

  const getEmoji = (sentiment) => {
    if (sentiment === 'positive') return <Smile className="w-8 h-8 text-green-400" />;
    if (sentiment === 'negative') return <Frown className="w-8 h-8 text-red-400" />;
    return <Meh className="w-8 h-8 text-yellow-400" />;
  };

  return (
    <div className="space-y-6 max-w-2xl">
      <div className="card">
        <div className="flex items-center gap-3 mb-4">
          <Brain className="w-6 h-6 text-purple-400" />
          <h2 className="text-xl font-bold text-white">Mental Health Monitor</h2>
        </div>
        <p className="text-gray-400 text-sm">Share your thoughts and feelings. We'll help navigate your emotional waters.</p>
      </div>

      <form onSubmit={handleAnalyze} className="card space-y-4">
        <div>
          <label className="block text-sm text-gray-400 mb-2">How are you feeling today?</label>
          <textarea 
            className="input-field min-h-[120px] resize-none" 
            placeholder="I've been feeling a bit overwhelmed with work lately, but I'm trying to stay positive..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn-primary w-full" disabled={loading || !text.trim()}>
          {loading ? 'Analyzing...' : '🧭 Analyze Mood'}
        </button>
      </form>

      {result && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-white">Analysis Result</h3>
            {getEmoji(result.sentiment)}
          </div>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-400">Sentiment:</span>
              <span className="text-white capitalize font-medium">{result.sentiment}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Stress Level:</span>
              <span className={`font-medium ${result.stress_level === 'high' ? 'text-red-400' : result.stress_level === 'moderate' ? 'text-yellow-400' : 'text-green-400'}`}>
                {result.stress_level}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Confidence:</span>
              <span className="text-white">{(result.confidence * 100).toFixed(0)}%</span>
            </div>
            <div className="pt-3 border-t border-navy-600">
              <p className="text-teal-400 text-sm">💡 {result.suggestion}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default MindCompass;
