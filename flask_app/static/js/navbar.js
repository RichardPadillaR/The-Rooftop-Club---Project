var lis = document.querySelectorAll("li");

lis.forEach(function(li) {
  li.addEventListener("click", function() {
    // Remove "active" class from all lis
    lis.forEach(function(li) {
      li.classList.remove("active");
    });

    // Add "active" class to the clicked li
    this.classList.add("active");
  });
});