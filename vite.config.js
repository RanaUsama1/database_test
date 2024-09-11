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

import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig(({ command, mode, ssrBuild }) => {
  const isProduction = mode === "production";
  const ret = {
    base: isProduction ? "/database_test/" : "/",
    plugins: [vue()],
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
    },
  };

  ret.define = {
    __API_URL__: JSON.stringify(
      isProduction
        ? "https://ranausama1.github.io/database_test/"
        : "http://localhost:3000"
    ),
  };

  return ret;
});
