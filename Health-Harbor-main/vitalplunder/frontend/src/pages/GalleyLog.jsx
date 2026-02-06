import React, { useState } from 'react';
import { Utensils, Upload, Apple } from 'lucide-react';

function GalleyLog() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!image) return;
    setLoading(true);
    // TODO: API call to /api/galley-log/analyze with FormData
    // const formData = new FormData(); formData.append('image', image);
    // const response = await api.galleyLog.analyzeImage(formData);
    setTimeout(() => {
      setResult({
        food_item: 'Grilled Salmon with Vegetables',
        confidence: 0.87,
        nutrition: { calories: 420, protein: 35, carbs: 12, fat: 22, fiber: 4 },
        health_rating: 'Excellent',
        notes: 'Rich in omega-3 fatty acids and protein. Great choice!'
      });
      setLoading(false);
    }, 1500);
  };

  return (
    <div className="space-y-6 max-w-2xl">
      <div className="card">
        <div className="flex items-center gap-3 mb-4">
          <Utensils className="w-6 h-6 text-orange-400" />
          <h2 className="text-xl font-bold text-white">Diet & Nutrition Tracker</h2>
        </div>
        <p className="text-gray-400 text-sm">Upload a photo of your meal and let us analyze the nutritional content.</p>
      </div>

      <form onSubmit={handleAnalyze} className="card space-y-4">
        <div className="border-2 border-dashed border-navy-600 rounded-lg p-6 text-center">
          {preview ? (
            <div className="space-y-3">
              <img src={preview} alt="Food preview" className="max-h-48 mx-auto rounded-lg" />
              <button type="button" onClick={() => { setImage(null); setPreview(null); }} className="text-sm text-red-400 hover:text-red-300">Remove</button>
            </div>
          ) : (
            <label className="cursor-pointer block">
              <Upload className="w-12 h-12 text-gray-500 mx-auto mb-2" />
              <p className="text-gray-400">Click to upload food image</p>
              <p className="text-xs text-gray-500 mt-1">PNG, JPG up to 5MB</p>
              <input type="file" accept="image/*" className="hidden" onChange={handleImageChange} />
            </label>
          )}
        </div>
        <button type="submit" className="btn-primary w-full" disabled={loading || !image}>
          {loading ? 'Analyzing...' : '🍽️ Analyze Meal'}
        </button>
      </form>

      {result && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-white">{result.food_item}</h3>
            <span className={`px-2 py-1 rounded text-xs font-medium ${result.health_rating === 'Excellent' ? 'bg-green-900 text-green-300' : 'bg-yellow-900 text-yellow-300'}`}>
              {result.health_rating}
            </span>
          </div>
          <div className="grid grid-cols-5 gap-2 mb-4">
            {Object.entries(result.nutrition).map(([key, val]) => (
              <div key={key} className="text-center p-2 bg-navy-700 rounded">
                <div className="text-lg font-bold text-orange-400">{val}{key === 'calories' ? '' : 'g'}</div>
                <div className="text-xs text-gray-400 capitalize">{key}</div>
              </div>
            ))}
          </div>
          <div className="flex items-start gap-2 p-3 bg-navy-700/50 rounded-lg">
            <Apple className="w-5 h-5 text-green-400 mt-0.5" />
            <p className="text-sm text-gray-300">{result.notes}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default GalleyLog;
