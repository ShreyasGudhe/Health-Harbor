import React, { useState } from 'react';
import { FileText, Upload, AlertTriangle, Shield } from 'lucide-react';

function ShipDoctor() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const f = e.target.files[0];
    if (f) setFile(f);
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    // TODO: API call to /api/ship-doctor/analyze with FormData
    // const formData = new FormData(); formData.append('document', file);
    // const response = await api.shipDoctor.analyzeDocument(formData);
    setTimeout(() => {
      setResult({
        document_type: 'Blood Test Report',
        date_detected: '2026-01-10',
        summary: 'Overall results are within normal ranges. Cholesterol levels are slightly elevated.',
        key_findings: [
          { metric: 'Hemoglobin', value: '14.2 g/dL', status: 'normal' },
          { metric: 'Cholesterol', value: '210 mg/dL', status: 'elevated' },
          { metric: 'Blood Sugar', value: '95 mg/dL', status: 'normal' },
        ],
        recommendations: ['Consider dietary changes to lower cholesterol', 'Follow up in 3 months']
      });
      setLoading(false);
    }, 2000);
  };

  return (
    <div className="space-y-6 max-w-2xl">
      <div className="card">
        <div className="flex items-center gap-3 mb-4">
          <FileText className="w-6 h-6 text-teal-400" />
          <h2 className="text-xl font-bold text-white">Medical Document Analyzer</h2>
        </div>
        <p className="text-gray-400 text-sm">Upload your medical reports for AI-powered analysis and insights.</p>
      </div>

      {/* Medical Disclaimer */}
      <div className="card bg-red-900/20 border-red-700/30">
        <div className="flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-red-400 mt-0.5" />
          <div>
            <h4 className="font-semibold text-red-400 mb-1">Medical Disclaimer</h4>
            <p className="text-sm text-gray-400">
              This tool provides informational summaries only and is NOT a substitute for professional medical advice. 
              Always consult qualified healthcare providers for diagnosis and treatment decisions.
            </p>
          </div>
        </div>
      </div>

      <form onSubmit={handleAnalyze} className="card space-y-4">
        <div className="border-2 border-dashed border-navy-600 rounded-lg p-6 text-center">
          {file ? (
            <div className="space-y-2">
              <FileText className="w-12 h-12 text-teal-400 mx-auto" />
              <p className="text-white">{file.name}</p>
              <p className="text-xs text-gray-500">{(file.size / 1024).toFixed(1)} KB</p>
              <button type="button" onClick={() => setFile(null)} className="text-sm text-red-400 hover:text-red-300">Remove</button>
            </div>
          ) : (
            <label className="cursor-pointer block">
              <Upload className="w-12 h-12 text-gray-500 mx-auto mb-2" />
              <p className="text-gray-400">Upload medical document</p>
              <p className="text-xs text-gray-500 mt-1">PDF, PNG, JPG supported</p>
              <input type="file" accept=".pdf,.png,.jpg,.jpeg" className="hidden" onChange={handleFileChange} />
            </label>
          )}
        </div>
        <button type="submit" className="btn-primary w-full" disabled={loading || !file}>
          {loading ? 'Analyzing Document...' : '🔍 Analyze Document'}
        </button>
      </form>

      {result && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-semibold text-white">{result.document_type}</h3>
              <p className="text-xs text-gray-500">Detected date: {result.date_detected}</p>
            </div>
            <Shield className="w-6 h-6 text-teal-400" />
          </div>
          
          <div className="mb-4 p-3 bg-navy-700/50 rounded-lg">
            <p className="text-sm text-gray-300">{result.summary}</p>
          </div>

          <div className="mb-4">
            <h4 className="text-sm font-medium text-gray-400 mb-2">Key Findings</h4>
            <div className="space-y-2">
              {result.key_findings.map((f, i) => (
                <div key={i} className="flex items-center justify-between p-2 bg-navy-700 rounded">
                  <span className="text-white">{f.metric}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-gray-400">{f.value}</span>
                    <span className={`text-xs px-2 py-0.5 rounded ${f.status === 'normal' ? 'bg-green-900 text-green-300' : 'bg-yellow-900 text-yellow-300'}`}>
                      {f.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h4 className="text-sm font-medium text-gray-400 mb-2">Recommendations</h4>
            <ul className="space-y-1">
              {result.recommendations.map((r, i) => (
                <li key={i} className="text-sm text-gray-300 flex items-start gap-2">
                  <span className="text-teal-400">•</span> {r}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default ShipDoctor;
