var coll = document.getElementsByClassName("collapsible");
var arrow = document.getElementById("textarea_arrow")
var i;

window.onload

for (i = 0; i < coll.length; i++) {
coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    arrow.classList.toggle("flip")
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
        content.style.display = "none";
    } else {
        content.style.display = "block";
    }
});
}