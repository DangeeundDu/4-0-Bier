function change_background() {
  var url_path_current = document.getElementById("content").style.backgroundImage;
  var url_path_new = "";
  do {
    url_path_new = "url(" + '"' + "images/wallpaper/glasses" + (Math.floor(Math.random() * 3) + 1) + "-bg.png" + '")';
  } while (url_path_current === url_path_new);
  document.getElementById("content").style.backgroundImage = url_path_new;
}