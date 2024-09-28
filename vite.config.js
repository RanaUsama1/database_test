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

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "node:url";

export default defineConfig(({ command, mode }) => {
  const isProduction = mode === "production";

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
    },
    build: {
      rollupOptions: {
        external: ["vue-json-csv"],
      },
    },
    base: isProduction ? "/database_test/" : "/", // Correct base configuration
    define: {
      __API_URL__: JSON.stringify(
        isProduction
          ? "https://your-production-api-url"
          : "http://localhost:3000"
      ), // Set different API URL based on environment
    },
  };
});
