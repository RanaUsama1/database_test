// import { fileURLToPath, URL } from "node:url";
// import { defineConfig } from "vite";
// import vue from "@vitejs/plugin-vue";

// // https://vitejs.dev/config/
// export default defineConfig(({ command, mode, ssrBuild }) => {
//   const ret = {
//     base: "/database_test/",
//     plugins: [vue()],
//     resolve: {
//       alias: {
//         "@": fileURLToPath(new URL("./src", import.meta.url)),
//       },
//     },
//   };
//   ret.define = {
//     __API_URL__: JSON.stringify("http://localhost:3000"),
//   };
//   return ret;
// });

// import { fileURLToPath, URL } from "node:url";
// import { defineConfig } from "vite";
// import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
// export default defineConfig(({ command, mode, ssrBuild }) => {
//   const isProduction = mode === "production";
//   const ret = {
//     base: isProduction ? "/database_test/" : "/",
//     plugins: [vue()],
//     resolve: {
//       alias: {
//         "@": fileURLToPath(new URL("./src", import.meta.url)),
//       },
//     },
//   };

//   ret.define = {
//     __API_URL__: JSON.stringify(
//       isProduction
//         ? "https://ranausama1.github.io/database_test/"
//         : "http://localhost:3000"
//     ),
//   };

//   return ret;
// });

// export default defineConfig(({ command, mode }) => {
//   const isProduction = mode === "production";
//   return {
//     base: isProduction ? "/database_test/" : "/", // Use the correct base for GitHub Pages
//     plugins: [vue()],
//     resolve: {
//       alias: {
//         "@": fileURLToPath(new URL("./src", import.meta.url)),
//       },
//     },
//   };
// });

// export default defineConfig({
//   // base: process.env.NODE_ENV === "production" ? "/database_test/" : "/",
//   base: "/database_test/",
//   plugins: [vue()],
// });

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "node:url";

export default defineConfig(({ command, mode }) => {
  const isProduction = mode === "production";

  return {
    base: isProduction ? "/database_test/" : "/", // Set base path for GitHub Pages
    plugins: [vue()], // Use Vue plugin
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)), // Alias for src
      },
    },
  };
});
