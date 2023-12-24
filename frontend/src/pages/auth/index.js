"use client";

import "./index.css";
import { useRouter } from "next/router";

const auth = () => {
  const router = useRouter();

  async function onSubmit(event) {
    event.preventDefault();

    const formData = new FormData(event.currentTarget);

    try {
      const response = await fetch("/api/token", {
        method: "POST",
        body: formData,
      });

      if (response) {
        const data = await response.json();

        if (data.access_token) {
          sessionStorage.setItem("accessToken", data.access_token);
          router.push("/");
        }
      }
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div className="bg-purple-900 text-white min-h-screen flex flex-col justify-center py-12 px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
       
        <img src="https://media.discordapp.net/attachments/1187038211839643792/1188058548727451678/output.png?ex=659924bf&is=6586afbf&hm=2c81d38f12a956655d5761b00ef4b21d21e493ddc1626e280472c14c5b3ccd49&=&format=webp&quality=lossless&width=455&height=455" alt="Company Logo" className="mx-auto mb-4" width={100} height={100}/>

        <h1 className="text-4xl font-bold mb-4">
          <i>CareCompanion ChatBot</i>
        </h1>
        <h2 className="text-2xl font-bold mb-8">
          Login into your account
        </h2>

        <form className="space-y-6" onSubmit={onSubmit} method="POST">
          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium leading-6"
            >
              Email address
            </label>
            <div className="mt-2">
              <input
                id="email"
                name="username"
                type="email"
                autoComplete="email"
                required
                className="block w-full rounded-md border-0 py-2 text-black bg-purple-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 placeholder-gray-400 text-sm"
              />
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between">
              <label
                htmlFor="password"
                className="block text-sm font-medium leading-6"
              >
                Password
              </label>
              <div className="text-sm">
                <a
                  href="#"
                  className="font-semibold text-indigo-500 hover:text-indigo-400"
                >
                  Forgot password?
                </a>
              </div>
            </div>
            <div className="mt-2">
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                className="block w-full rounded-md border-0 py-2 text-black bg-purple-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 placeholder-gray-400 text-sm"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              className="flex w-full justify-center rounded-md bg-indigo-600 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Sign in
            </button>
          </div>
        </form>

        <p className="mt-8 text-center text-sm text-gray-400">
         Don't have an account?{' '}
          <a
            href="#"
            className="font-semibold text-indigo-500 hover:text-indigo-400"
          >
            Click Here to create one
          </a>
        </p>
      </div>
    </div>
  );
};


const Registration = () => {
  const router = useRouter();

  const onSubmit = async (event) => {
    event.preventDefault();
    // Implement your registration logic here
    // Example: Make a POST request to create a new user
  };

  return (
    <div className="bg-purple-900 text-white min-h-screen flex flex-col justify-center py-12 px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <img
          src="https://media.discordapp.net/attachments/1187038211839643792/1188058548727451678/output.png?ex=659924bf&is=6586afbf&hm=2c81d38f12a956655d5761b00ef4b21d21e493ddc1626e280472c14c5b3ccd49&=&format=webp&quality=lossless&width=455&height=455"
          alt="Company Logo"
          className="mx-auto mb-4"
          width={100}
          height={100}
        />
        <h1 className="text-4xl font-bold mb-4">
          <i>Registration Form</i>
        </h1>
        {/* Registration form */}
        <form className="space-y-6" onSubmit={onSubmit} method="POST">
          {/* Email field */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium leading-6">
              Email address
            </label>
            <div className="mt-2">
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="block w-full rounded-md border-0 py-2 text-black bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 placeholder-gray-400 text-sm"
              />
            </div>
          </div>
          {/* First name field */}
          <div>
            <label htmlFor="firstName" className="block text-sm font-medium leading-6">
              First Name
            </label>
            <div className="mt-2">
              <input
                id="firstName"
                name="firstName"
                type="text"
                autoComplete="given-name"
                required
                className="block w-full rounded-md border-0 py-2 text-black bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 placeholder-gray-400 text-sm"
              />
            </div>
          </div>
          {/* Last name field */}
          <div>
            <label htmlFor="lastName" className="block text-sm font-medium leading-6">
              Last Name
            </label>
            <div className="mt-2">
              <input
                id="lastName"
                name="lastName"
                type="text"
                autoComplete="family-name"
                required
                className="block w-full rounded-md border-0 py-2 text-black bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 placeholder-gray-400 text-sm"
              />
            </div>
          </div>
          {/* Password field */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium leading-6">
              Password
            </label>
            <div className="mt-2">
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="new-password"
                required
                className="block w-full rounded-md border-0 py-2 text-black bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 placeholder-gray-400 text-sm"
              />
            </div>
          </div>
          {/* Submit button */}
          <div>
            <button
              type="submit"
              className="flex w-full justify-center rounded-md bg-indigo-600 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Sign Up
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};


export default auth;
