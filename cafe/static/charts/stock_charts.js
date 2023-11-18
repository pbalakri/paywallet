var ctx = document
  .getElementById("chart-product-count-by-stock")
  .getContext("2d");
new Chart(ctx, {
  type: "pie",
  data: JSON.parse(
    document.getElementById("get_product_count_based_on_stock").textContent
  ),
  options: {
    plugins: {
      title: {
        display: true,
        text: "Products by Stock Status",
      },
    },
  },
});
