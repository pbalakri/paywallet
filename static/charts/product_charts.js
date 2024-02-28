var ctx = document
  .getElementById("chart-product-count-by-category")
  .getContext("2d");
new Chart(ctx, {
  type: "pie",
  data: JSON.parse(
    document.getElementById("product_count_by_category").textContent
  ),
  options: {
    plugins: {
      title: {
        display: true,
        text: "Product count by category",
      },
    },
  },
});

var ctx = document
  .getElementById("chart-product-count-by-allergies")
  .getContext("2d");
new Chart(ctx, {
  type: "pie",
  data: JSON.parse(
    document.getElementById("product_count_by_allergies").textContent
  ),
  options: {
    plugins: {
      title: {
        display: true,
        text: "Product count by allergies",
      },
    },
  },
});
