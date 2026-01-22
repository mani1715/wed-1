import React from 'react';

/**
 * EventContentFields Component
 * 
 * Renders event-type specific content fields dynamically based on event_type.
 * 
 * EVENT CONTENT STRUCTURE:
 * - Engagement: couple_names, engagement_date (optional - uses main date), venue_details
 * - Haldi: bride_name, groom_name, ceremony_time, dress_code
 * - Mehendi: bride_name, mehendi_time (optional - uses start_time), venue_details
 * - Marriage: Full details (uses all standard fields, can add additional custom content)
 * - Reception: couple_names, reception_time (optional - uses start_time), venue_details
 */
const EventContentFields = ({ eventType, eventContent = {}, onChange }) => {
  const handleFieldChange = (field, value) => {
    onChange({
      ...eventContent,
      [field]: value
    });
  };

  // Engagement fields
  if (eventType === 'engagement') {
    return (
      <div className="mt-4 p-4 bg-pink-50 border border-pink-200 rounded-lg">
        <h4 className="text-sm font-semibold text-pink-900 mb-3">Engagement Specific Details</h4>
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Couple Names
            </label>
            <input
              type="text"
              value={eventContent.couple_names || ''}
              onChange={(e) => handleFieldChange('couple_names', e.target.value)}
              placeholder="e.g., Rajesh & Priya"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            />
            <p className="text-xs text-gray-500 mt-1">Display couple's names for engagement ceremony</p>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Venue Details
            </label>
            <textarea
              value={eventContent.venue_details || ''}
              onChange={(e) => handleFieldChange('venue_details', e.target.value)}
              placeholder="Special venue details or notes"
              rows={2}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            />
          </div>
        </div>
      </div>
    );
  }

  // Haldi fields
  if (eventType === 'haldi') {
    return (
      <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
        <h4 className="text-sm font-semibold text-yellow-900 mb-3">Haldi Ceremony Details</h4>
        <div className="space-y-3">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Bride Name
              </label>
              <input
                type="text"
                value={eventContent.bride_name || ''}
                onChange={(e) => handleFieldChange('bride_name', e.target.value)}
                placeholder="Bride's name"
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Groom Name
              </label>
              <input
                type="text"
                value={eventContent.groom_name || ''}
                onChange={(e) => handleFieldChange('groom_name', e.target.value)}
                placeholder="Groom's name"
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
              />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Ceremony Time
            </label>
            <input
              type="text"
              value={eventContent.ceremony_time || ''}
              onChange={(e) => handleFieldChange('ceremony_time', e.target.value)}
              placeholder="e.g., Morning 10 AM onwards"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            />
            <p className="text-xs text-gray-500 mt-1">Specify special timing or duration</p>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Dress Code
            </label>
            <input
              type="text"
              value={eventContent.dress_code || ''}
              onChange={(e) => handleFieldChange('dress_code', e.target.value)}
              placeholder="e.g., Traditional Yellow Attire"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            />
          </div>
        </div>
      </div>
    );
  }

  // Mehendi fields
  if (eventType === 'mehendi') {
    return (
      <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
        <h4 className="text-sm font-semibold text-green-900 mb-3">Mehendi Ceremony Details</h4>
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Bride Name
            </label>
            <input
              type="text"
              value={eventContent.bride_name || ''}
              onChange={(e) => handleFieldChange('bride_name', e.target.value)}
              placeholder="Bride's name"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Mehendi Time
            </label>
            <input
              type="text"
              value={eventContent.mehendi_time || ''}
              onChange={(e) => handleFieldChange('mehendi_time', e.target.value)}
              placeholder="e.g., Evening 5 PM onwards"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            />
            <p className="text-xs text-gray-500 mt-1">Special timing for mehendi application</p>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Venue Details
            </label>
            <textarea
              value={eventContent.venue_details || ''}
              onChange={(e) => handleFieldChange('venue_details', e.target.value)}
              placeholder="Additional venue information or special notes"
              rows={2}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            />
          </div>
        </div>
      </div>
    );
  }

  // Marriage fields (most detailed)
  if (eventType === 'marriage') {
    return (
      <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
        <h4 className="text-sm font-semibold text-red-900 mb-3">Marriage Ceremony Details</h4>
        <div className="space-y-3">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Bride's Full Name
              </label>
              <input
                type="text"
                value={eventContent.bride_full_name || ''}
                onChange={(e) => handleFieldChange('bride_full_name', e.target.value)}
                placeholder="Bride's complete name"
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Groom's Full Name
              </label>
              <input
                type="text"
                value={eventContent.groom_full_name || ''}
                onChange={(e) => handleFieldChange('groom_full_name', e.target.value)}
                placeholder="Groom's complete name"
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
              />
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Bride's Parents
              </label>
              <input
                type="text"
                value={eventContent.bride_parents || ''}
                onChange={(e) => handleFieldChange('bride_parents', e.target.value)}
                placeholder="e.g., Mr. & Mrs. Sharma"
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Groom's Parents
              </label>
              <input
                type="text"
                value={eventContent.groom_parents || ''}
                onChange={(e) => handleFieldChange('groom_parents', e.target.value)}
                placeholder="e.g., Mr. & Mrs. Kumar"
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
              />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Muhurat Time (Auspicious Time)
            </label>
            <input
              type="text"
              value={eventContent.muhurat_time || ''}
              onChange={(e) => handleFieldChange('muhurat_time', e.target.value)}
              placeholder="e.g., 10:30 AM - 11:00 AM"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Rituals & Customs
            </label>
            <textarea
              value={eventContent.rituals || ''}
              onChange={(e) => handleFieldChange('rituals', e.target.value)}
              placeholder="Describe special rituals or customs"
              rows={2}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Dress Code
            </label>
            <input
              type="text"
              value={eventContent.dress_code || ''}
              onChange={(e) => handleFieldChange('dress_code', e.target.value)}
              placeholder="e.g., Traditional Indian Attire"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            />
          </div>
        </div>
      </div>
    );
  }

  // Reception fields
  if (eventType === 'reception') {
    return (
      <div className="mt-4 p-4 bg-purple-50 border border-purple-200 rounded-lg">
        <h4 className="text-sm font-semibold text-purple-900 mb-3">Reception Details</h4>
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Couple Names
            </label>
            <input
              type="text"
              value={eventContent.couple_names || ''}
              onChange={(e) => handleFieldChange('couple_names', e.target.value)}
              placeholder="e.g., Mr. & Mrs. Kumar"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Reception Time
            </label>
            <input
              type="text"
              value={eventContent.reception_time || ''}
              onChange={(e) => handleFieldChange('reception_time', e.target.value)}
              placeholder="e.g., Evening 7 PM onwards"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            />
            <p className="text-xs text-gray-500 mt-1">Specify cocktail/dinner timing</p>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Venue Details
            </label>
            <textarea
              value={eventContent.venue_details || ''}
              onChange={(e) => handleFieldChange('venue_details', e.target.value)}
              placeholder="Additional venue information (parking, dress code, etc.)"
              rows={2}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Dress Code
            </label>
            <input
              type="text"
              value={eventContent.dress_code || ''}
              onChange={(e) => handleFieldChange('dress_code', e.target.value)}
              placeholder="e.g., Formal / Semi-Formal"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            />
          </div>
        </div>
      </div>
    );
  }

  return null;
};

export default EventContentFields;
