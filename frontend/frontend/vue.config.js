const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
});
//Required to avoid lint errors 
// chainWebpack: config => {
//   config.module.rule('eslint').use('eslint-loader').options({
//     fix: true
//   })
// }
