"use client";

import { useState, createContext, useEffect } from "react";
import { useRouter } from "next/router";

export const AuthContext = createContext({
  auth: {},
  setAuth: () => {},
  user: {},
  token: "",
});

export const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState();
  const [user, setUser] = useState();
  const [token, setToken] = useState();

  if (typeof window !== "undefined") {
    const router = useRouter();
    const sessionStorageAccessToken =
      sessionStorage.getItem("accessToken") || "";

    useEffect(() => {
      const fetchData = async () => {
        try {
          if (!sessionStorageAccessToken) {
            router.push("/auth");
          } else {
            const response = await fetch(`${process.env.API_URL}/users/me`, {
              method: "GET",
              headers: {
                Authorization: `Bearer ${sessionStorageAccessToken}`,
              },
            });
            const data = await response.json();

            setToken(sessionStorageAccessToken);
            setUser(data);

            if (response.ok) {
              setAuth(true);
            } else {
              console.error(
                "Failed to fetch user data:",
                response.status,
                response.statusText
              );
              window.location.pathname = "/";
              router.push("/auth");
            }
          }
        } catch (error) {
          console.error("Error fetching user data:", error);
          router.push("/auth");
        }
      };

      fetchData();
    }, [sessionStorageAccessToken]);
  }

  return (
    <AuthContext.Provider value={{ auth, setAuth, user, token }}>
      {children}
    </AuthContext.Provider>
  );
};
