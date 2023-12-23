"use client";

import { AuthProvider } from "@/components/Auth/AuthProvider";
import MainLayout from "@/app/layout";
import Chat from "@/components/Chat";

const home = () => {
  return (
    <AuthProvider>
      <MainLayout>
        <Chat />
      </MainLayout>
    </AuthProvider>
  );
};

export default home;
