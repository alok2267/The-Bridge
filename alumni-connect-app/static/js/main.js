/**
 * Toggles the sidebar navigation menu.
 * Slides the sidebar in and out and adjusts the main content margin.
 */
function toggleSidebar() {
  const sidebar = document.getElementById("mySidebar");
  const main = document.getElementById("main");

  if (sidebar.style.width === "250px") {
    sidebar.style.width = "0";
    main.style.marginLeft = "0";
  } else {
    sidebar.style.width = "250px";
    main.style.marginLeft = "250px";
  }
}

/**
 * Filters the alumni directory list based on user input in real-time.
 * This function is called on every key press in the search input field.
 */
function searchAlumni() {
  const input = document.getElementById('search');
  // Check if the search input exists on the page
  if (!input) return;

  const filter = input.value.toLowerCase();
  const ul = document.getElementById('alumniList');
  const li = ul.getElementsByTagName('li');

  // Loop through all list items, and hide those who don't match the search query
  for (let i = 0; i < li.length; i++) {
    let txtValue = li[i].textContent || li[i].innerText;
    if (txtValue.toLowerCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}

