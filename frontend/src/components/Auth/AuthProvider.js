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
      if (!auth) {
        const url = sessionStorageAccessToken ? "/" : "/auth";
        router.push(url);
      }
    }, [auth]);
  }

  return (
    <AuthContext.Provider value={{ auth, setAuth }}>
      {children}
    </AuthContext.Provider>
  );
};
