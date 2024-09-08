import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig(({ command, mode, ssrBuild }) => {
  const ret = {
<<<<<<< HEAD
=======
    base: '/database_test/',
>>>>>>> 44e61027cd376e8c2bebdb7999e623fca78b13f1
    plugins: [vue()],
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
    },
  };
  ret.define = {
    __API_URL__: JSON.stringify("http://localhost:3000"),
  };
  return ret;
});
