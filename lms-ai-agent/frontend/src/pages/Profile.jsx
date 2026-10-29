import { useEffect, useState } from "react";
import api from "../api/axios";
import ProfileForm from "../components/ProfileForm";
import ChatWidget from "../components/ChatWidget";

export default function Profile() {
  const [profile, setProfile] = useState(null);

  const fetchProfile = async () => {
    const response = await api.get("/profile");
    setProfile(response.data);
  };

  useEffect(() => {
    let active = true;
    api.get("/profile").then((response) => {
      if (active) {
        setProfile(response.data);
      }
    });

    return () => {
      active = false;
    };
  }, []);

  return (
    <>
      <ProfileForm profile={profile} refresh={fetchProfile} />
      <ChatWidget refresh={fetchProfile} />
    </>
  );
}