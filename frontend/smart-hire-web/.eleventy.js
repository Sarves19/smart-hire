const { ICONS } = require("./src/_data/icons.js");

module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy({ "src/js": "assets/js" });

  eleventyConfig.addShortcode("icon", function (name, cls = "") {
    const path = ICONS[name];
    if (!path) return "";
    return `<svg class="ic ${cls}" viewBox="0 0 24 24" aria-hidden="true">${path}</svg>`;
  });

  eleventyConfig.addFilter("money", function (n) {
    return "$" + Number(n).toLocaleString("en-US");
  });

  eleventyConfig.addPairedShortcode("raw", function (content) {
    return content;
  });

  // Every internal link in this project is written as a flat "/section/page.html"
  // URL. Eleventy's default permalink nests non-index templates into pretty
  // "/section/page/index.html" directories instead, so override it globally.
  eleventyConfig.addGlobalData("eleventyComputed", {
    permalink: (data) => `${data.page.filePathStem}.html`,
  });

  return {
    dir: {
      input: "src/pages",
      includes: "../_includes",
      data: "../_data",
      output: "_site",
    },
    templateFormats: ["njk", "html"],
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
  };
};
