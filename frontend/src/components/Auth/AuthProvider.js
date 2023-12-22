"use client";

import { useState, createContext, useEffect } from "react";
import { useRouter } from "next/router";

export const AuthContext = createContext({
  auth: {},
  setAuth: () => {},
});

export const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState();
  const [user, setUser] = useState();

  if (typeof window !== "undefined") {
    const router = useRouter();
    const sessionStorageAccessToken =
      sessionStorage.getItem("accessToken") || "";

    useEffect(() => {
      const fetchData = async () => {
        try {
          if (!sessionStorageAccessToken) {
            console.log("reutrn");
            router.push("/auth");
          } else {
            const response = await fetch("/api/users/me", {
              method: "GET",
              headers: {
                Authorization: `Bearer ${sessionStorageAccessToken}`,
              },
            });
            setUser(response);

            if (response.ok) {
              setAuth(true);
            } else {
              console.error(
                "Failed to fetch user data:",
                response.status,
                response.statusText
              );
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
    <AuthContext.Provider value={{ auth, setAuth, user }}>
      {children}
    </AuthContext.Provider>
  );
};
