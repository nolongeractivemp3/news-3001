// vibe coded remake later
function loadTable(tableId, fields, data) {
  var rows = "";
  $.each(data, function (index, item) {
    var row = "<tr>";
    $.each(fields, function (fIndex, field) {
      var content = item[field] ?? "";

      // My Opinion: Logic belongs here to transform the raw data into a button
      if (field === "link") {
        content = `<a href="${content}" role="button" target="_blank">Open</a>`;
      }

      row += "<td>" + content + "</td>";
    });
    rows += row + "</tr>"; // Fixed the </tr> typo too
  });
  $("#" + tableId).html(rows);
}

// Use this target ID instead
const fetchNews = fetch("http://localhost:5000/");

fetchNews
  .then((response) => response.json())
  .then((data) =>
    loadTable(
      "newsTableBody",
      ["Source", "title", "description", "link"],
      data,
    ),
  );
