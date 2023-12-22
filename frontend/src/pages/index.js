"use client";

import { AuthProvider } from "@/components/Auth/AuthProvider";
import MainLayout from "@/app/layout";
import Chart from "@/components/Chat";

const home = () => {
  return (
    <AuthProvider>
      <MainLayout>
        <Chart />
      </MainLayout>
    </AuthProvider>
  );
};

export default home;
