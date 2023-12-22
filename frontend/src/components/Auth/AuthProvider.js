"use client";

import { useState, createContext, useEffect } from "react";
import { useRouter } from "next/router";

export const AuthContext = createContext({
  auth: {},
  setAuth: () => {},
});

export const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState();

  let sessionStorageAccessToken;

  if (typeof window !== "undefined") {
    const router = useRouter();
    sessionStorageAccessToken = sessionStorage.getItem("accessToken") || "";

    useEffect(() => {
      if (!sessionStorageAccessToken) {
        router.push("/auth");
      } else {
        setAuth(true);
      }
    }, [sessionStorageAccessToken]);
  }

  return (
    <AuthContext.Provider value={{ auth, setAuth }}>
      {children}
    </AuthContext.Provider>
  );
};
