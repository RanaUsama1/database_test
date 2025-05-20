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
    server: {
      proxy: {
        '/api': {
          target: 'http://localhost:8000', // Local backend
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        }
      }
    },
    base: isProduction ? "/database_test/" : "/",
    define: {
      __API_URL__: JSON.stringify(
        isProduction 
          ? "https://ncbibackend.vercel.app" 
          : "http://localhost:8000"
      ),
    },
  };
});
