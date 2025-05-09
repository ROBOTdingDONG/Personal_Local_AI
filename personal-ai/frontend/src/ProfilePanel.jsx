// frontend/src/ProfilePanel.jsx
// Placeholder content
import React, { useState, useEffect } from 'react';

function ProfilePanel() {
  const [profileData, setProfileData] = useState(null);

  // Placeholder: In a real app, you might fetch this or have it passed via props
  // For now, it could try to fetch from a dedicated endpoint if you create one,
  // or display a message about where profile.json is located.
  useEffect(() => {
    // This is a conceptual fetch. You would need a backend endpoint 
    // that serves profile.json or parts of it.
    // fetch('/api/profile')
    //   .then(res => res.json())
    //   .then(data => setProfileData(data))
    //   .catch(err => console.error("Could not fetch profile:", err));
    setProfileData({ info: "Profile data will be displayed here. (profile.json is managed server-side)" });
  }, []);

  return (
    <div>
      <h2>User Profile</h2>
      {profileData ? (
        <pre>{JSON.stringify(profileData, null, 2)}</pre>
      ) : (
        <p>Loading profile...</p>
      )}
      <p><small>The <code>profile.json</code> is stored and updated on the backend in <code>personal-ai/backend/memory/profile.json</code>.</small></p>
    </div>
  );
}

export default ProfilePanel;
