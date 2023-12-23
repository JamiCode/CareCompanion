"use client";
import { useRouter } from "next/router";
import { AuthProvider } from "@/components/Auth/AuthProvider";
import MainLayout from "@/app/layout";
import Chat from "@/components/Chat";

const home = () => {
  const router = useRouter();
  const { id } = router.query;

  console.log("route", id?.[0]);
  return (
    <AuthProvider>
      <MainLayout>{id?.[0] ? <Chat /> : ""}</MainLayout>
    </AuthProvider>
  );
};

export default home;
